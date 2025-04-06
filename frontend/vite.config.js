import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    host: "0.0.0.0",
    port: 3000,
    watch: {
      usePolling: true, // Ensures changes are detected
    },
    proxy: {
      "/translation-endpoints": {
        target: "http://localhost:5000", // 127.0.0.1 or localhost if running locally
        changeOrigin: true,
        secure: false,
        rewrite: (path) => path.replace(/^\/translation-endpoints/, 'translation-endpoints/api/v1/translate'),
      },
    },
  },
});
