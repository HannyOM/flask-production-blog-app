import { defineConfig } from "vite";
import { resolve } from "path";

export default defineConfig({
  build: {
    outDir: "bloggr/static",
    emptyOutDir: false,
    lib: {
      entry: resolve(__dirname, "bloggr/static/js/editor.js"),
      name: "Editor",
      fileName: "editor",
      formats: ["iife"],
    },
    rollupOptions: {
      input: {
        editor: resolve(__dirname, "bloggr/static/js/editor.js"),
      },
    },
  },
  resolve: {
    alias: {
      "@": resolve(__dirname, "bloggr"),
    },
  },
});
