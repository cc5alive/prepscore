(function () {
  "use strict";
  var D = window.PREP;
  var ROOT = document.body.getAttribute("data-root") || "";
  var KEY = "prepscore.answers.v1";
  var state = { loc: "suburbs", people: 2, a: {} };

  function load() {
    try { var s = JSON.parse(localStorage.getItem(KEY) || "null"); if (s && s.a) state = Object.assign(state, s); } catch (e) {}
    // #earthquake-country or #earthquake-country,los-angeles (from a city guide)
    var h = (location.hash || "").replace("#", "").split(",");
    if (h[0] && D.locations.some(function (l) { return l.slug === h[0]; })) {
      state.loc = h[0];
      state.city = (h[1] && D.cities[h[1]]) ? h[1] : null;
    }
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
    // Days come only from what's actually stored. A filter needs a water source, so it adds no days.
    // An unanswered question means "unknown", never a guess.
    var wd = state.a.w_store == null ? null : qw.choices[state.a.w_store][2];
    var heater = 0;
    if (wd != null && state.a.w_heater) { heater = Math.max(1, Math.round(12 / state.people)); wd += heater; }
    var fd = state.a.f_store == null ? null : qf.choices[state.a.f_store][2];
    var days = (wd == null || fd == null) ? null : Math.min(wd, fd);
    var gaps = D.quiz.map(function (q) { return { q: q, miss: weight(q) * (1 - value(q)) }; })
      .filter(function (g) { return g.miss > 0.01; })
      .sort(function (a, b) { return b.miss - a.miss; }).slice(0, 8);
    var catPct = {};
    Object.keys(cats).forEach(function (k) { catPct[k] = Math.round(100 * cats[k].g / cats[k].t); });
    return { score: score, days: days, water: wd, food: fd, heater: heater, tier: tierFor(score), cats: catPct, gaps: gaps };
  }

  function daysLabel(d) { return d == null ? "?" : d >= 90 ? "90+" : String(d); }
  function dayWord(d) { return d === 1 ? "day" : "days"; }
  function limitsText(r) {
    var w = r.water == null ? "Water: not answered yet" :
      r.water === 0 ? "Water: none stored" :
      "Water: about " + daysLabel(r.water) + " " + dayWord(r.water) + (r.heater ? ", counting your water heater" : "");
    var f = r.food == null ? "Food: not answered yet" : "Food: about " + daysLabel(r.food) + " " + dayWord(r.food);
    var lead = "";
    if (r.days == null) lead = "Answer the water and food questions to see how long your supplies last. ";
    else if (r.water === 0) lead = "You have no stored water, so that is the gap to fix first. ";
    else if (r.water < r.food) lead = "Water runs out first. ";
    else if (r.food < r.water) lead = "Food runs out first. ";
    else lead = "Water and food run out about the same time. ";
    return lead + w + ". " + f + ".";
  }

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
    $$("[data-out=dayword]").forEach(function (e) { e.textContent = r.days == null ? "days of supplies" : r.days === 1 ? "day of supplies" : "days of supplies"; });
    $$("[data-out=limits]").forEach(function (e) { e.textContent = limitsText(r); });
    $$(".tier-chip").forEach(function (e) { e.style.setProperty("--tier", t.color); e.style.color = t.text; e.textContent = t.name; });
    $$("[data-cat-bar]").forEach(function (e) { e.style.width = r.cats[e.dataset.catBar] + "%"; });
    $$("[data-cat-pct]").forEach(function (e) { e.textContent = r.cats[e.dataset.catPct] + "%"; });
    var L = loc();
    $$("[data-out=loc]").forEach(function (e) { e.textContent = L.name; });

    var n = state.people;
    $("#t-water").textContent = (14 * n) + " gal";
    $("#t-food").textContent = (28 * n) + "k kcal";
    $("#t-bags").textContent = (14 * n * 2);

    var bar = $(".mobile-bar");
    if (bar) bar.classList.toggle("empty", !Object.keys(state.a).some(function (k) { return state.a[k]; }));
    renderPlan(r);
    renderCityNote();
    window.__result = r;
    drawCard(r);
    renderPrint(r);
  }

  // ---------- plan ----------
  function esc(t) { return String(t == null ? "" : t).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function catOf(q) { return D.cats.filter(function (c) { return c.id === q.cat; })[0]; }
  function city() { return (state.city && D.cities[state.city]) || null; }
  function act(q) {
    // Partly done (e.g. 3 days of water stored): use the "build on it" wording
    if (q.type === "choice" && state.a[q.id] != null && value(q) > 0 && D.act[q.id + "+"]) return D.act[q.id + "+"];
    return D.act[q.id] || [q.label, null];
  }
  function localWhy(q) {
    var c = catOf(q), C = city();
    if (C && c.guide) {
      var p = C.pri.filter(function (x) { return x[1] === c.guide; })[0];
      if (p) return C.name + ": " + p[0];
    }
    var L = loc(), m = ((L.mult || {})[q.cat] || 1) * ((L.item || {})[q.id] || 1);
    return m >= 1.3 ? "This counts extra where you live (" + L.name.toLowerCase() + ")." : "";
  }
  function alertLinks() {
    var C = city();
    return C ? C.alerts : null;
  }

  // Gaps a free calculator can size for this household (calculators carry no product links)
  var TOOLS = {
    w_store: ["/water-calculator", "Work out your water"], "w_store+": ["/water-calculator", "Work out your water"],
    f_store: ["/food-calculator", "Work out your food"], "f_store+": ["/food-calculator", "Work out your food"],
    p_station: ["/power-calculator", "Size a power station"], p_solar: ["/power-calculator", "Size a power station"]
  };
  function renderPlan(r) {
    var ul = $("#gaps"); ul.innerHTML = "";
    var top = r.gaps.slice(0, 3), rest = r.gaps.slice(3);
    if (!top.length) { ul.innerHTML = "<li><b>No gaps left.</b><span class=\"why\">Now practice the plan with your household, and check your kit twice a year.</span></li>"; }
    top.forEach(function (g) {
      var a = act(g.q), c = catOf(g.q), li = document.createElement("li");
      var html = "<b>" + esc(a[0]) + "</b><span class=\"why\">" + esc(g.q.tip) + "</span>";
      var lw = localWhy(g.q);
      if (lw) html += "<span class=\"local\">" + esc(lw) + "</span>";
      html += a[1] ? "<span class=\"free\"><b>Free option:</b> " + esc(a[1]) + "</span>" : "<span class=\"free\"><b>Costs nothing.</b></span>";
      if (g.q.id === "c_alerts" && alertLinks()) {
        html += "<span class=\"alert-links\">" + alertLinks().map(function (x) { return "<a href=\"" + esc(x[1]) + "\" target=\"_blank\" rel=\"noopener\">" + esc(x[0]) + "</a>"; }).join("") + "</span>";
      }
      var tool = TOOLS[g.q.id];
      if (tool) html += "<a class=\"btn ghost sm tool-link\" href=\"" + tool[0] + "?people=" + state.people + "\">" + tool[1] + " &rarr;</a>";
      if (c.guide) html += " <a class=\"guide-link\" href=\"/guides/" + c.guide + "\">" + esc(c.name) + " guide</a>";
      li.innerHTML = html;
      var buy = D.buy && D.buy[g.q.id];
      if (buy && buy.url && a[1]) {
        var row = document.createElement("div");
        row.className = "gap-buy";
        var btn = document.createElement("a");
        btn.className = "btn sm"; btn.href = buy.url; btn.target = "_blank";
        btn.rel = buy.aff === false ? "noopener" : "sponsored nofollow noopener";
        btn.textContent = buy.aff === false ? "Find one" : "Check price";
        var nm = document.createElement("span");
        nm.textContent = (buy.aff === false ? "" : "Our pick: ") + buy.name;
        row.appendChild(nm); row.appendChild(btn);
        li.appendChild(row);
      }
      ul.appendChild(li);
    });
    var nx = $("#next"), wrap = $("#next-wrap");
    nx.innerHTML = rest.map(function (g) { return "<li>" + esc(act(g.q)[0]) + "</li>"; }).join("");
    wrap.hidden = !rest.length;
  }

  function renderCityNote() {
    var el = $("#city-note"), C = city();
    if (!C) { el.hidden = true; return; }
    el.hidden = false;
    el.innerHTML = "Set up for <b>" + esc(C.name) + ", " + esc(C.state) + "</b>, with local alert links in your plan. Weighted for " +
      esc(loc().name.toLowerCase()) + "; if your home is different, such as an apartment, pick that setting below.";
  }

  function renderPrint(r) {
    var el = $("#plan-print"); if (!el) return;
    var n = state.people, L = loc(), C = city();
    var date = new Date().toLocaleDateString("en-US", { month: "long", day: "numeric", year: "numeric" });
    var top = r.gaps.slice(0, 3), rest = r.gaps.slice(3);
    var acts = top.length ? top.map(function (g) {
      var a = act(g.q), lw = localWhy(g.q);
      return "<li><span class=\"pp-box\"></span><div><b>" + esc(a[0]) + "</b><p>" + esc(g.q.tip) + (lw ? " " + esc(lw) : "") + "</p>" +
        (a[1] ? "<p class=\"pp-free\"><b>Free option:</b> " + esc(a[1]) + "</p>" : "<p class=\"pp-free\"><b>Costs nothing.</b></p>") + "</div></li>";
    }).join("") : "<li><div><b>No gaps left.</b><p>Practice the plan with your household and check your kit twice a year.</p></div></li>";
    var next = rest.map(function (g) { return "<li><span class=\"pp-box\"></span>" + esc(act(g.q)[0]) + "</li>"; }).join("");
    var alerts = C ? C.alerts.map(function (x) { return "<li><span class=\"pp-box\"></span>" + esc(x[0]) + ": " + esc(x[1].replace(/^https?:\/\//, "").replace(/\/$/, "")) + "</li>"; }).join("")
      : "<li><span class=\"pp-box\"></span>Sign up for your county's emergency alerts. Search your county name plus \"emergency alerts\".</li>";
    var where = C ? esc(C.name) + ", " + esc(C.state) + " (" + esc(L.name.toLowerCase()) + ")" : esc(L.name);
    var line = function (label) { return "<div class=\"pp-line\"><span>" + label + "</span><i></i></div>"; };
    el.innerHTML =
      "<header class=\"pp-head\"><div><h1>Our emergency plan</h1><p>" + where + " · " + n + (n === 1 ? " person" : " people") + " · made " + esc(date) + "</p></div>" +
      "<div class=\"pp-score\"><b>" + r.score + "</b><span>PrepScore / 100</span></div></header>" +
      "<p class=\"pp-days\"><b>" + esc(daysLabel(r.days)) + " " + (r.days === 1 ? "day" : "days") + " of supplies.</b> " + esc(limitsText(r)) + "</p>" +
      "<div class=\"pp-cols\"><section><h2>This week</h2><ol class=\"pp-acts\">" + acts + "</ol>" +
      (next ? "<h2>After that</h2><ul class=\"pp-next\">" + next + "</ul>" : "") + "</section>" +
      "<section><h2>Supply targets</h2><table class=\"pp-targets\"><tr><th></th><th>3 days</th><th>2 weeks</th></tr>" +
      "<tr><td>Water</td><td>" + (3 * n) + " gal</td><td>" + (14 * n) + " gal</td></tr>" +
      "<tr><td>Food (adults)</td><td>" + (6 * n) + ",000 cal</td><td>" + (28 * n) + ",000 cal</td></tr>" +
      "<tr><td>Toilet bags</td><td>" + (3 * n * 2) + "</td><td>" + (14 * n * 2) + "</td></tr></table>" +
      "<p class=\"pp-note\">1 gallon of water per person per day, more in heat. Add extra for pets, nursing parents and anyone sick.</p>" +
      "<h2>Local alerts</h2><ul class=\"pp-next\">" + alerts + "</ul>" +
      "<h2>Our household plan</h2>" + line("Meeting spot near home") + line("Meeting spot outside the neighborhood") +
      line("Out-of-area contact and phone") + line("Evacuation zone or route") + line("Where our kit is") + line("Gas, water and power shutoffs") +
      line("Doctor, pharmacy and vet") + "</section></div>" +
      "<footer class=\"pp-foot\">Made with the free PrepScore quiz at " + esc(D.site.host) + "/quiz. General information, not professional advice. In an emergency, follow local officials.</footer>";
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
      x.fillText("OF SUPPLIES", 80 + dw, 298);
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
    return D.site.url + "/score/" + r.tier.slug + "#s" + r.score + (r.days == null ? "" : "-d" + r.days);
  }
  function shareText() {
    var r = window.__result;
    if (r.days == null) return "My PrepScore is " + r.score + "/100: " + r.tier.name + ". How prepared are you?";
    return "I have " + daysLabel(r.days) + " " + dayWord(r.days) + " of water and food stored. PrepScore " + r.score + "/100: " + r.tier.name + ". How long would you last?";
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
    // Printing the quiz page always prints the plan, whether from the button or the browser's Print command.
    $("#btn-print").addEventListener("click", function () { window.print(); });
    window.addEventListener("beforeprint", function () { renderPrint(window.__result); document.body.classList.add("print-plan"); });
    window.addEventListener("afterprint", function () { document.body.classList.remove("print-plan"); });
    wireShare();
  }

  load(); syncInputs(); wire(); render();
})();
