<template>
  <q-card class="q-mb-sm q-pa-none">
    <q-bar dense class="bg-white hover_ctrl q-pa-none">
      <div class="drag_handler q-space" style="text-align: left; font-weight: bold">
        <span v-if="headerMode == 'custom'">{{ headerCustomText }}</span>
        <span v-if="headerMode == 'markdown'">{{ markdown_name }}</span>
      </div>
      <q-btn dense flat @click="setFolded(true)" icon="unfold_less" size="xs" v-if="!folded">
        <q-tooltip :delay="550" anchor="top middle" self="center middle"> Fold block </q-tooltip>
      </q-btn>
      <q-btn dense flat @click="setFolded(false)" icon="unfold_more" size="xs" v-if="folded">
        <q-tooltip :delay="550" anchor="top middle" self="center middle"> Unfold block </q-tooltip>
      </q-btn>
      <q-btn dense flat @click="edit" icon="edit" size="xs">
        <q-tooltip :delay="550" anchor="top middle" self="center middle"> Edit block </q-tooltip>
      </q-btn>
      <!-- Settings menu-->
      <q-btn dense flat icon="settings">
        <q-tooltip :delay="550" anchor="top middle" self="center middle"> Customize block </q-tooltip>
        <q-menu>
          <div class="column w300 q-pa-md">
            <div>Header:</div>
            <div class="column">
              <q-radio size="sm" dense v-model="headerMode" val="none" label="None" @update:model-value="setHeader" />
              <q-radio
                size="sm"
                dense
                v-model="headerMode"
                val="markdown"
                label="Markdown name"
                @update:model-value="setHeader"
              />
              <q-radio
                size="sm"
                dense
                v-model="headerMode"
                val="custom"
                @update:model-value="setHeader"
                label="Custom"
              />
              <q-input
                dense
                v-model="headerCustomText"
                outlined
                label="Custom header"
                @change="setHeader"
                debounce="2000"
                @keypress.stop
                v-if="headerMode == 'custom'"
              />
            </div>
          </div>
        </q-menu>
      </q-btn>
      <q-btn dense flat @click="delBlock" icon="delete" size="xs" v-if="actions.delblock">
        <q-tooltip :delay="550" anchor="top middle" self="center middle"> Delete block </q-tooltip>
      </q-btn>
    </q-bar>
    <q-card-section class="text-left q-py-sm q-px-md" style="user-select: text" v-if="!folded">
      <q-card-section class="text-center" v-if="markdown === undefined">
        Loading... <q-spinner-rings color="grey" size="md" />
      </q-card-section>
      <div v-html="markdown_fmt" v-else @dblclick="edit" />
    </q-card-section>
    <q-card-section class="text-center q-py-none q-px-none" style="user-select: text" v-else>
      <q-btn dense flat @click="setFolded(false)" icon="more_horiz" size="xs" style="width: 100%" v-if="folded">
        <q-tooltip :delay="550" anchor="top middle" self="center middle"> Unfold block </q-tooltip>
      </q-btn>
    </q-card-section>
  </q-card>
</template>

<script>
import { mapState } from "vuex";
import { Dialog } from "quasar";
import marked from "marked";
import DEditMarkdown from "@/components/dialog/DEditMarkdown";

export default {
  name: "BlockMarkdown",
  emits: ["delBlock", "setHeader", "setFolded"],
  props: ["block", "actions"],
  created: async function () {
    this.headerCustomText = this.block.headerCustomText || "Header";
    this.folded = this.block.folded || false;
    this.headerMode = this.block.headerMode || "none";

    marked.setOptions({
      breaks: true,
    });
    if (this.$store.state.markdown.markdown_data[this.block.uid] === undefined) {
      await this.$store.dispatch("aMarkdownLoad", this.block.uid);
    }
  },
  data: function () {
    return {
      showMoveArrow: false,
      headerCustomText: "",
      headerMode: "",
      folded: false,
    };
  },
  computed: mapState({
    markdown(state) {
      return state.markdown.markdown_data[this.block.uid];
    },
    markdown_name(state) {
      if (state.markdown.markdown_data[this.block.uid]) return state.markdown.markdown_data[this.block.uid].name;
      return "Loading";
    },
    markdown_fmt(state) {
      return marked(state.markdown.markdown_data[this.block.uid].md);
    },
  }),
  methods: {
    async setHeader() {
      this.$emit("setHeader", this.headerMode, this.headerCustomText);
    },
    async setFolded(folded) {
      this.folded = folded;
      this.$emit("setFolded", this.folded);
    },
    async delBlock() {
      this.$q
        .dialog({
          title: "Confirm",
          dark: true,
          message: "Would you like to delete block?",
          options: {
            type: "checkbox",
            model: [],
            items: [{ label: "Delete markdown content.", value: "delmd" }],
          },
          cancel: true,
          persistent: true,
        })
        .onOk((data) => {
          this.$emit("delBlock");
          if (data[0] == "delmd") this.$store.dispatch("aMarkdownDelete", { uid: this.block.uid });
        });
    },
    async edit() {
      Dialog.create({
        component: DEditMarkdown,
        componentProps: {
          uid: this.block.uid,
        },
      });
    },
  },
};
</script>
