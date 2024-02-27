<script lang="ts">
  import { Handle, Position, type NodeProps } from "@xyflow/svelte";
  import SettingsIcon from "@assets/SettingsIcon.svelte";

  type $$Props = NodeProps;
  export let data: $$Props["data"];
</script>

<div class="wrapper gradient">
  <div class="inner">
    <div class="top-part">
      <div class="title">
        {data.title}
        {#if data.subline}
          <div class="subline">{data.subline}</div>
        {/if}
      </div>

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
    <div class="content">
      <slot />
    </div>
  </div>
  <Handle type="target" position={Position.Left} />
  <Handle type="source" position={Position.Right} />
</div>

<style>
  .top-part {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  .settings-icon {
    margin-left: 5rem;
  }

  .settings-icon button {
    background: none;
    border: none;
    cursor: pointer;
  }
  .subline {
    font-size: 12px;
    color: #777;

    margin-bottom: 0.5rem;
  }

  .content {
    background: #2c2d2f;
    width: 100%;
    min-height: 5rem;
    cursor: default;
  }
</style>
