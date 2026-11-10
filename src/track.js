(function () {
  "use strict";
  // Anonymous count of clicks on retailer links: page, product and button only. No cookies, nothing about you.
  function send(e) {
    var a = e.target && e.target.closest ? e.target.closest('a[href*="amazon.com/"]') : null;
    if (!a || !navigator.sendBeacon) return;
    var u; try { u = new URL(a.href); } catch (x) { return; }
    var m = u.pathname.match(/\/dp\/([A-Z0-9]{10})/);
    var box = a.closest("[id]");
    var data = {
      p: location.pathname,
      t: u.searchParams.get("tag") || "",
      a: m ? m[1] : (u.searchParams.get("k") ? "search" : ""),
      l: (a.textContent || "").replace(/\s+/g, " ").trim().slice(0, 60),
      s: box ? box.id : ""
    };
    try { navigator.sendBeacon("/api/click", new Blob([JSON.stringify(data)], { type: "application/json" })); } catch (x) {}
  }
  document.addEventListener("click", send, true);
  document.addEventListener("auxclick", send, true);
})();
