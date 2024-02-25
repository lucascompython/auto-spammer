<script lang="ts">
  import { Handle, Position, type NodeProps } from "@xyflow/svelte";
  import { get, type Writable } from "svelte/store";
  import "@xyflow/svelte/dist/style.css";
  import "./style.css";
  import SettingsIcon from "@assets/SettingsIcon.svelte";
  type $$Props = NodeProps;

  export let data: { title: string; attributes: Writable<string>[] };

  const { title, attributes } = data;

  const attributeValues = attributes.map((attr) => get(attr));
  const attributesString = attributeValues.join("\n");
  console.log(attributesString);
</script>

<div class="base-node">
  <Handle type="target" position={Position.Left} />

  <Handle type="source" position={Position.Right} />
  <div>
    <div class="top-part">
      <p class="title">{data.title}</p>

      <!-- <img class="settings-icon" src="/settings.svg" alt="Settings Icon" /> -->
      <div class="settings-icon">
        <SettingsIcon />
      </div>
    </div>

    <div class="attributes-area-wrapper">
      <textarea
        class="attributes-area"
        disabled
        style="margin-top: 0.5rem"
        rows="2"
        cols="20"
      >
        {attributesString}
      </textarea>
    </div>
  </div>
</div>

<style>
  .base-node {
    padding: 1rem;
    background: #3d3d3d;
    border-radius: 0.125rem;
    font-size: 0.7rem;
    border: 2.5px solid #eee;
  }

  .base-node:hover {
    border-image: var(--accent-gradient);
    border-image-slice: 1;
    border-width: 2px;
    border-style: solid;
  }

  .attributes-area-wrapper {
    width: 97.3%;
  }

  .attributes-area {
    resize: none;
    background: #2c2d2f;
    overflow: hidden;
    width: 100%;
    color: #ffffff;
  }

  .title {
    font-size: 1.5rem;
    color: #ffffff;

    margin: 0;
  }

  .top-part {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .settings-icon {
    margin-left: 5rem;
  }

  .settings-icon:hover {
    cursor: pointer;
  }
</style>
