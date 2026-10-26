import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    // same-origin in dev: session cookie + CSRF work without extra CORS setup
    proxy: { "/api": "http://localhost:8000" },
  },
});
