(function () {
  "use strict";
  // Food storage calculator. Planning figures are shown on the page:
  // 2,000 kcal per adult (2,500 if active), 1,400 per child under 12; example pantry split by share of calories.
  var KEY = "prepscore.food.v1";
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var data = JSON.parse($("#fc-data").textContent);
  var K = data.kcal, P = data.pantry; // [id, name, unit, kcal, shareNoCook, shareStove, note]
  var st = { adults: 2, kids: 0, active: false, stove: false, goal: 14 };
  try { var s = JSON.parse(localStorage.getItem(KEY) || "null"); if (s) st = Object.assign(st, s); } catch (e) {}
  function save() { try { localStorage.setItem(KEY, JSON.stringify(st)); } catch (e) {} }
  function fmt(n) { return Math.round(n).toLocaleString("en-US"); }
  var GOALS = [[3, "3 days"], [14, "2 weeks"], [30, "1 month"]];

  function sync() {
    $("#fc-adults").textContent = st.adults;
    $("#fc-kids").textContent = st.kids;
    $("#fc-active").checked = st.active;
    $("#fc-stove").checked = st.stove;
    document.querySelectorAll("[data-goal]").forEach(function (b) { b.setAttribute("aria-pressed", String(+b.getAttribute("data-goal") === st.goal)); });
  }
  function render() {
    var daily = st.adults * (st.active ? K.adult_active : K.adult) + st.kids * K.child;
    $("#fc-daily").textContent = fmt(daily);
    var rows = "";
    GOALS.forEach(function (g) {
      var tot = daily * g[0];
      rows += "<tr" + (g[0] === st.goal ? " class=\"sel\"" : "") + "><th scope=\"row\">" + g[1] + "</th><td>" + fmt(tot) + "</td><td>" +
        (tot ? Math.ceil(tot / 3600) + (Math.ceil(tot / 3600) === 1 ? " pack" : " packs") : "—") + "</td></tr>";
    });
    $("#fc-rows").innerHTML = rows;
    var goalLabel = GOALS.filter(function (g) { return g[0] === st.goal; })[0][1];
    var total = daily * st.goal;
    $("#fc-total").textContent = fmt(total);
    $("#fc-goal-l").textContent = goalLabel;
    var list = "";
    P.forEach(function (p) {
      var share = st.stove ? p[5] : p[4];
      if (!share || !total) return;
      var n = Math.ceil(total * share / p[3]);
      list += "<li><span class=\"fc-n\">" + n + "</span><span class=\"fc-what\"><b>" + p[1] + "</b><span>" + n + " × " + p[2] + ", about " + fmt(p[3]) + " calories each" +
        (p[6] ? ". " + p[6] : "") + "</span></span></li>";
    });
    $("#fc-list").innerHTML = list || "<li>Add someone to your household to see a list.</li>";
    $("#fc-stove-note").hidden = !st.stove;
    save();
  }
  $("#fc-adults-minus").addEventListener("click", function () { st.adults = Math.max(0, st.adults - 1); sync(); render(); });
  $("#fc-adults-plus").addEventListener("click", function () { st.adults = Math.min(20, st.adults + 1); sync(); render(); });
  $("#fc-kids-minus").addEventListener("click", function () { st.kids = Math.max(0, st.kids - 1); sync(); render(); });
  $("#fc-kids-plus").addEventListener("click", function () { st.kids = Math.min(20, st.kids + 1); sync(); render(); });
  $("#fc-active").addEventListener("change", function (e) { st.active = e.target.checked; render(); });
  $("#fc-stove").addEventListener("change", function (e) { st.stove = e.target.checked; render(); });
  document.querySelectorAll("[data-goal]").forEach(function (b) {
    b.addEventListener("click", function () { st.goal = +b.getAttribute("data-goal"); sync(); render(); });
  });
  sync(); render();
})();
