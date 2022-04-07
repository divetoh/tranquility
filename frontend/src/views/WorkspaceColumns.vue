<template>
  <div>
    <div class="row fit no-wrap items-start content-start">
      <div
        class="col-xs-10 col-sm-6 col-md-3 q-pa-md"
        v-for="(column, index) in workspace.workspace.content"
        :key="column.type"
      >
        <q-bar class="bg-transparent hover_ctrl" dense>
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
      <!-- Column right button block -->
      <div class="col-1 q-ma-md">
        <q-btn class="bg-white" round icon="add" size="sm" v-on:click="addCol" />
      </div>
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
