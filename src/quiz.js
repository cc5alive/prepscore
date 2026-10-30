(function () {
  "use strict";
  var D = window.PREP;
  var ROOT = document.body.getAttribute("data-root") || "";
  var KEY = "prepscore.answers.v1";
  var state = { loc: "suburbs", people: 2, a: {} };

  function load() {
    try { var s = JSON.parse(localStorage.getItem(KEY) || "null"); if (s && s.a) state = Object.assign(state, s); } catch (e) {}
    var h = (location.hash || "").replace("#", "");
    if (h && D.locations.some(function (l) { return l.slug === h; })) state.loc = h;
  }
  function save() { try { localStorage.setItem(KEY, JSON.stringify(state)); } catch (e) {} }

  function loc() { return D.locations.filter(function (l) { return l.slug === state.loc; })[0] || D.locations[1]; }
  function weight(q) {
    var L = loc();
    return q.w * ((L.mult || {})[q.cat] || 1) * ((L.item || {})[q.id] || 1);
  }
  function value(q) {
    var v = state.a[q.id];
    if (q.type === "choice") return v == null ? 0 : q.choices[v][1];
    return v ? 1 : 0;
  }
  function tierFor(score) {
    for (var i = 0; i < D.tiers.length; i++) if (score >= D.tiers[i].min && score <= D.tiers[i].max) return D.tiers[i];
    return D.tiers[0];
  }
  function compute() {
    var tot = 0, got = 0, cats = {};
    D.cats.forEach(function (c) { cats[c.id] = { t: 0, g: 0 }; });
    D.quiz.forEach(function (q) {
      var w = weight(q), v = value(q);
      tot += w; got += w * v; cats[q.cat].t += w; cats[q.cat].g += w * v;
    });
    var score = Math.round(100 * got / tot);
    var qw = D.quiz.filter(function (q) { return q.id === "w_store"; })[0];
    var qf = D.quiz.filter(function (q) { return q.id === "f_store"; })[0];
    var wd = state.a.w_store == null ? 0 : qw.choices[state.a.w_store][2];
    var fd = state.a.f_store == null ? 1 : qf.choices[state.a.f_store][2];
    if (state.a.w_filter) wd += 7;
    if (state.a.w_heater) wd += Math.max(1, Math.round(12 / state.people));
    var days = Math.min(wd, fd);
    var gaps = D.quiz.map(function (q) { return { q: q, miss: weight(q) * (1 - value(q)) }; })
      .filter(function (g) { return g.miss > 0.01; })
      .sort(function (a, b) { return b.miss - a.miss; }).slice(0, 5);
    var catPct = {};
    Object.keys(cats).forEach(function (k) { catPct[k] = Math.round(100 * cats[k].g / cats[k].t); });
    return { score: score, days: days, tier: tierFor(score), cats: catPct, gaps: gaps };
  }

  function daysLabel(d) { return d >= 90 ? "90+" : String(d); }

  // ---------- render ----------
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

  function syncInputs() {
    $$(".chip[data-loc]").forEach(function (b) { b.setAttribute("aria-pressed", String(b.dataset.loc === state.loc)); });
    $("#people-out").textContent = state.people;
    D.quiz.forEach(function (q) {
      if (q.type === "choice") {
        $$('input[name="' + q.id + '"]').forEach(function (inp) { inp.checked = String(state.a[q.id]) === inp.value; });
      } else {
        var el = $("#" + q.id); if (el) el.checked = !!state.a[q.id];
      }
    });
  }

  function render() {
    var r = compute();
    var t = r.tier;
    $$("[data-out=score]").forEach(function (e) { e.textContent = r.score; });
    $$("[data-out=days]").forEach(function (e) { e.textContent = daysLabel(r.days); });
    $$("[data-out=tier]").forEach(function (e) { e.textContent = t.name; });
    $$("[data-out=line]").forEach(function (e) { e.textContent = t.line; });
    $$("[data-out=dayword]").forEach(function (e) { e.textContent = r.days === 1 ? "day on your own" : "days on your own"; });
    $$(".tier-chip").forEach(function (e) { e.style.setProperty("--tier", t.color); e.style.color = t.text; e.textContent = t.name; });
    $$("[data-cat-bar]").forEach(function (e) { e.style.width = r.cats[e.dataset.catBar] + "%"; });
    $$("[data-cat-pct]").forEach(function (e) { e.textContent = r.cats[e.dataset.catPct] + "%"; });
    var L = loc();
    $$("[data-out=loc]").forEach(function (e) { e.textContent = L.name; });

    var n = state.people;
    $("#t-water").textContent = (14 * n) + " gal";
    $("#t-food").textContent = (28 * n) + "k kcal";
    $("#t-bags").textContent = (14 * n * 2);

    var ul = $("#gaps"); ul.innerHTML = "";
    if (!r.gaps.length) { ul.innerHTML = "<li><b>No gaps left.</b><span>Now practice the plan with your household.</span></li>"; }
    r.gaps.forEach(function (g) {
      var c = D.cats.filter(function (c) { return c.id === g.q.cat; })[0];
      var li = document.createElement("li");
      var label = g.q.type === "choice" ? g.q.label.replace(/\?$/, "") : g.q.label;
      li.innerHTML = "<b></b><span></span>" + (c.guide ? ' <a href="' + ROOT + "guides/" + c.guide + '.html">' + c.name + " guide</a>" : "");
      li.querySelector("b").textContent = label;
      li.querySelector("span").textContent = g.q.tip + " ";
      ul.appendChild(li);
    });
    window.__result = r;
    drawCard(r);
  }

  // ---------- share card ----------
  var fontsReady = (document.fonts && document.fonts.load) ? Promise.all([
    document.fonts.load('900 120px "Big Shoulders Display"'),
    document.fonts.load('800 60px "Big Shoulders Display"'),
    document.fonts.load('600 28px "Public Sans"')
  ]).catch(function () {}) : Promise.resolve();

  function cssVar(n) { return getComputedStyle(document.documentElement).getPropertyValue(n).trim(); }

  function drawCard(r) {
    var cv = $("#card"); if (!cv) return;
    fontsReady.then(function () {
      var x = cv.getContext("2d"), W = 1200, H = 630;
      var ink = "#142019", paper = "#ECEFE8", surf = "#F7F8F3", muted = "#55625A", sig = "#F2B705";
      x.fillStyle = paper; x.fillRect(0, 0, W, H);
      // crate frame
      x.fillStyle = ink; x.fillRect(48, 48, W - 84, H - 84);
      x.fillStyle = surf; x.fillRect(36, 36, W - 84, H - 84);
      x.strokeStyle = ink; x.lineWidth = 5; x.strokeRect(36, 36, W - 84, H - 84);
      // top strip
      x.beginPath(); x.moveTo(36, 106); x.lineTo(W - 48, 106); x.stroke();
      x.fillStyle = ink; x.font = '700 24px "Public Sans", sans-serif'; x.textBaseline = "middle";
      x.fillText("PREPSCORE  ·  " + loc().name.toUpperCase(), 64, 72);
      x.textAlign = "right"; x.fillText("HOW LONG WOULD YOU LAST?  " + D.site.host.toUpperCase(), W - 76, 72); x.textAlign = "left";
      // days
      x.textBaseline = "alphabetic";
      x.font = '900 230px "Big Shoulders Display", Impact, sans-serif';
      var dl = daysLabel(r.days);
      x.fillText(dl, 60, 330);
      var dw = x.measureText(dl).width;
      x.font = '800 44px "Big Shoulders Display", sans-serif';
      x.fillText(r.days === 1 ? "DAY" : "DAYS", 80 + dw, 248);
      x.fillText("ON MY OWN", 80 + dw, 298);
      // score
      x.textAlign = "right";
      x.font = '900 150px "Big Shoulders Display", Impact, sans-serif';
      x.fillText(String(r.score), W - 80, 300);
      x.font = '600 24px "Public Sans", sans-serif'; x.fillStyle = muted;
      x.fillText("PREPSCORE / 100", W - 80, 336);
      x.textAlign = "left";
      // tier
      x.fillStyle = r.tier.color; x.fillRect(64, 372, 16, 64);
      x.fillStyle = ink; x.font = '800 66px "Big Shoulders Display", sans-serif';
      x.fillText(r.tier.name, 96, 430);
      x.fillStyle = muted; x.font = '500 28px "Public Sans", sans-serif';
      x.fillText(r.tier.line, 66, 478);
      // bars
      var cats = D.cats, bx = 64, by = 512, colW = (W - 84 - 56) / 5;
      x.font = '600 17px "Public Sans", sans-serif';
      cats.forEach(function (c, i) {
        var cx = bx + (i % 5) * colW, cy = by + Math.floor(i / 5) * 34;
        x.fillStyle = ink; x.fillText(c.short, cx, cy + 6);
        x.fillStyle = "#C8D0C5"; x.fillRect(cx + 100, cy - 4, colW - 120, 9);
        x.fillStyle = ink; x.fillRect(cx + 100, cy - 4, (colW - 120) * r.cats[c.id] / 100, 9);
      });
      // hazard band + url
      x.save(); x.beginPath(); x.rect(36, H - 60, W - 84, 12); x.clip();
      for (var s = -40; s < W; s += 28) { x.fillStyle = sig; x.beginPath(); x.moveTo(s, H - 48); x.lineTo(s + 14, H - 48); x.lineTo(s + 26, H - 60); x.lineTo(s + 12, H - 60); x.fill(); }
      x.restore();
    });
  }

  function shareUrl() {
    var r = window.__result;
    return D.site.url + "/score/" + r.tier.slug + "#s" + r.score + "-d" + r.days;
  }
  function shareText() {
    var r = window.__result;
    return "I could last " + daysLabel(r.days) + (r.days === 1 ? " day" : " days") + " on my own. PrepScore " + r.score + "/100: " + r.tier.name + ". How long would you last?";
  }
  function status(msg) { var s = $("#share-status"); if (s) s.textContent = msg; }

  function wireShare() {
    $("#btn-share").addEventListener("click", function () {
      var cv = $("#card");
      var data = { title: "My PrepScore", text: shareText(), url: shareUrl() };
      try {
        cv.toBlob(function (blob) {
          var file = blob && new File([blob], "prepscore.png", { type: "image/png" });
          if (file && navigator.canShare && navigator.canShare({ files: [file] })) {
            navigator.share(Object.assign({ files: [file] }, data)).catch(function () {});
          } else if (navigator.share) {
            navigator.share(data).catch(function () { status("Sharing isn't available here. Use Copy link or Save image."); });
          } else { status("Sharing isn't available in this browser. Use Copy link or Save image."); }
        }, "image/png");
      } catch (e) { status("Sharing isn't available here. Use Copy link."); }
    });
    $("#btn-save").addEventListener("click", function () {
      try {
        var a = document.createElement("a");
        a.href = $("#card").toDataURL("image/png"); a.download = "my-prepscore.png";
        document.body.appendChild(a); a.click(); a.remove();
        status("Image saved.");
      } catch (e) { status("Saving isn't available here. Long-press or right-click the card to save it."); }
    });
    $("#btn-copy").addEventListener("click", function () {
      var txt = shareText() + " " + shareUrl();
      var p = navigator.clipboard && navigator.clipboard.writeText ? navigator.clipboard.writeText(txt) : Promise.reject();
      p.then(function () { status("Link copied."); }, function () {
        var ta = $("#copy-fallback"); ta.hidden = false; ta.value = txt; ta.select(); status("Press Ctrl+C or Cmd+C to copy.");
      });
    });
    function intent(sel, fn) { var a = $(sel); a.addEventListener("click", function () { a.href = fn(); }); a.addEventListener("focus", function () { a.href = fn(); }); a.addEventListener("mouseenter", function () { a.href = fn(); }); }
    intent("#s-x", function () { return "https://twitter.com/intent/tweet?text=" + encodeURIComponent(shareText()) + "&url=" + encodeURIComponent(shareUrl()); });
    intent("#s-fb", function () { return "https://www.facebook.com/sharer/sharer.php?u=" + encodeURIComponent(shareUrl()); });
    intent("#s-reddit", function () { return "https://www.reddit.com/submit?url=" + encodeURIComponent(shareUrl()) + "&title=" + encodeURIComponent(shareText()); });
    intent("#s-wa", function () { return "https://wa.me/?text=" + encodeURIComponent(shareText() + " " + shareUrl()); });
  }

  function wire() {
    $$(".chip[data-loc]").forEach(function (b) {
      b.addEventListener("click", function () { state.loc = b.dataset.loc; save(); syncInputs(); render(); });
    });
    $("#people-minus").addEventListener("click", function () { state.people = Math.max(1, state.people - 1); save(); syncInputs(); render(); });
    $("#people-plus").addEventListener("click", function () { state.people = Math.min(12, state.people + 1); save(); syncInputs(); render(); });
    document.addEventListener("change", function (e) {
      var t = e.target;
      if (!t.matches || !t.matches("[data-q]")) return;
      if (t.type === "radio") state.a[t.name] = Number(t.value);
      else state.a[t.id] = t.checked;
      save(); render();
    });
    $("#btn-reset").addEventListener("click", function () { state.a = {}; save(); syncInputs(); render(); status(""); });
    wireShare();
  }

  load(); syncInputs(); wire(); render();
})();
