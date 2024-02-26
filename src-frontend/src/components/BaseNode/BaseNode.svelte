<script lang="ts">
  import { Handle, Position, type NodeProps } from "@xyflow/svelte";
  import { get, type Writable } from "svelte/store";
  import "@xyflow/svelte/dist/style.css";
  import "./style.css";
  import SettingsIcon from "@assets/SettingsIcon.svelte";
  type $$Props = NodeProps;

  export let data: { title: string; attributes: Writable<string>[] };

  const attributeValues = data.attributes.map((attr) => get(attr));
  const attributesString = attributeValues.join("\n");
</script>

<div class="base-node">
  <Handle type="target" position={Position.Left} />
  <Handle type="source" position={Position.Right} />

  <div class="top-part">
    <p class="title">{data.title}</p>

    <div class="settings-icon">
      <button
        on:click={(e) => {
          console.log("ola");
          console.log("ola2");
        }}
      >
        <SettingsIcon />
      </button>
    </div>
  </div>

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

<style>
  /* .base-node {
    padding: 1rem;
    background: #3d3d3d;
    border-radius: 0.125rem;
    font-size: 0.7rem;
    border: 2.5px solid #eee;
    border-radius: 0.5rem;
    transition: border-color 0.3s ease;
  }

  .base-node:hover {
    border-color: var(--accent);
    transition: border-color 0.3s ease;
  } */

  /* TODO: See the why this is blurrying things on certai environments */
  .base-node {
    position: relative;
    padding: 1rem;
    background: #3d3d3d;
    border-radius: 0.5rem;
    font-size: 0.7rem;
  }

  .base-node:before {
    content: "";
    position: absolute;
    top: -2px;
    right: -2px;
    bottom: -2px;
    left: -2px;
    background: var(--accent-gradient);
    border-radius: 0.5rem;
    z-index: -1;
    transition: opacity 0.3s ease;
    opacity: 0;
  }

  .base-node:hover:before {
    opacity: 1;
  }

  .attributes-area {
    resize: none;
    background: #2c2d2f;
    overflow: hidden;
    width: 97.3%;
    color: #ffffff;
    border: none;
    white-space: pre-line;
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

  .settings-icon:hover button {
    cursor: pointer;
  }

  .settings-icon button {
    background: none;
    border: none;
  }
</style>
