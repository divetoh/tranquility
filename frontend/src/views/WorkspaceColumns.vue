<template>
  <div class="ws_wrap scroll6">
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
          <BlockWrapper
            v-for="(block, row) in column.content"
            :block="block"
            :key="block.uid"
            :workspace="uid"
            :row="row"
            :col="index"
            :v-if="false"
          />
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
  },
  methods: {
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
