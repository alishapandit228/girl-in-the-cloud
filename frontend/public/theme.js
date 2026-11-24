(() => {
  function apply(mode) {
    const hour = new Date().getHours();
    document.documentElement.dataset.theme = mode === "auto" ? (hour >= 6 && hour < 18 ? "day" : "night") : mode;
  }
  let mode = "auto";
  try { mode = localStorage.getItem("theme") || mode; } catch {}
  apply(mode);
  document.addEventListener("DOMContentLoaded", () => {
    const select = document.querySelector("#theme");
    select.value = mode;
    select.onchange = () => {
      mode = select.value;
      try { localStorage.setItem("theme", mode); } catch {}
      apply(mode);
    };
  });
  setInterval(() => apply(mode), 60000);
})();
