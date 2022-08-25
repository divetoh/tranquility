<template>
  <div>
    <q-page class="flex column">
      <div
        @dragover="dragover"
        @dragenter="dragenter"
        @dragleave="dragleave"
        @drop="drop"
        @scroll="scroll"
        ref="wrapperRef"
      >
        <q-tabs
          no-caps
          dense
          align="left"
          narrow-indicator
          class="bg-topbar text-white"
          :v-if="workspaces != undefined"
        >
          <q-route-tab
            class="activity_tab"
            v-for="ws in workspaces"
            :key="ws.uid"
            :to="'/ws/' + ws.uid"
            :label="ws.name"
          />
          <q-btn class="glossy" round icon="edit" size="sm" v-on:click="edit_activity" />
        </q-tabs>
        <div class="dropzone" ref="dropzone" />
      </div>
      <div style="flex-grow: 1; position: relative">
        <div v-if="workspace == undefined">&nbsp;</div>
        <WorkspaceColumns :uid="workspace_id" v-else />
      </div>
    </q-page>
  </div>
</template>

<script>
import WorkspaceColumns from "@/views/WorkspaceColumns";
import DEditActivity from "@/components/dialog/DEditActivity";
import { mapState } from "vuex";
import { Dialog } from "quasar";

export default {
  name: "Workspace",
  components: {
    WorkspaceColumns,
  },
  created: async function () {
    this.vars = {
      dropenter_level: 0,
      drop_grid: [],
      col: -1,
    };
    if (this.$route.params.ws_uid == undefined) {
      // Workspace ID don't set in URL
      if (this.$store.state.current.workspace != undefined)
        this.$router.replace({ path: "/ws/" + this.$store.state.current.workspace });
      else if (this.$store.state.activity.lst[this.$store.state.current.activity].workspaces[0] != undefined) {
        await this.$store.dispatch(
          "aCurrentSetWorkspace",
          this.$store.state.activity.lst[this.$store.state.current.activity].workspaces[0]
        );
        this.$router.replace({ path: "/ws/" + this.$store.state.current.workspace });
      }
    } else {
      // Workspace ID set in URL
      if (this.$store.state.current.activity != this.$route.params.ws_uid)
        await this.$store.dispatch("aCurrentSetWorkspace", this.$route.params.ws_uid);
    }
  },
  watch: {
    async $route(to) {
      if (to.name != "ws" && to.path != "/ws/") return;
      if (
        to.params.ws_uid == undefined &&
        this.$store.state.activity.lst[this.$store.state.current.activity].workspaces[0] != undefined
      ) {
        await this.$store.dispatch(
          "aCurrentSetWorkspace",
          this.$store.state.activity.lst[this.$store.state.current.activity].workspaces[0]
        );
        this.$router.replace({ path: "/ws/" + this.$store.state.current.workspace });
      } else await this.$store.dispatch("aCurrentSetWorkspace", to.params.ws_uid);
    },
  },
  methods: {
    // --- Drag'n'drop metods ---
    drop: async function () {
      // Drag'n'drop action complited, object dropped.
      if (this.vars.col != -1) {
        const target = this.workspaces[this.vars.col].uid;
        if (target == this.uid) return;
        if (this.$store.state.workspace.workspace_lst[target] === undefined) {
          await this.$store.dispatch("aWorkspaceLoad", target);
        }
        if (this.$dragState.objectType == "WSBlock") {
          this.$store.dispatch("aCrossWorkspaceBlockMove", {
            workspace: this.$dragState.object.workspace,
            from_row: this.$dragState.object.row,
            from_col: this.$dragState.object.col,
            to_workspace: target,
          });
        } else if (this.$dragState.objectType == "WSColumn" && this.vars.col != -1) {
          this.$store.dispatch("aCrossWorkspaceColumnMove", {
            workspace: this.$dragState.object.workspace,
            from_col: this.$dragState.object.col,
            to_workspace: target,
          });
        }
      }
      this.$_cleanDropstate();
    },
    dragover: function (event) {
      // Dragging object over workspace. If object is acceptable - check for intersection of dropzone.
      if (this.dropenter_level == 0) return;
      if (this.vars.drop_grid.length == 0) return;
      // Checking for intersection of dropzones when dragging Workspace Column.
      var col = -1;
      for (const _col in this.vars.drop_grid) {
        if (
          Math.abs(event.x < this.vars.drop_grid[_col].x) ||
          Math.abs(event.x > this.vars.drop_grid[_col].x + this.vars.drop_grid[_col].w)
        )
          continue;
        col = parseInt(_col);
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
        const x_off = this.vars.drop_grid[col].x + wrap.scrollLeft - wrap.getBoundingClientRect().x;
        const y_off = this.vars.drop_grid[col].y - (wrap.scrollTop + wrap.getBoundingClientRect().y);
        this.$_showDropzone(x_off, y_off, this.vars.drop_grid[col].w, 50);
      }
      event.preventDefault();
    },
    dragenter: function (event) {
      // Dragging enter workspace area. Initialize drag'n'drop state if object acceptable.
      if (this.$dragState.objectType != "WSColumn" && this.$dragState.objectType != "WSBlock") return;
      this.vars.dropenter_level += 1;
      // If dragging just started - calculate dropzones grid
      if (this.vars.dropenter_level == 1) this.$_calcDragGrid();
      event.preventDefault();
    },
    dragleave: function (event) {
      // Dragging leave workspace area
      if (this.$dragState.objectType != "WSColumn" && this.$dragState.objectType != "WSBlock") return;
      this.vars.dropenter_level -= 1;
      // Cursor moved out from component or drag ending.
      if (this.vars.dropenter_level == 0) this.$_cleanDropstate();
      event.preventDefault();
    },
    $_cleanDropstate: function () {
      // Clean dropstate and hide dropzone
      this.$_hideDropzone();
      this.vars.dropenter_level = 0;
      this.vars.drop_grid = [];
      this.vars.col = -1;
    },
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
    $_calcDragGrid: function () {
      // Calculate avaliable dropzones for current workspace and object type
      var i;
      this.vars.drop_grid = [];
      const cols = this.$refs.wrapperRef.getElementsByClassName("activity_tab");
      for (i = 0; i < cols.length; i++) {
        const br = cols[i].getBoundingClientRect();
        this.vars.drop_grid.push({ x: br.x, w: br.width, y: br.y });
      }
    },
    async edit_activity() {
      Dialog.create({
        component: DEditActivity,
        componentProps: {
          activity: this.$store.state.current.activity,
        },
      });
      // TODO: if current workspace deleted redirect to first workspace
    },
  },
  computed: mapState({
    workspace(state) {
      if (state.current.workspace == undefined) return undefined;
      return state.workspace.workspace_lst[state.current.workspace];
    },
    workspace_id(state) {
      return state.current.workspace;
    },
    workspaces(state) {
      if (state.current.activity == undefined) return undefined;
      if (state.activity.lst[state.current.activity] == undefined) return undefined;
      var workspace_lst = [];
      for (var i of state.activity.lst[state.current.activity].workspaces) {
        if (state.workspace.workspace_lst[i] == undefined) return undefined;
        workspace_lst.push({
          uid: i,
          name: state.workspace.workspace_lst[i].name,
        });
      }
      return workspace_lst;
    },
  }),
};
</script>
