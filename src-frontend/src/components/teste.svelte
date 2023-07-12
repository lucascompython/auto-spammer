<script lang="ts">
  import { register } from "@tauri-apps/api/globalShortcut";
  import { invoke } from "@tauri-apps/api/tauri";
  register("F6", () => {
    invoke("type_string", { string: "Hello World" });
  });
</script>
