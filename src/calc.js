(function () {
  "use strict";
  // Water storage calculator. Assumptions are shown on the page:
  // 1 gal per person per day (CDC, Ready.gov), doubled in very hot weather (Ready.gov),
  // pets ~1 oz per lb per day, 8.34 lb per gallon, stacked 5-gal containers ~0.1 sq ft per gallon.
  var KEY = "prepscore.water.v1";
  var $ = function (s) { return document.querySelector(s); };
  var st = { people: 2, petlb: 0, hot: false, have: 0, heater: false };
  try { var s = JSON.parse(localStorage.getItem(KEY) || "null"); if (s) st = Object.assign(st, s); } catch (e) {}
  function save() { try { localStorage.setItem(KEY, JSON.stringify(st)); } catch (e) {} }
  function fmt(n, d) { return Number(n).toLocaleString("en-US", { maximumFractionDigits: d || 0 }); }

  function sync() {
    $("#wc-people").textContent = st.people;
    $("#wc-petlb").value = st.petlb || "";
    $("#wc-hot").checked = st.hot;
    $("#wc-have").value = st.have || "";
    $("#wc-heater").checked = st.heater;
  }
  function render() {
    var perDay = st.people * (st.hot ? 2 : 1) + (st.petlb || 0) / 128;
    var have = (st.have || 0) + (st.heater ? 40 : 0);
    $("#wc-daily").textContent = fmt(perDay, 1) + " gal";
    var days = perDay > 0 ? Math.floor(have / perDay) : 0;
    $("#wc-lasts").textContent = have <= 0 ? "0 days" : (days >= 90 ? "90+ days" : days + (days === 1 ? " day" : " days"));
    $("#wc-lasts-note").textContent = have <= 0 ? "You have no stored water yet. Start with the 3-day amount." :
      days >= 14 ? "You've reached the two-week target. Keep it fresh: replace water you bottled yourself every six months." :
      days >= 3 ? "Past the 3-day minimum. Two weeks is the next target." : "Short of the 3-day minimum. That's the first goal.";
    var rows = "";
    [[3, "3 days"], [7, "1 week"], [14, "2 weeks"]].forEach(function (h) {
      var need = Math.ceil(perDay * h[0]);
      var gap = Math.max(0, need - have);
      var jugs = Math.ceil(gap / 5);
      rows += "<tr><th scope=\"row\">" + h[1] + "</th><td>" + fmt(need) + " gal</td><td>" + (gap ? fmt(gap) + " gal" : "Done") + "</td>" +
        "<td>" + (gap ? jugs + (jugs === 1 ? " container" : " containers") : "—") + "</td>" +
        "<td>" + (gap ? fmt(gap * 8.34) + " lb" : "—") + "</td><td>" + (gap ? "~" + fmt(Math.max(1, gap * 0.1), 0) + " sq ft" : "—") + "</td></tr>";
    });
    $("#wc-rows").innerHTML = rows;
    var two = Math.ceil(perDay * 14);
    $("#wc-weight").textContent = fmt(two * 8.34) + " lb";
    save();
  }
  function num(el) { var v = parseFloat(el.value); return isFinite(v) && v > 0 ? Math.min(v, 100000) : 0; }
  $("#wc-minus").addEventListener("click", function () { st.people = Math.max(1, st.people - 1); sync(); render(); });
  $("#wc-plus").addEventListener("click", function () { st.people = Math.min(20, st.people + 1); sync(); render(); });
  $("#wc-petlb").addEventListener("input", function (e) { st.petlb = num(e.target); render(); });
  $("#wc-have").addEventListener("input", function (e) { st.have = num(e.target); render(); });
  $("#wc-hot").addEventListener("change", function (e) { st.hot = e.target.checked; render(); });
  $("#wc-heater").addEventListener("change", function (e) { st.heater = e.target.checked; render(); });
  sync(); render();
})();
