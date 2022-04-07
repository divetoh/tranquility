<template>
  <div>
    <BlockMarkdown
      v-if="block.type == 'markdown'"
      :uid="block.uid"
      :actions="actions"
      @moveBlock="moveBlock"
      @delBlock="delBlock"
    />
    <TaskList v-if="block.type == 'coretasklist'" :actions="actions" @moveBlock="moveBlock" @delBlock="delBlock" />
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
  methods: {
    moveBlock: async function (direction) {
      this.$store.dispatch("aWorkspaceBlockMove", {
        workspace: this.workspace,
        row: this.row,
        col: this.col,
        direction,
      });
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
    actions(state) {
      const ws = state.workspace.workspace_lst[this.workspace].workspace;
      return {
        moveleft: this.col > 0,
        moveright: this.col < ws.content.length - 1,
        moveup: this.row > 0,
        movedown: this.row < ws.content[this.col].content.length - 1,
        delblock: true,
      };
    },
  }),
};
</script>
