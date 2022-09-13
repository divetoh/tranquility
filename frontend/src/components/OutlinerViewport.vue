<template>
  <q-card class="full-width full-height text-left q-pa-md">
    <div v-if="loading">Loading... <q-spinner-rings color="grey" size="md" /></div>
    <template v-else>
      <div v-html="markdown_fmt" v-if="fileType == 'markdown'" />
      <WorkspaceColumns :uid="fileUid" v-else-if="fileType == 'workspace'" />
      <div v-else>Unsupported.</div>
    </template>
  </q-card>
</template>

<script>
import { mapState } from "vuex";
import marked from "marked";
import WorkspaceColumns from "@/views/WorkspaceColumns";

export default {
  name: "OutlinerViewport",
  created: async function () {},
  data: function () {
    return {
      fileSource: undefined,
      fileUid: undefined,
      fileType: undefined,
      loading: false,
    };
  },
  components: { WorkspaceColumns },
  computed: mapState({
    markdown_fmt(state) {
      if (state.markdown.markdown_data[this.fileUid]) return marked(state.markdown.markdown_data[this.fileUid].md);
    },
  }),
  methods: {
    async setFile(uid, source, type) {
      this.loading = true;
      this.fileSource = source;
      this.fileUid = uid;
      this.fileType = type;
      if (source == "markdown") await this.showMarkdown();
      else this.loading = false;
    },
    async showMarkdown() {
      if (this.$store.state.markdown.markdown_data[this.fileUid] === undefined) {
        await this.$store.dispatch("aMarkdownLoad", this.fileUid);
      }
      this.loading = false;
    },
  },
};
</script>
