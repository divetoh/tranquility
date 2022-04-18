<template>
  <q-card class="q-mb-sm q-pa-none">
    <q-bar dense class="bg-white hover_ctrl q-pa-none">
      <q-space class="drag_handler" />
      <q-btn dense flat v-on:click="edit" icon="edit" size="xs">
        <q-tooltip :delay="550" anchor="top middle" self="center middle"> Edit block </q-tooltip>
      </q-btn>
      <q-btn dense flat v-on:click="delBlock" icon="delete" size="xs" v-if="actions.delblock">
        <q-tooltip :delay="550" anchor="top middle" self="center middle"> Delete block </q-tooltip>
      </q-btn>
    </q-bar>
    <q-card-section class="text-left q-pa-sm" style="user-select: text">
      <q-card-section class="text-center" v-if="markdown === undefined">
        Loading... <q-spinner-rings color="grey" size="md" />
      </q-card-section>
      <div v-html="markdown_fmt" v-else />
    </q-card-section>
  </q-card>
</template>

<script>
import { mapState } from "vuex";
import marked from "marked";
import { Dialog } from "quasar";
import DEditMarkdown from "@/components/dialog/DEditMarkdown";

export default {
  name: "BlockMarkdown",
  emits: ["delBlock"],
  props: ["uid", "actions"],
  created: async function () {
    marked.setOptions({
      breaks: true,
    });
    if (this.$store.state.markdown.markdown_data[this.uid] === undefined) {
      await this.$store.dispatch("aMarkdownLoad", this.uid);
    }
  },
  data: function () {
    return {
      showMoveArrow: false,
    };
  },
  computed: mapState({
    markdown(state) {
      return state.markdown.markdown_data[this.$props.uid];
    },
    markdown_fmt(state) {
      return marked(state.markdown.markdown_data[this.$props.uid].md);
    },
  }),
  methods: {
    async delBlock() {
      this.$q
        .dialog({
          title: "Confirm",
          message: "Would you like to delete block?",
          options: {
            type: "checkbox",
            model: [],
            // inline: true
            items: [{ label: "Delete markdown content.", value: "delmd" }],
          },
          cancel: true,
          persistent: true,
        })
        .onOk((data) => {
          this.$emit("delBlock");
          if (data[0] == "delmd") this.$store.dispatch("aMarkdownDelete", { uid: this.uid });
        });
    },
    async edit() {
      Dialog.create({
        component: DEditMarkdown,
        componentProps: {
          uid: this.$props.uid,
        },
      });
    },
  },
};
</script>
