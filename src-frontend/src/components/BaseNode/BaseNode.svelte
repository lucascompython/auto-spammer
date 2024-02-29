<script lang="ts">
  import {
    Handle,
    Position,
    type NodeProps,
    useConnection,
  } from "@xyflow/svelte";
  import SettingsIcon from "@assets/SettingsIcon.svelte";

  type $$Props = NodeProps;
  export let data: $$Props["data"];

  export let id: $$Props["id"];

  const connection = useConnection();

  let isConnecting = false;
  let isTarget = false;

  $: isConnecting = !!$connection.startHandle?.nodeId;
  $: isTarget =
    !!$connection.startHandle &&
    $connection.startHandle?.nodeId !== id &&
    $connection.startHandle?.type === "source";

  console.log(connection);
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
  <Handle
    style="border-color: {isTarget ? '#e92a67' : ''}"
    type="target"
    position={Position.Left}
  />
  <Handle
    style="border-color: {isConnecting && !isTarget ? '#2a8af6' : ''}"
    type="source"
    position={Position.Right}
  />
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
    border-radius: 0.25rem;
  }
</style>
