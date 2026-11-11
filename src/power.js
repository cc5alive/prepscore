(function () {
  "use strict";
  // Power station size calculator. Assumptions are shown on the page:
  // usable energy = rated Wh x 0.85 (inverter losses through the AC outlets), plus 20% headroom.
  var KEY = "prepscore.power.v1";
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var data = JSON.parse($("#pc-data").textContent);
  var DEV = data.devices; // [id, name, hint, run, per, unit, use, qty, surge]
  var st = {};
  DEV.forEach(function (d) { st[d[0]] = { q: d[7], u: d[6] }; });
  st.custom = { q: 0, u: 1, w: 0 };
  try {
    var saved = JSON.parse(localStorage.getItem(KEY) || "null");
    if (saved) Object.keys(saved).forEach(function (k) { if (st[k]) st[k] = Object.assign(st[k], saved[k]); });
  } catch (e) {}
  function save() { try { localStorage.setItem(KEY, JSON.stringify(st)); } catch (e) {} }
  function fmt(n, d) { return Number(n).toLocaleString("en-US", { maximumFractionDigits: d || 0 }); }
  function up(n, step) { return Math.ceil(n / step) * step; }
  function wh(n) { return n >= 1000 ? fmt(n / 1000, n >= 10000 ? 0 : 1) + " kWh" : fmt(n) + " Wh"; }

  function sizeClass(w) {
    if (w <= 120) return ["One or two power banks", "A couple of 20,000 mAh power banks cover this. No station needed.", "$ to $$"];
    if (w <= 320) return ["Small power station, about 300 Wh", "Or a few power banks if you only need USB.", "$$$"];
    if (w <= 650) return ["Small power station, about 500 Wh", "Easy to carry; enough for phones, lights and a CPAP.", "$$$"];
    if (w <= 1300) return ["Mid-size power station, about 1,000 Wh", "The most common size for apartments and CPAP users.", "$$$$"];
    if (w <= 2600) return ["Large power station, about 2,000 Wh", "Or a 1,000 Wh station plus a solar panel.", "$$$$"];
    if (w <= 6000) return ["Expandable home battery, 2 to 6 kWh", "Or a smaller station recharged by solar each day.", "$$$$"];
    return ["Bigger than portable batteries", "Look at a generator (outdoors only) or a home battery with solar.", "$$$$"];
  }

  function totals() {
    var daily = 0, run = 0, surgeExtra = 0, cpap = false, fridge = false;
    DEV.forEach(function (d) {
      var s = st[d[0]];
      if (!s.q) return;
      var use = d[5] === "night" || d[5] === "day" ? 1 : s.u;
      daily += s.q * d[4] * use;
      run += s.q * d[3];
      if (d[8]) surgeExtra = Math.max(surgeExtra, d[8] - d[3]);
      if (d[0] === "cpap" || d[0] === "cpaph") cpap = true;
      if (d[0] === "fridge" || d[0] === "freezer") fridge = true;
    });
    var c = st.custom;
    if (c.q && c.w) { daily += c.q * c.w * c.u; run += c.q * c.w; }
    return { daily: daily, run: run, surge: run + surgeExtra, cpap: cpap, fridge: fridge };
  }

  function render() {
    var t = totals();
    $("#pc-daily").textContent = wh(t.daily);
    $("#pc-run").textContent = fmt(t.run) + " W";
    var buy1 = t.daily ? up(t.daily / 0.85 * 1.2, 50) : 0;
    var c1 = sizeClass(buy1);
    var head = $("#pc-class");
    if (!t.daily) {
      head.innerHTML = "<b>Add a device to start.</b>";
    } else {
      head.innerHTML = "<span class=\"pc-k\">To cover one day without recharging</span><b>" + c1[0] + "</b><span>" + c1[1] +
        " Buy at least <strong>" + fmt(buy1) + " Wh</strong>. Typical cost: <span class=\"pc-band\">" + c1[2] + "</span></span>";
    }
    var rows = "";
    [[1, "1 day"], [3, "3 days"], [7, "1 week"]].forEach(function (h) {
      var b = t.daily ? up(t.daily * h[0] / 0.85 * 1.2, 50) : 0;
      rows += "<tr><th scope=\"row\">" + h[1] + "</th><td>" + (b ? fmt(b) + " Wh" : "—") + "</td><td>" + (b ? sizeClass(b)[0] : "—") + "</td></tr>";
    });
    $("#pc-rows").innerHTML = rows;
    var out = up(Math.max(t.run * 1.2, 1), 50), surge = up(Math.max(t.surge * 1.1, out), 50);
    var o = t.run ? "Look for at least <b>" + fmt(out) + " W</b> continuous output" + (t.surge > t.run ? " and <b>" + fmt(surge) + " W</b> surge, for motors starting up" : "") + "." : "";
    if (t.run > 3600) o += " That's more than most portable stations deliver at once. Run big loads one at a time, or look at a generator or a home battery with a transfer switch.";
    else if (t.run > 1800) o += " Many 1,000 Wh stations top out around 1,500 to 2,000 W, so check the spec sheet.";
    $("#pc-out").innerHTML = o;
    var notes = [];
    if (t.daily) notes.push("On a clear day, a 200 W folding solar panel puts back roughly 400 to 700 Wh, " +
      (t.daily <= 450 ? "enough to cover what you use in a day." : "about " + fmt(550 / t.daily * 100) + "% of what you use in a day."));
    if (t.fridge) notes.push("Fridges and freezers don't need to run nonstop: keep the doors shut and run them a couple of hours at a time to stretch the battery.");
    if (t.cpap) notes.push("Turning off the CPAP humidifier and heated tube cuts its power use by about 4 to 5 times. <a href=\"/guides/cpap-power-outage\">CPAP runtime table and tips</a>.");
    $("#pc-notes").innerHTML = notes.map(function (n) { return "<li>" + n + "</li>"; }).join("");
    $("#pc-sticky-txt").textContent = t.daily ? wh(t.daily) + " a day · buy " + fmt(buy1) + "+ Wh" : "Add a device to start";
    save();
  }

  function num(el, max) { var v = parseFloat(el.value); return isFinite(v) && v >= 0 ? Math.min(v, max) : 0; }
  document.querySelectorAll(".pc-dev").forEach(function (row) {
    var id = row.getAttribute("data-id"), s = st[id];
    var out = $("output", row), use = $("input.pc-use-in", row), watts = $("input.pc-w-in", row);
    function sync() {
      out.textContent = s.q;
      row.classList.toggle("on", s.q > 0);
      if (use) use.value = s.u;
      if (watts) watts.value = s.w || "";
    }
    $("[data-dir='-1']", row).addEventListener("click", function () { s.q = Math.max(0, s.q - 1); sync(); render(); });
    $("[data-dir='1']", row).addEventListener("click", function () { s.q = Math.min(20, s.q + 1); sync(); render(); });
    if (use) use.addEventListener("input", function () { s.u = num(use, 24); render(); });
    if (watts) watts.addEventListener("input", function () { s.w = num(watts, 5000); if (s.w && !s.q) { s.q = 1; out.textContent = 1; row.classList.add("on"); } render(); });
    sync();
  });
  $("#pc-reset").addEventListener("click", function () {
    DEV.forEach(function (d) { st[d[0]].q = 0; st[d[0]].u = d[6]; });
    st.custom = { q: 0, u: 1, w: 0 };
    document.querySelectorAll(".pc-dev").forEach(function (row) {
      var id = row.getAttribute("data-id"), s = st[id];
      $("output", row).textContent = s.q; row.classList.remove("on");
      var u = $("input.pc-use-in", row); if (u) u.value = s.u;
      var w = $("input.pc-w-in", row); if (w) w.value = "";
    });
    render();
  });
  // Phone: a compact summary bar until the results come into view
  var bar = $("#pc-sticky"), res = $(".pc-out");
  if (bar && res && "IntersectionObserver" in window) {
    new IntersectionObserver(function (es) { bar.classList.toggle("hide", es[0].isIntersecting || es[0].boundingClientRect.top < 0); }).observe(res);
  }
  render();
})();
