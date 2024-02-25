<script lang="ts">
  import { writable } from "svelte/store";
  import {
    SvelteFlow,
    Controls,
    Background,
    BackgroundVariant,
    MiniMap,
  } from "@xyflow/svelte";

  import TypeNode from "./ColorPickerNode.svelte";

  // 👇 this is important! You need to./ColorPicker.sveltes for Svelte Flow to work
  import "@xyflow/svelte/dist/style.css";

  // We are using writables for the nodes and edges to sync them easily. When a user drags a node for example, Svelte Flow updates its position.
  const nodes = writable([
    {
      id: "1",
      type: "input",
      data: { label: "Input Node" },
      position: { x: 0, y: 0 },
    },
    {
      id: "2",
      type: "default",
      data: { label: "Node" },
      position: { x: 0, y: 150 },
    },

    {
      id: "3",
      type: "colorPicker",
      data: { color: writable("#ff4000") },
      position: { x: 0, y: 300 },
    },
  ]);

  // same for edges
  const edges = writable([
    {
      id: "1-2",
      type: "default",
      source: "1",
      target: "2",
      label: "Edge Text",
    },
  ]);

  const nodeTypes = {
    colorPicker: TypeNode,
  };

  const snapGrid = [25, 25] as [number, number];
</script>

<!--
👇 By default, the Svelte Flow container has a height of 100%.
This means that the parent container needs a height to render the flow.
-->
<div class="flow">
  <SvelteFlow
    {nodes}
    {edges}
    {snapGrid}
    {nodeTypes}
    fitView
    proOptions={{ hideAttribution: true }}
    on:nodeclick={(event) => console.log("on node click", event.detail.node)}
  >
    <Background
      variant={BackgroundVariant.Lines}
      bgColor="#242424"
      patternColor="#484848"
      gap={25}
    />
    <MiniMap />
  </SvelteFlow>
</div>

<style>
  .flow {
    top: 0;
    left: 0;
    height: 100vh;
    width: 100%;
    position: absolute;
    /* takes fullscreen */
  }
</style>
