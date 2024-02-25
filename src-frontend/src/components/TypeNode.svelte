<script lang="ts">
  import { Handle, Position, type NodeProps } from "@xyflow/svelte";
  import type { Writable } from "svelte/store";

  type $$Props = NodeProps;

  export let data: { color: Writable<string> };

  const { color } = data;
</script>
