import { defineConfig } from "astro/config";
import compress from "astro-compress";

import svelte from "@astrojs/svelte";

import { loadEnv } from "vite";
const { PROD } = loadEnv(import.meta.env.PROD, process.cwd(), "");

// https://astro.build/config
export default defineConfig({
  compressHTML: PROD,
  integrations: [compress(), svelte()],
});
