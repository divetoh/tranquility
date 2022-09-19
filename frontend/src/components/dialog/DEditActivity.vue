<template>
  <q-dialog ref="dialogRef">
    <q-card class="column" style="width: 800px; max-width: 80vw; height: 600px; max-height: 80vh">
      <q-card-section>
        <div class="text-bold">Edit activity</div>
      </q-card-section>
      <q-separator />
      <q-card-section class="col row">
        <q-scroll-area class="col-6 scroll">
          <!--   Left list   -->
          Workspace enabled:
          <q-list bordered separator class="q-mr-lg">
            <q-item v-for="(ws, index) in a_workspaces" :key="index" dense active-class="bg-blue-grey-1">
              <q-item-section side>
                <q-btn-group flat>
                  <q-btn
                    dense
                    flat
                    round
                    size="sm"
                    icon="keyboard_arrow_up"
                    @click="move_workspace_up(index)"
                    :disabled="index == 0"
                  />
                  <q-btn
                    dense
                    flat
                    round
                    size="sm"
                    icon="keyboard_arrow_down"
                    @click="move_workspace_up(index + 1)"
                    :disabled="index == a_workspaces.length - 1"
                  />
                  <q-btn dense flat round size="sm" icon="block" @click="disable_workspace(ws)" />
                </q-btn-group>
              </q-item-section>
              <q-item-section>
                {{ workspace[ws].name }}
                <q-popup-edit
                  buttons
                  lazy-rule
                  @save="(val) => rename_workspace(val, ws)"
                  v-slot="scope"
                  :model-value="workspace[ws].name"
                >
                  <q-input v-model="scope.value" dense autofocus counter @keyup.enter="scope.set" />
                </q-popup-edit>
              </q-item-section>
            </q-item>
          </q-list>
          <q-btn-group class="q-mt-md">
            <q-btn
              dense
              size="sm"
              icon="view_column"
              label="Add column workspace"
              color="primary"
              @click="create_workspace('column')"
            />
          </q-btn-group>
        </q-scroll-area>
        <q-scroll-area class="col-6 scroll">
          <!--   Right list   -->
          Workspace avaliable:
          <q-list bordered separator class="q-mr-lg">
            <q-item v-for="(ws, index) in avaliable_workspace" :key="index" dense>
              <q-item-section side>
                <q-btn-group flat>
                  <q-btn dense flat round size="sm" icon="add_circle_outline" @click="enable_workspace(ws)" />
                  <q-btn dense flat round size="sm" icon="delete" @click="delete_workspace(ws)" />
                </q-btn-group>
              </q-item-section>
              <q-item-section>
                {{ workspace[ws].name }}
                <q-popup-edit
                  buttons
                  lazy-rule
                  @save="(val) => rename_workspace(val, ws)"
                  v-slot="scope"
                  :model-value="workspace[ws].name"
                >
                  <q-input v-model="scope.value" dense autofocus counter @keyup.enter="scope.set" />
                </q-popup-edit>
              </q-item-section>
            </q-item>
          </q-list>
        </q-scroll-area>
      </q-card-section>
      <q-separator />
      <q-card-actions align="right">
        <!--   Button area   -->
        <q-btn color="primary" label="Ok" v-close-popup />
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<script>
import { mapState } from "vuex";
import { Dialog } from "quasar";

export default {
  name: "DEditActivity",
  props: ["activity"],
  emits: ["ok", "hide"],
  created: async function () {},
  data: function () {
    return {};
  },
  methods: {
    show() {
      this.$refs.dialogRef.show();
    },
    hide() {
      this.$refs.dialogRef.hide();
    },
    onOKClick() {
      this.$emit("ok");
      this.hide();
    },
    onCancelClick() {
      this.hide();
    },
    async create_workspace(type) {
      const activity = this.$store.state.current.activity;
      const folder = await this.$store.dispatch("aFolderCreate", {
        name: "New workspace",
        foldertype: 1,
        parent: this.$store.state.activity.lst[activity].folder,
      });
      var workspace = await this.$store.dispatch("aWorkspaceCreate", {
        name: "New workspace",
        type: type,
        folder,
      });
      await this.$store.dispatch("aActivityAppendWorkspace", { activity, workspace });
    },
    async disable_workspace(workspace) {
      await this.$store.dispatch("aActivityRemoveWorkspace", {
        activity: this.$store.state.current.activity,
        workspace,
      });
    },
    async enable_workspace(workspace) {
      await this.$store.dispatch("aActivityAppendWorkspace", {
        activity: this.$store.state.current.activity,
        workspace: parseInt(workspace),
      });
    },
    async rename_workspace(name, workspace) {
      await this.$store.dispatch("aWorkspaceSetName", {
        workspace: parseInt(workspace),
        name,
      });
    },
    async delete_workspace(workspace) {
      Dialog.create({
        title: "Confirm delete",
        message: `Would you like to delete workspace ${this.$store.state.workspace.workspace_lst[workspace].name}?`,
        cancel: true,
        persistent: true,
      }).onOk(() => {
        this.$store.dispatch("aWorkspaceDelete", {
          workspace: parseInt(workspace),
        });
      });
    },
    async move_workspace_up(index) {
      await this.$store.dispatch("aActivityMoveWorkspaceUp", {
        activity: this.$store.state.current.activity,
        index,
      });
    },
  },
  computed: mapState({
    a_workspaces(state) {
      return state.activity.lst[this.activity].workspaces;
    },
    workspace(state) {
      return state.workspace.workspace_lst;
    },
    avaliable_workspace(state) {
      var aw = [];
      for (var i in state.workspace.workspace_lst) {
        if (!state.activity.lst[this.activity].workspaces.includes(parseInt(i))) aw.push(i);
      }
      return aw;
    },
  }),
};
</script>
