(function () {
  "use strict";
  // Anonymous counts, no cookies, nothing about you:
  // 1. clicks on retailer links (page, product and button);
  // 2. use of the free tools (someone used the quiz or a calculator, printed, shared a score, or followed a tool link).
  function beacon(path, data) {
    if (!navigator.sendBeacon) return;
    try { navigator.sendBeacon(path, new Blob([JSON.stringify(data)], { type: "application/json" })); } catch (x) {}
  }

  function retailer(e) {
    var a = e.target && e.target.closest ? e.target.closest('a[href*="amazon.com/"]') : null;
    if (!a) return;
    var u; try { u = new URL(a.href); } catch (x) { return; }
    var m = u.pathname.match(/\/dp\/([A-Z0-9]{10})/);
    var box = a.closest("[id]");
    beacon("/api/click", {
      p: location.pathname,
      t: u.searchParams.get("tag") || "",
      a: m ? m[1] : (u.searchParams.get("k") ? "search" : ""),
      l: (a.textContent || "").replace(/\s+/g, " ").trim().slice(0, 60),
      s: box ? box.id : ""
    });
  }
  document.addEventListener("click", retailer, true);
  document.addEventListener("auxclick", retailer, true);

  // Tool events: each counted at most once per page view (tool links each time).
  var sent = {};
  function ev(name, detail, once) {
    if (once && sent[name]) return;
    sent[name] = true;
    beacon("/api/event", { p: location.pathname, n: name, d: detail || "" });
  }
  var TOOL_FORM = "[data-q], .wc-in, .pc-list";
  function used(e) {
    var t = e.target;
    if (t && t.closest && t.closest(TOOL_FORM)) ev("use", "", true);
  }
  document.addEventListener("change", used, true);
  document.addEventListener("input", used, true);
  document.addEventListener("click", function (e) {
    var t = e.target && e.target.closest ? e.target : null;
    if (!t) return;
    if (t.closest(".wc-in button, .pc-list button, #people-minus, #people-plus, [data-loc]")) ev("use", "", true);
    var s = t.closest("#btn-share, #btn-save, #btn-copy, #s-x, #s-fb, #s-reddit, #s-wa");
    if (s) ev("share", s.id.replace(/^(btn|s)-/, ""), false);
    var tl = t.closest("a.tool-link, a.kit-tool");
    if (tl) { try { ev("tool", new URL(tl.href).pathname.slice(1), false); } catch (x) {} }
  }, true);
  window.addEventListener("beforeprint", function () { ev("print", "", true); });
})();
