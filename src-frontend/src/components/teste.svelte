<script lang="ts">
  import { register } from "@tauri-apps/api/globalShortcut";
  import { invoke } from "@tauri-apps/api/tauri";
  register("F6", async () => {
    invoke("type_string", { string: "Hello World" });
  });
</script>
