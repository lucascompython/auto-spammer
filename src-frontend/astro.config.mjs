import { defineConfig } from "astro/config";
import compress from "astro-compress";

import svelte from "@astrojs/svelte";

// https://astro.build/config
export default defineConfig({
  compressHTML: true,
  integrations: [compress(), svelte()]
});