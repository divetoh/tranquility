<template>
  <q-card class="q-mb-sm q-pa-none">
    <q-card-section class="text-center" v-if="tasklist === undefined">
      Loading... <q-spinner-rings color="grey" size="md" />
    </q-card-section>
    <template v-else>
      <q-bar dense class="bg-white hover_ctrl q-pa-none">
        <div class="drag_handler q-space" style="text-align: left; font-weight: bold">TaskList</div>
        <q-btn flat dense round color="orange" v-on:click="save" icon="save" size="xs" v-if="tasklist.saved === false">
          <q-tooltip :delay="550" anchor="top middle" self="center middle"> Save list </q-tooltip>
        </q-btn>
        <q-btn dense flat v-on:click="delTasklist" icon="delete" size="xs" v-if="actions.delblock === true">
          <q-tooltip :delay="550" anchor="top middle" self="center middle"> Delete block </q-tooltip>
        </q-btn>
      </q-bar>
      <q-card-section class="text-left q-pt-none q-px-sm q-pb-sm">
        <q-list
          @dragover="dragover"
          @dragenter="dragenter"
          @dragleave="dragleave"
          @drop="drop"
          @scroll="scroll"
          dense
          padding
        >
          <div ref="wrapperRef" class="q-mx-none">
            <TaskListLine
              class="tasklistline"
              draggable="True"
              @mousedown="mousedown"
              @dragstart="dragStart"
              @dragend="dragEnd"
              v-for="(name, index) in tasklist.jsondoc"
              :uid="tluid"
              :index="index"
              :data-row="index"
              :key="index"
              :is_coretasklist="is_coretasklist"
            ></TaskListLine>
            <div class="dropzone" ref="dropzone" />
          </div>
        </q-list>
        <div class="q-gutter-xs">
          <q-btn color="blue" v-on:click="add(1)" size="sm">+1 </q-btn>
          <q-btn color="blue" v-on:click="add(4)" size="sm">+4 </q-btn>
          <q-btn color="blue" v-on:click="add(8)" size="sm">+8 </q-btn>
        </div>
      </q-card-section>
    </template>
  </q-card>
</template>

<script>
import { mapState } from "vuex";
import TaskListLine from "@/components/items/TaskListLine";

export default {
  name: "TaskList",
  props: ["uid", "actions"],
  emits: ["delBlock"],
  data() {
    return {
      tluid: this.uid,
      is_coretasklist: false,
    };
  },
  created: async function () {
    if (this.tluid === undefined) {
      this.is_coretasklist = true;
      this.tluid = this.$store.state.auth.userProfile.coretasklist;
    }
    if (this.$store.state.tasklist.lst[this.tluid] === undefined) {
      await this.$store.dispatch("aTasklistLoad", this.tluid);
    }
    this.vars = {
      handled: false,
      dropenter_level: 0,
      drop_grid: [],
      row: -1,
    };
  },
  components: {
    TaskListLine,
  },
  computed: mapState({
    tasklist: function (state) {
      return state.tasklist.lst[this.tluid];
    },
  }),
  methods: {
    mousedown: function (event) {
      // Is clicked on drag handler?
      this.vars.handled = event.target.classList.contains("tldrag_handler");
    },
    dragStart: function (event) {
      if (this.$dragState.objectType != "") return;
      if (this.vars.handled) {
        this.$dragState.objectType = "TaskListItem";
        this.$dragState.object = {
          tasklist: this.tluid,
          row: parseInt(event.target.dataset.row),
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
    // --- Drag'n'drop metods ---
    drop: function () {
      // Drag'n'drop action complited, object dropped.
      if (this.vars.row != -1) {
        this.$store.dispatch("aTasklistItemMove", {
          from_uid: this.$dragState.object.tasklist,
          from_row: this.$dragState.object.row,
          to_uid: this.tluid,
          to_row: this.vars.row,
        });
      }
      this.$_cleanDropstate();
    },
    dragover: function (event) {
      // Dragging object over workspace. If object is acceptable - check for intersection of dropzone.
      if (this.dropenter_level == 0 || this.vars.drop_grid.length == 0) return;
      // Checking for intersection of dropzones when dragging Workspace Blocks.
      var row = -1;
      if (event.x >= this.vars.drop_grid.x1 && event.x <= this.vars.drop_grid.x2) {
        for (const _row in this.vars.drop_grid.y) {
          if (Math.abs(this.vars.drop_grid.y[_row] - event.y) > 15) continue;
          row = parseInt(_row);
          break;
        }
      }
      if (row == this.vars.row) {
        event.preventDefault();
        return;
      }
      this.vars.row = row;
      // Highlight dropzone
      if (row == -1) this.$_hideDropzone();
      else {
        const wrap = this.$refs["wrapperRef"];
        const x_off = this.vars.drop_grid.x1 + wrap.scrollLeft - wrap.getBoundingClientRect().x;
        const y_off = this.vars.drop_grid.y[row] - (wrap.scrollTop + wrap.getBoundingClientRect().y);
        const width = this.vars.drop_grid.x2 - this.vars.drop_grid.x1;
        this.$_showDropzone(x_off, y_off + 3, width + 20, 6);
      }
      event.preventDefault();
    },
    dragenter: function (event) {
      // Dragging enter workspace area. Initialize drag'n'drop state if object acceptable.
      if (this.$dragState.objectType != "TaskListItem") return;
      this.vars.dropenter_level += 1;
      if (this.vars.dropenter_level == 1) {
        // If dragging just started - calculate dropzones grid
        this.$_calcDragGrid();
      }
      event.preventDefault();
    },
    dragleave: function (event) {
      // Dragging leave workspace area
      if (this.$dragState.objectType != "TaskListItem") return;
      this.vars.dropenter_level -= 1;
      if (this.vars.dropenter_level == 0) {
        // Cursor moved out from component or drag ending.
        this.$_cleanDropstate();
      }
      event.preventDefault();
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
      this.vars.row = -1;
    },
    $_calcDragGrid: function () {
      // Calculate avaliable dropzones for current workspace and object type
      var i;
      this.vars.drop_grid = [];
      const br = this.$refs.wrapperRef.getBoundingClientRect();
      this.vars.drop_grid = { x1: br.x, x2: br.right, y: [br.y] };
      const cols = this.$refs.wrapperRef.getElementsByClassName("tasklistline");
      for (i = 0; i < cols.length; i++) {
        const br = cols[i].getBoundingClientRect();
        this.vars.drop_grid.y.push(br.bottom);
      }
    },
    async add(count) {
      await this.$store.dispatch("aTasklistAddRows", {
        uid: this.tluid,
        count,
      });
    },
    async save() {
      await this.$store.dispatch("aTasklistSave", this.tluid);
    },
    async delTasklist() {
      var dlg = {
        title: "Confirm",
        dark: true,
        message: "Would you like to delete tasklist?",
        cancel: true,
        persistent: true,
      };
      if (!this.is_coretasklist) {
        dlg.options = {
          type: "checkbox",
          model: [],
          items: [{ label: "Delete tasklist content.", value: "deltl" }],
        };
      }
      this.$q.dialog(dlg).onOk((data) => {
        this.$emit("delBlock");
        if (!this.is_coretasklist && data[0] == "deltl") this.$store.dispatch("aTasklistDelete", { uid: this.uid });
      });
    },
  },
};
</script>
