<template>
  <div>
    <q-page class="flex column">
      <div>
        <q-tabs
          no-caps
          dense
          align="left"
          narrow-indicator
          class="bg-topbar text-white"
          :v-if="workspaces != undefined"
        >
          <q-route-tab v-for="ws in workspaces" :key="ws.uid" :to="'/ws/' + ws.uid" :label="ws.name" />
          <q-btn class="glossy" round icon="edit" size="sm" v-on:click="edit_activity" />
        </q-tabs>
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
