import {defineConfig} from "vite";
export default defineConfig({
  base:"/enhanced/",publicDir:false,
  build:{outDir:"public/enhanced",rollupOptions:{input:"src/index.tsx",output:{entryFileNames:"scene.js",assetFileNames:asset=>asset.name?.endsWith(".css")?"fonts.css":"assets/[name]-[hash][extname]"}}},
  test:{environment:"jsdom"}
});
