<script lang="ts">
  import { type NodeProps } from "@xyflow/svelte";
  import BaseNode from "@components/BaseNode/BaseNode.svelte";

  type $$Props = NodeProps;
  export let id: $$Props["id"];
  id;
  // export let data: $$Props["data"];
  // data;
  export let dragHandle: $$Props["dragHandle"] = undefined;
  dragHandle;
  export let type: $$Props["type"] = undefined;
  type;
  export let selected: $$Props["selected"] = undefined;
  selected;
  export let isConnectable: $$Props["isConnectable"];
  isConnectable;
  export let zIndex: $$Props["zIndex"];
  zIndex;
  export let width: $$Props["width"] = undefined;
  width;
  export let height: $$Props["height"] = undefined;
  height;
  export let dragging: $$Props["dragging"];
  dragging;
  export let targetPosition: $$Props["targetPosition"] = undefined;
  targetPosition;
  export let sourcePosition: $$Props["sourcePosition"] = undefined;
  sourcePosition;
  export let positionAbsoluteX: $$Props["positionAbsoluteX"];
  positionAbsoluteX;
  export let positionAbsoluteY: $$Props["positionAbsoluteY"];
  positionAbsoluteY;

  export let data: $$Props["data"] = {
    text: "Type something",
    delay: 0,
  };

  // export let data: {
  //   text: string;
  //   delay: number;
  //   cancelKey?: string;
  // };
</script>

<BaseNode
  {id}
  {data}
  {dragHandle}
  {type}
  {selected}
  {isConnectable}
  {zIndex}
  {width}
  {height}
  {dragging}
  {targetPosition}
  {sourcePosition}
  {positionAbsoluteX}
  {positionAbsoluteY}
>
  <!-- <label>
    Text:
    <input type="text" bind:value={data.text} />
  </label> -->

  <span role="textbox" contenteditable>Test</span>
  <span class="input" role="textbox" contenteditable> 99 </span>

  <label>
    Delay:
    <input
      type="number"
      bind:value={data.delay}
      on:keyup={(e) => {
        // TODO: Fix this
        if (
          (e.key < "0" || e.key > "9") &&
          e.key !== "Backspace" &&
          e.key !== "Delete" &&
          e.key !== "."
        ) {
          e.preventDefault();
        }
      }}
    />
  </label>
</BaseNode>

<style>
  input {
    background: none;
    outline: none;
    border: none;
    color: white;

    border-radius: 0.25rem;
    background: #4c4d4f;
    min-width: 3rem;
    max-width: 160px;
    margin-left: 1rem;

    border: 1px solid transparent;
    transition: border 0.2s ease;

    &:focus {
      border: 1px solid #e92a67;
    }
  }

  input::-webkit-outer-spin-button,
  input::-webkit-inner-spin-button {
    -webkit-appearance: none;
    margin: 0;
  }
  input[type="number"] {
    -moz-appearance: textfield;
    appearance: textfield;
  }

  label {
    display: flex;
    align-items: center;
    color: url(--accent-gradient);
    margin-left: 0.5rem;
  }

  span {
    /* make it editable */
    cursor: text !important;
    display: inline-block !important;
    padding: 0.5rem !important;
    border-radius: 0.25rem !important;
    background: #4c4d4f !important;
    color: white !important;
    margin: 0.5rem !important;
    -webkit-nbsp-mode: normal !important;
    white-space: pre-wrap !important;
    writing-mode: horizontal-tb !important;
    -webkit-user-select: text !important;
    user-select: text !important;

    display: inline-block;
    -webkit-rtl-ordering: logical;
  }
</style>
