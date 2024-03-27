<script lang="ts">
  import BaseNode, {
    type BaseNodeProps,
  } from "@components/BaseNode/BaseNode.svelte";

  type $$Props = BaseNodeProps & {
    data: {
      text: string;
      delay: number;
      cancelKey?: string;
    };
  };

  // #region Unused props that are here just for not having the "unknown prop" warning

  export let id: $$Props["id"];
  id;
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

  // #endregion

  export let data: $$Props["data"] = {
    text: "Type something",
    delay: 69,
    title: "Type Node",
    subline: "Subline",
    cancelKey: "",
  };
</script>

<BaseNode
  {id}
  data={{
    title: data.title,
    subline: data.subline,
  }}
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
  <div class="input-container">
    <div class="label">Text:</div>
    <span class="nodrag" contenteditable="true" bind:innerText={data.text}
    ></span>
  </div>

  <div class="input-container">
    <div class="label">Delay(s):</div>
    <span
      class="nodrag"
      contenteditable="true"
      role="textbox"
      tabindex="0"
      on:keypress={(e) => {
        if (e.key === ".") {
          // @ts-ignore
          if (e.target.innerText.includes(".")) {
            e.preventDefault();
            return false;
          }
          return true;
        } else if (isNaN(parseFloat(e.key))) {
          e.preventDefault();
          return false;
        }

        return true;
      }}
      on:input={(e) => {
        // @ts-ignore
        data.delay = parseFloat(e.target.innerText);
      }}>{data.delay}</span
    >
  </div>

  <div class="input-container">
    <div class="label">Cancel key:</div>
    <span
      class="nodrag"
      class:optional-placeholder={data.cancelKey === ""}
      contenteditable="true"
      role="textbox"
      bind:textContent={data.cancelKey}
    ></span>
  </div></BaseNode
>

<style>
  .input-container {
    display: flex;
    align-items: center;
    margin-left: 0.5rem;
  }

  .input-container span {
    background: none;
    outline: none;
    border: none;
    color: white;
    cursor: text;

    border-radius: 0.25rem;
    background: #4c4d4f;
    min-width: 5rem;
    max-width: 160px;
    margin-left: 1rem;
    margin-top: 0.25rem;

    border: 1px solid transparent;
    transition: border 0.2s ease;

    font-size: 0.9rem;
    font-weight: 400;

    &:focus {
      border: 1px solid #e92a67;
    }
  }

  .input-container span[tabindex="0"] {
    max-width: 120px;
  }

  .optional-placeholder::before {
    content: "Optional";
    color: rgb(160, 154, 154);
  }
</style>
