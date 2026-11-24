const $ = (selector, root = document) => root.querySelector(selector);
const element = (tag, text) => Object.assign(document.createElement(tag), {textContent: text});
async function api(path, body) {
  const response = await fetch("/api/" + path, body === undefined ? {} : {
    method: "POST", headers: {"Content-Type": "application/json"}, body: JSON.stringify(body)
  });
  const data = await response.json();
  if (!response.ok) throw new Error(typeof data.detail === "string" ? data.detail : "Check the fields and try again.");
  return data;
}
function boot() {
  const toast = $(".boot");
  if (!toast || matchMedia("(prefers-reduced-motion: reduce)").matches) return;
  try { if (sessionStorage.getItem("entered")) return; sessionStorage.setItem("entered","yes"); } catch {}
  toast.hidden = false;
  document.body.classList.add("entering");
  function finish() { toast.hidden = true; document.body.classList.remove("entering"); }
  $("button",toast).onclick = finish;
  ["Connecting to the clouds","Entering my little universe"].forEach((s,i) => setTimeout(() => $("span",toast).textContent = s,550*(i+1)));
  setTimeout(finish,1800);
}
boot();
document.querySelectorAll("[data-picker]").forEach(group => {
  for (const button of group.querySelectorAll("button")) {
    function reveal() {
      group.querySelectorAll("button").forEach(b => b.setAttribute("aria-pressed", String(b === button)));
      $("p",group).textContent = button.dataset.detail;
    }
    button.onclick = button.onfocus = reveal;
  }
});
const dockLinks = Array.from(document.querySelectorAll(".dock a"));
function highlight() {
  let active;
  for (const s of document.querySelectorAll("main section[id]")) {
    if (s.getBoundingClientRect().top <= innerHeight*.55) active = s.id;
  }
  for (const link of dockLinks) {
    if (link.dataset.section === active) link.setAttribute("aria-current","location");
    else link.removeAttribute("aria-current");
  }
}
highlight(); addEventListener("scroll",highlight,{passive:true});
const cursorMedia = matchMedia("(hover:hover) and (pointer:fine) and (prefers-reduced-motion:no-preference)");
document.addEventListener("pointermove",e => {
  const cursor = $(".cursor");
  cursor.style.display = cursorMedia.matches ? "block" : "none";
  cursor.style.transform = "translate(" + (e.clientX+12) + "px," + (e.clientY+13) + "px)";
});
document.documentElement.addEventListener("pointerleave",() => $(".cursor").style.display="none");
const contact = $("#contact-form");
if (contact) contact.onsubmit = async e => {
  e.preventDefault(); const status = $("[role=status]",contact); const submit = $("button",contact);
  submit.disabled = true; status.textContent = "Submitting…";
  try { const data = await api("contact",Object.fromEntries(new FormData(contact))); status.textContent = data.message; contact.reset(); }
  catch (err) { status.textContent = err.message; } finally { submit.disabled = false; }
};
async function github() {
  const root = $("#github-stats"); if (!root) return;
  try {
    const data = await api("github");
    root.replaceChildren();
    const totals = element("div",""); totals.className="stats";
    for (const [label,value] of Object.entries(data.stats)) {
      const stat=element("span","");stat.append(element("strong",value),element("small",label));totals.append(stat);
    }
    root.append(totals);
    for (const [label,value] of [["Featured repositories",data.featured],["Repository languages",data.languages],["Recent public activity",data.activity]]) {
      if (value?.length) root.append(element("h3",label),element("p",value.join(" · ")));
    }
    if (data.calendar) {
      root.append(element("h3",data.calendar.totalContributions+" contributions"));
      const grid=element("div","");grid.className="calendar";grid.setAttribute("aria-label","Contribution calendar");
      for (const w of data.calendar.weeks) {const week=element("div","");week.className="week";
        for(const d of w.contributionDays){const day=element("i","");day.className="day";day.dataset.on=String(d.contributionCount>0);day.title=d.date+" · "+d.contributionCount;week.append(day);}grid.append(week);}
      root.append(grid);
    }
    if(data.note) root.append(element("p",data.note));
  } catch { root.textContent = "GitHub activity is temporarily unavailable."; }
}
if ($("#github-stats")) { const obs=new IntersectionObserver(entries=>{if(entries.some(e=>e.isIntersecting)){obs.disconnect();github();}},{rootMargin:"300px"});obs.observe($("#github-stats")); }
const search = $("#blog-filter");
if(search) search.oninput=()=>{
  const query=search.elements.q.value.toLowerCase();const cat=search.elements.category.value;
  let count=0;document.querySelectorAll("[data-article]").forEach(item=>{
    item.hidden=!(item.dataset.article.includes(query)&&(!cat||item.dataset.category===cat));if(!item.hidden) count++;
  });$("#results").textContent=count+" published "+(count===1?"article":"articles");
};

const atlas = $(".atlas");
if (atlas) {
  atlas.addEventListener("pointermove", event => {
    if (!cursorMedia.matches) return;
    const box = atlas.getBoundingClientRect();
    atlas.style.setProperty("--dx", ((event.clientX-box.left)/box.width-.5)*8+"px");
    atlas.style.setProperty("--dy", ((event.clientY-box.top)/box.height-.5)*6+"px");
  });
  atlas.addEventListener("pointerleave", () => { atlas.style.removeProperty("--dx"); atlas.style.removeProperty("--dy"); });
}
