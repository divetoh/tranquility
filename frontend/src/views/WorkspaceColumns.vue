<template>
  <div
    class="ws_wrap scroll6"
    @dragover="dragover"
    @dragenter="dragenter"
    @dragleave="dragleave"
    @drop="drop"
    @scroll="scroll"
    ref="wrapperRef"
  >
    <div class="ws_col_container w400" v-for="(column, index) in workspace.workspace.content" :key="column.type">
      <div class="ws_col_wrap">
        <!-- Column header -->
        <q-bar class="bg-transparent hover_ctrl" style="display: block; margin: 0px 0px 14px" dense>
          <q-chip square text-color="white" class="bg-topbar q-pa-xs q-mb-md" style="width: 100%">
            <q-btn-group outline class="hover_block">
              <q-btn dense flat v-on:click="moveColLeft(index)" icon="keyboard_arrow_left" :disabled="index == 0">
                <q-tooltip :delay="550" anchor="top middle" self="center middle"> Move Column Left </q-tooltip>
              </q-btn>
              <q-btn
                dense
                flat
                v-on:click="moveColLeft(index + 1)"
                icon="keyboard_arrow_right"
                :disabled="index == workspace.workspace.content.length - 1"
              >
                <q-tooltip :delay="550" anchor="top middle" self="center middle"> Move Column Right </q-tooltip>
              </q-btn>
            </q-btn-group>
            <q-space />
            <div>
              &nbsp;{{ column.name }}&nbsp;
              <q-popup-edit
                buttons
                lazy-rule
                @save="(val) => setColumnName(val, index)"
                v-slot="scope"
                v-model="column.name"
              >
                <q-input v-model="scope.value" dense autofocus counter @keyup.enter="scope.set" />
              </q-popup-edit>
            </div>
            <q-space />
            <q-btn-group outline class="hover_block">
              <q-btn dense flat v-on:click="delCol(index)" icon="delete">
                <q-tooltip :delay="550" anchor="top middle" self="center middle"> Delete column </q-tooltip>
              </q-btn>
            </q-btn-group>
          </q-chip>
        </q-bar>
        <!-- Column content -->
        <div class="ws_col_content scroll6">
          <template v-for="(block, row) in column.content" :key="block.uid">
            <BlockWrapper :block="block" :workspace="uid" :row="row" :col="index" />
          </template>
          <!-- Column footer button block -->
          <q-btn-group rounded class="bg-white">
            <q-btn icon="article" size="sm" v-on:click="createBlockMD(index)" />
            <q-btn icon="more_horiz" size="sm" v-on:click="createBlockDialog(index)" />
          </q-btn-group>
        </div>
      </div>
    </div>
    <!-- Right button block -->
    <div class="ws_col_container">
      <q-btn class="bg-white" round icon="add" size="sm" v-on:click="addCol" />
    </div>
    <div class="dropzone" ref="dropzone" />
  </div>
</template>

<script>
import BlockWrapper from "@/components/BlockWrapper";
import { mapState } from "vuex";
import { Dialog } from "quasar";
import DSelectWorkspaceBlock from "@/components/dialog/DSelectWorkspaceBlock";
export default {
  name: "WorkspaceColumns",
  props: ["uid"],
  components: {
    BlockWrapper,
  },
  created: async function () {
    if (this.$store.state.workspace.workspace_lst[this.uid] === undefined) {
      await this.$store.dispatch("aWorkspaceLoad", this.uid);
    }
    this.vars = {
      dragEnterLevel: 0,
      dragLines: [],
      col: -1,
      row: -1,
    };
  },
  methods: {
    // --- Dragging metods ---
    drop: function () {
      if (this.vars.row != -1) {
        this.$store.dispatch("aWorkspaceBlockMove", {
          workspace: this.uid,
          from_row: this.$dragState.object.row,
          from_col: this.$dragState.object.col,
          to_row: this.vars.row,
          to_col: this.vars.col,
        });
      }
      // Reset dragging variables
      this.$refs["dropzone"].style.display = "none";
      this.vars.dragLines = [];
      this.vars.col = -1;
      this.vars.row = -1;
      this.vars.dragEnterLevel = 0;
    },
    dragover: function (event) {
      if (this.dragEnterLevel == 0) return;
      if (this.vars.dragLines.length == 0) return;
      // Сheck the possibility of transfer
      var row = -1;
      var col = -1;
      for (const _col in this.vars.dragLines) {
        if (event.x < this.vars.dragLines[_col].x1 || event.x > this.vars.dragLines[_col].x2) continue;
        col = parseInt(_col);
        for (const _row in this.vars.dragLines[col].y) {
          if (Math.abs(this.vars.dragLines[col].y[_row] - event.y) > 30) continue;
          row = parseInt(_row);
          if (
            col == this.$dragState.object.col &&
            (row == this.$dragState.object.row || row == this.$dragState.object.row + 1)
          )
            row = -1;
          break;
        }
        break;
      }
      if (col == this.vars.col && row == this.vars.row) {
        event.preventDefault();
        return;
      }
      // Highlight dropzone
      const dz = this.$refs["dropzone"].style;
      const wrap = this.$refs["wrapperRef"];
      const x_off = wrap.scrollLeft + wrap.getBoundingClientRect().x;
      const y_off = wrap.scrollTop + wrap.getBoundingClientRect().y;

      this.vars.col = col;
      this.vars.row = row;
      if (row == -1) {
        dz.display = "none";
      } else {
        dz.display = "block";
        dz.left = this.vars.dragLines[col].x1 + x_off - 5 + "px";
        dz.width = this.vars.dragLines[col].x2 - this.vars.dragLines[col].x1 + 10 + "px";
        dz.top = this.vars.dragLines[col].y[row] - 30 - y_off + "px";
        dz.height = "60px";
      }
      event.preventDefault();
    },
    dragleave: function () {
      this.vars.dragEnterLevel -= 1;
      if (this.vars.dragEnterLevel > 0) return;
      // Cursor moved out from component or drag ending.
      this.$refs["dropzone"].style.display = "none";
      this.vars.dragLines = [];
      this.vars.col = -1;
      this.vars.row = -1;
    },
    dragenter: function () {
      this.vars.dragEnterLevel += 1;
      if (this.vars.dragEnterLevel != 1) return;
      // Store avaliable drag positions in this.vars.dragLines
      this.calc_drag_grid();
    },
    calc_drag_grid: function () {
      this.vars.dragLines = [];
      const cols = this.$refs.wrapperRef.getElementsByClassName("ws_col_content");
      for (var i = 0; i < cols.length; i++) {
        const br = cols[i].getBoundingClientRect();
        var col = { x1: br.x, x2: br.right, y: [br.y] };
        var blocks = cols[i].getElementsByClassName("block_wrapper");
        for (var j = 0; j < blocks.length; j++) {
          const br2 = blocks[j].getBoundingClientRect();
          col.y.push(br2.bottom + 4);
        }
        this.vars.dragLines.push(col);
      }
    },
    scroll: function () {
      if (this.vars.dragEnterLevel > 0) this.calc_drag_grid();
    },
    // --- Action metods ---
    createBlockMD: async function (column) {
      var markdown = await this.$store.dispatch("aMarkdownCreate", {
        name: "Workspace block",
        md: "New block.",
      });
      await this.$store.dispatch("aWorkspaceColumnAppendMarkdown", {
        workspace: this.uid,
        column,
        markdown,
      });
    },
    createBlockDialog: async function (column) {
      Dialog.create({
        component: DSelectWorkspaceBlock,
        componentProps: {
          uid: this.$props.uid,
        },
      }).onOk((data) => {
        switch (data) {
          case "markdown":
            this.createBlockMD(column);
            break;
          case "coretasklist":
            this.$store.dispatch("aWorkspaceColumnAppendBlock", {
              workspace: this.uid,
              column,
              param: { type: "coretasklist" },
            });
            break;
        }
      });
    },
    addCol: async function () {
      await this.$store.dispatch("aWorkspaceColumnAdd", {
        workspace: this.uid,
      });
    },
    moveColLeft: async function (index) {
      await this.$store.dispatch("aWorkspaceColumnMoveLeft", {
        workspace: this.uid,
        index,
      });
    },
    delCol: async function (index) {
      this.$q
        .dialog({
          title: "Confirm",
          message: "Would you like to delete workspace column?",
          cancel: true,
          persistent: true,
        })
        .onOk(() => {
          this.$store.dispatch("aWorkspaceColumnDelete", {
            workspace: this.uid,
            index,
          });
        });
    },
    async setColumnName(name, index) {
      await this.$store.dispatch("aWorkspaceSetColumnName", { workspace: this.uid, name, index });
    },
  },
  computed: mapState({
    workspace(state) {
      return state.workspace.workspace_lst[this.uid];
    },
  }),
};
</script>

<style scoped>
.ws_wrap {
  position: absolute;
  top: 0;
  bottom: 0;
  left: 0;
  right: 0;
  display: block;
  overflow-x: auto;
  overflow-y: hidden;
  white-space: nowrap;
  padding: 5px 0px 0px 200px;
  margin-left: -200px;
  text-align: left;
}

.ws_wrap::-webkit-scrollbar-track {
  margin-left: 206px;
}

.ws_col_container {
  display: inline-block;
  height: 100%;
  margin: 0px;
  padding: 5px 14px 0px 14px;
  box-sizing: border-box;
  text-align: center;
}

.ws_col_wrap {
  display: flex;
  flex-direction: column;
  max-height: 100%;
  box-sizing: border-box;
}

.ws_col_content {
  flex-grow: 1;
  flex-shrink: 1;
  display: block;
  overflow-x: hidden;
  overflow-y: auto;
  padding: 0px 2px 5px 2px;
}

.w400 {
  width: 400px;
}
</style>
