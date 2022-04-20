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
        <q-bar
          class="bg-transparent hover_ctrl draggable ws_col_header"
          style="display: block; margin: 0px 0px 14px"
          dense
        >
          <q-chip
            square
            text-color="white"
            class="bg-topbar q-pa-xs q-mb-md drag_handler"
            style="width: 100%"
            @dragstart="dragColumnStart"
            @dragend="dragColumnEnd"
            draggable="True"
            :data-col="index"
          >
            <q-space />
            <div style="cursor: pointer">
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
              <q-btn dense flat v-on:click="deleteColumn(index)" icon="delete">
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
            <q-btn icon="article" size="sm" v-on:click="createBlockMarkdown(index)" />
            <q-btn icon="more_horiz" size="sm" v-on:click="createBlockDialog(index)" />
          </q-btn-group>
        </div>
      </div>
    </div>
    <!-- Right button block -->
    <div class="ws_col_container">
      <q-btn class="bg-white" round icon="add" size="sm" v-on:click="addColumn" />
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
      dropenter_level: 0,
      drop_grid: [],
      col: -1,
      row: -1,
    };
  },
  methods: {
    // --- Column header drag ---
    dragColumnStart: function (event) {
      this.$dragState.objectType = "WSColumn";
      this.$dragState.object = {
        workspace: this.uid,
        col: parseInt(event.target.dataset.col),
      };
      event.target.parentElement.parentElement.style.opacity = 0.5;
    },
    dragColumnEnd: function (event) {
      this.$dragState.objectType = "";
      this.$dragState.object = {};
      event.target.parentElement.parentElement.style.opacity = "";
    },

    // --- Drag'n'drop metods ---
    drop: function () {
      // Drag'n'drop action complited, object dropped.
      if (this.$dragState.objectType == "WSBlock" && this.vars.row != -1) {
        this.$store.dispatch("aWorkspaceBlockMove", {
          workspace: this.uid,
          from_row: this.$dragState.object.row,
          from_col: this.$dragState.object.col,
          to_row: this.vars.row,
          to_col: this.vars.col,
        });
      } else if (this.$dragState.objectType == "WSColumn" && this.vars.col != -1) {
        this.$store.dispatch("aWorkspaceColumnMove", {
          workspace: this.uid,
          from_col: this.$dragState.object.col,
          to_col: this.vars.col,
        });
      }
      this.$_cleanDropstate();
    },
    dragover: function (event) {
      // Dragging object over workspace. If object is acceptable - check for intersection of dropzone.
      if (this.dropenter_level == 0) return;
      if (this.vars.drop_grid.length == 0) return;
      if (this.$dragState.objectType == "WSBlock") this.dragoverBlock(event);
      else if (this.$dragState.objectType == "WSColumn") this.dragoverColumn(event);
    },
    dragoverBlock: function (event) {
      // Checking for intersection of dropzones when dragging Workspace Blocks.
      var row = -1;
      var col = -1;
      for (const _col in this.vars.drop_grid) {
        if (event.x < this.vars.drop_grid[_col].x1 || event.x > this.vars.drop_grid[_col].x2) continue;
        col = parseInt(_col);
        for (const _row in this.vars.drop_grid[col].y) {
          if (Math.abs(this.vars.drop_grid[col].y[_row] - event.y) > 30) continue;
          row = parseInt(_row);
          // Disable dragging object to it's old location
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
      this.vars.col = col;
      this.vars.row = row;

      // Highlight dropzone
      if (row == -1) this.$_hideDropzone();
      else {
        const wrap = this.$refs["wrapperRef"];
        const x_off = this.vars.drop_grid[col].x1 + wrap.scrollLeft + wrap.getBoundingClientRect().x;
        const y_off = this.vars.drop_grid[col].y[row] - (wrap.scrollTop + wrap.getBoundingClientRect().y);
        const width = this.vars.drop_grid[col].x2 - this.vars.drop_grid[col].x1;
        this.$_showDropzone(x_off - 5, y_off - 30, width + 10, 60);
      }
      event.preventDefault();
    },
    dragoverColumn: function (event) {
      // Checking for intersection of dropzones when dragging Workspace Column.
      var col = -1;
      for (const _col in this.vars.drop_grid) {
        if (Math.abs(event.x - this.vars.drop_grid[_col].x) > 60) continue;
        if (Math.abs(event.y - this.vars.drop_grid[_col].y) > 60) break;
        col = parseInt(_col);
        // Disable dragging object to it's old location
        if (col == this.$dragState.object.col || col == this.$dragState.object.col + 1) col = -1;
        break;
      }
      if (col == this.vars.col) {
        event.preventDefault();
        return;
      }
      this.vars.col = col;
      // Highlight dropzone
      if (col == -1) this.$_hideDropzone();
      else {
        const wrap = this.$refs["wrapperRef"];
        const x_off = this.vars.drop_grid[col].x + wrap.scrollLeft + wrap.getBoundingClientRect().x;
        const y_off = this.vars.drop_grid[col].y - (wrap.scrollTop + wrap.getBoundingClientRect().y);
        this.$_showDropzone(x_off - 30, y_off - 20, 60, 100);
      }
      event.preventDefault();
    },
    dragenter: function () {
      // Dragging enter workspace area. Initialize drag'n'drop state if object acceptable.
      if (this.$dragState.objectType != "WSColumn" && this.$dragState.objectType != "WSBlock") return;
      this.vars.dropenter_level += 1;
      if (this.vars.dropenter_level != 1) return;
      // If dragging just started - calculate dropzones grid
      this.$_calcDragGrid();
    },
    dragleave: function () {
      // Dragging leave workspace area
      if (this.$dragState.objectType != "WSColumn" && this.$dragState.objectType != "WSBlock") return;
      this.vars.dropenter_level -= 1;
      if (this.vars.dropenter_level > 0) return;
      // Cursor moved out from component or drag ending.
      this.$_cleanDropstate();
    },
    scroll: function () {
      // Recalculate dropzones grid if workspace scrolled
      if (this.vars.dropenter_level > 0) this.$_calcDragGrid();
    },

    // --- Internal functions for drag'n'drop ---
    $_hideDropzone: function () {
      // Hide dropzone highlight
      this.$refs["dropzone"].style.display = "none";
    },
    $_showDropzone: function (x, y, w, h) {
      // Show dropzone highlight
      this.$refs["dropzone"].style.display = "block";
      this.$refs["dropzone"].style.left = x + "px";
      this.$refs["dropzone"].style.width = w + "px";
      this.$refs["dropzone"].style.top = y + "px";
      this.$refs["dropzone"].style.height = h + "px";
    },
    $_cleanDropstate: function () {
      // Clean dropstate and hide dropzone
      this.$_hideDropzone();
      this.vars.dropenter_level = 0;
      this.vars.drop_grid = [];
      this.vars.col = -1;
      this.vars.row = -1;
    },
    $_calcDragGrid: function () {
      // Calculate avaliable dropzones for current workspace and object type
      var i, col;
      this.vars.drop_grid = [];
      if (this.$dragState.objectType == "WSBlock") {
        // Calculate drop zones for Workspace Block
        const cols = this.$refs.wrapperRef.getElementsByClassName("ws_col_content");
        for (i = 0; i < cols.length; i++) {
          const br = cols[i].getBoundingClientRect();
          col = { x1: br.x, x2: br.right, y: [br.y] };
          var blocks = cols[i].getElementsByClassName("block_wrapper");
          for (var j = 0; j < blocks.length; j++) {
            const br2 = blocks[j].getBoundingClientRect();
            col.y.push(br2.bottom + 4);
          }
          this.vars.drop_grid.push(col);
        }
      } else if (this.$dragState.objectType == "WSColumn") {
        // Calculate drop zones for Workspace Column
        const cols = this.$refs.wrapperRef.getElementsByClassName("ws_col_header");
        for (i = 0; i < cols.length; i++) {
          const br = cols[i].getBoundingClientRect();
          this.vars.drop_grid.push({ x: br.x - 14, y: br.y + br.height / 2 });
          if (i == cols.length - 1) this.vars.drop_grid.push({ x: br.right + 14, y: br.y + br.height / 2 });
        }
      }
    },

    // --- Action metods ---
    createBlockMarkdown: async function (column) {
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
            this.createBlockMarkdown(column);
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
    addColumn: async function () {
      await this.$store.dispatch("aWorkspaceColumnAdd", {
        workspace: this.uid,
      });
    },
    deleteColumn: async function (index) {
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
</style>
