(function () {
  "use strict";
  var $$ = function (s) { return Array.prototype.slice.call(document.querySelectorAll(s)); };

  // Scenario picker
  var chips = $$(".chip[data-scn]");
  function pick(id) {
    chips.forEach(function (c) { c.setAttribute("aria-pressed", String(c.dataset.scn === id)); });
    $$(".scn-panel").forEach(function (p) { p.hidden = p.dataset.panel !== id; });
    $$(".matrix [data-col]").forEach(function (c) { c.classList.toggle("col-on", c.dataset.col === id); });
  }
  chips.forEach(function (c) { c.addEventListener("click", function () { pick(c.dataset.scn); }); });
  var h = (location.hash || "").replace("#", "");
  if (h && chips.some(function (c) { return c.dataset.scn === h; })) pick(h);

  // Go-bag checklist
  var boxes = $$("[data-ck]");
  if (boxes.length) {
    var KEY = "prepscore.gobag.v1", saved = {};
    try { saved = JSON.parse(localStorage.getItem(KEY) || "{}") || {}; } catch (e) {}
    var count = document.getElementById("ck-count");
    function upd() {
      var n = boxes.filter(function (b) { return b.checked; }).length;
      if (count) count.textContent = n + " of " + boxes.length + " packed";
    }
    boxes.forEach(function (b) {
      b.checked = !!saved[b.id];
      b.addEventListener("change", function () {
        saved[b.id] = b.checked;
        try { localStorage.setItem(KEY, JSON.stringify(saved)); } catch (e) {}
        upd();
      });
    });
    upd();
  }
})();

(function () {
  "use strict";
  // City picker: jump straight to the chosen city guide.
  Array.prototype.forEach.call(document.querySelectorAll("[data-city-pick]"), function (f) {
    var sel = f.querySelector("select");
    function go(ev) {
      if (sel && sel.value) { if (ev) ev.preventDefault(); location.href = sel.value; }
    }
    f.addEventListener("submit", go);
    if (sel) sel.addEventListener("change", function () { go(); });
  });
  // Print buttons (go-bag checklist).
  Array.prototype.forEach.call(document.querySelectorAll("[data-print]"), function (b) {
    b.addEventListener("click", function () { document.body.classList.add("print-checklist"); window.print(); });
  });
  window.addEventListener("afterprint", function () { document.body.classList.remove("print-checklist"); });
})();
