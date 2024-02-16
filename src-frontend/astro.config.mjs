import { defineConfig } from "astro/config";

// https://astro.build/config
export default defineConfig({
  integrations: [(await import("astro-compress")).default()],
  output: "server",
});
