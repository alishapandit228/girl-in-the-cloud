import "@fontsource/cormorant-garamond/latin-500.css";
import "@fontsource/cormorant-garamond/latin-500-italic.css";
import "@fontsource/cormorant-garamond/latin-600.css";
import "@fontsource/inter/latin-400.css";
import "@fontsource/inter/latin-600.css";

const scene = document.querySelector<HTMLElement>("#scene");
if (scene && window.matchMedia("(min-width: 760px) and (prefers-reduced-motion:no-preference)").matches) {
  const observer = new IntersectionObserver(entries => {
    if (!entries.some(entry => entry.isIntersecting)) return;
    observer.disconnect();
    const probe = document.createElement("canvas").getContext("webgl2");
    if (!probe) return;
    probe.getExtension("WEBGL_lose_context")?.loseContext();
    import("./workspace").then(({mount}) => mount(scene)).catch(() => {});
  });
  observer.observe(scene);
}

const viewer = document.querySelector<HTMLElement>("#atlas-viewer");
const toggle = document.querySelector<HTMLButtonElement>("#atlas-toggle");
const desktop = window.matchMedia("(min-width:760px) and (prefers-reduced-motion:no-preference)");
if (viewer && toggle && desktop.matches) {
  let stop: (()=>void)|undefined;
  function close(){
    stop?.();
    stop=undefined;
    viewer!.hidden=true;
    toggle!.textContent="Explore in 3D";
    toggle!.setAttribute("aria-pressed","false");
    viewer!.parentElement?.classList.remove("exploring");
  }
  toggle.hidden=false;
  toggle.onclick=async()=>{
    if (stop) {close();return;}
    toggle.disabled=true;
    try {
      const canvas=document.createElement("canvas");
      const probe=canvas.getContext("webgl2");
      if(!probe){toggle.hidden=true;return;}
      probe.getExtension("WEBGL_lose_context")?.loseContext();
      const {mountAtlas}=await import("./atlas");
      if(!desktop.matches)return;
      viewer.hidden=false;
      viewer.parentElement?.classList.add("exploring");
      stop=mountAtlas(viewer);
      toggle.textContent="Show illustration";
      toggle.setAttribute("aria-pressed","true");
    } catch {close();toggle.hidden=true;}
    finally {toggle.disabled=false;}
  };
  desktop.addEventListener("change",()=>{if(!desktop.matches)close();toggle.hidden=!desktop.matches;});
  const visibility=new IntersectionObserver(entries=>{if(stop&&!entries.some(e=>e.isIntersecting))close();});
  visibility.observe(toggle.parentElement!);
}
