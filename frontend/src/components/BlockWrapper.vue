<template>
  <div
    class="draggable block_wrapper"
    draggable="True"
    @mousedown="mousedown"
    @dragstart="dragStart"
    @dragend="dragEnd"
    ref="wrapperRef"
  >
    <BlockMarkdown v-if="block.type == 'markdown'" :uid="block.uid" :actions="actions" @delBlock="delBlock" />
    <TaskList v-if="block.type == 'coretasklist'" :actions="actions" @delBlock="delBlock" />
  </div>
</template>

<script>
import BlockMarkdown from "@/components/BlockMarkdown";
import TaskList from "@/components/TaskList";
import { mapState } from "vuex";

export default {
  name: "BlockWrapper",
  props: ["workspace", "block", "row", "col"],
  components: {
    BlockMarkdown,
    TaskList,
  },
  created: async function () {
    this.vars = {
      handled: false,
    };
  },
  methods: {
    mousedown: function (event) {
      // Is clicked on drag handler?
      this.vars.handled = event.target.classList.contains("drag_handler");
    },
    dragStart: function (event) {
      if (this.vars.handled) {
        this.$dragState.objectType = "WSBlock";
        this.$dragState.object = {
          workspace: this.workspace,
          block: this.block.uid,
          row: this.row,
          col: this.col,
        };
        event.target.style.opacity = 0.5;
      } else {
        event.preventDefault();
        return false;
      }
    },
    dragEnd: function (event) {
      this.$dragState.objectType = "";
      this.$dragState.object = {};
      event.target.style.opacity = "";
    },
    delBlock: async function () {
      this.$store.dispatch("aWorkspaceBlockDelete", {
        workspace: this.workspace,
        row: this.row,
        col: this.col,
      });
    },
  },
  computed: mapState({
    actions() {
      return {
        delblock: true,
      };
    },
  }),
};
</script>
