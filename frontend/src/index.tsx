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
