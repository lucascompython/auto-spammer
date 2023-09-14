import { defineConfig } from "astro/config";
import Compress from "astro-compress";

import svelte from "@astrojs/svelte";

// https://astro.build/config
export default defineConfig({
  compressHTML: import.meta.env.PROD,
  integrations: [
    svelte({
      compilerOptions: {
        dev: !import.meta.env.PROD,
      },
    }),
    Compress(),
  ],
});
