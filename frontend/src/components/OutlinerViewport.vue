<template>
  <q-card class="full-width full-height text-left q-pa-none column">
    <q-bar style="background-color: rgb(245, 245, 245)">
      <template v-if="fileType == 'markdown'">
        <q-btn-group class="bg-grey-5" flat dense>
          <q-btn icon="edit_note" flat dense :color="mode == 'edit' ? 'primary' : 'gray-10'" @click="setMode('edit')" />
          <q-btn
            icon="vertical_split"
            flat
            dense
            :color="mode == 'both' ? 'primary' : 'gray-10'"
            @click="setMode('both')"
          />
          <q-btn icon="preview" flat dense :color="mode == 'view' ? 'primary' : 'gray-10'" @click="setMode('view')" />
        </q-btn-group>
        <q-btn icon="info" dense class="bg-grey-5" color="gray-10" flat @click="showMarkdownSyntax" />
      </template>
      <q-space />
      <q-btn class="bg-primary" color="white" no-caps flat label="Save" @click="saveFile" v-if="showSaveBtn" />
    </q-bar>
    <q-separator />
    <q-card-section class="col row edit-viewport">
      <div v-if="loading">Loading... <q-spinner-rings color="grey" size="md" /></div>
      <template v-else-if="fileSource == 'markdown'">
        <textarea
          class="input col-grow"
          :value="md"
          @input="update"
          v-if="mode == 'edit' || mode == 'both'"
          style="resize: none"
        ></textarea>
        <div class="output q-pl-lg" v-html="markdown_fmt" v-if="mode == 'view' || mode == 'both'"></div>
      </template>
      <template v-else-if="fileSource == 'jsondoc'">
        <div class="output q-pl-lg col-grow">
          <pre style="max-width: 100%; word-wrap: break-word; white-space: pre-wrap">{{ jsondoc }}</pre>
        </div>
      </template>
      <template v-else>
        <div></div>
      </template>
    </q-card-section>
  </q-card>
</template>

<script>
import { Dialog } from "quasar";
import { mapState } from "vuex";
import marked from "marked";
import DHelpMarkdown from "@/components/dialog/DHelpMarkdown";
import { debounce } from "lodash-es";
import { api } from "@/api";

export default {
  name: "OutlinerViewport",
  created: async function () {},
  beforeUnmount() {
    this.saveFile();
  },
  data: function () {
    return {
      fileSource: undefined,
      fileUid: undefined,
      fileType: undefined,
      loading: false,
      showEdit: true,
      showView: true,
      showSaveBtn: false,
      md: "",
      jsondoc: "",
      mdName: "",
    };
  },
  components: {},
  computed: mapState({
    markdown_fmt() {
      return marked(this.md);
    },
    mode: (state) => state.current.outlinerViewMode,
  }),
  methods: {
    update: debounce(function (e) {
      this.md = e.target.value;
    }, 100),
    async setFile(uid, source, type) {
      this.saveFile();
      this.loading = true;
      this.md = "";
      this.jsondoc = "";
      this.fileSource = source;
      this.fileUid = uid;
      this.fileType = type;
      if (source == "markdown") {
        await this.showMarkdown();
        this.showSaveBtn = true;
      } else if (source == "jsondoc") {
        await this.showJSONDoc();
        this.showSaveBtn = false;
      } else {
        this.showSaveBtn = false;
        this.loading = false;
      }
    },
    saveFile() {
      if (this.fileSource == "markdown") this.saveMarkdown();
    },
    saveMarkdown() {
      this.$store.dispatch("aMarkdownUpdate", {
        uid: this.fileUid,
        data: { md: this.md },
      }).auth;
    },
    async showMarkdown() {
      if (this.$store.state.markdown.markdown_data[this.fileUid] === undefined) {
        await this.$store.dispatch("aMarkdownLoad", this.fileUid);
      }
      this.md = this.$store.state.markdown.markdown_data[this.fileUid].md;
      this.mdName = this.$store.state.markdown.markdown_data[this.fileUid].name;
      this.loading = false;
    },
    async setMode(mode) {
      this.$store.state.current.outlinerViewMode = mode;
    },
    async showMarkdownSyntax() {
      Dialog.create({
        component: DHelpMarkdown,
      });
    },
    async showJSONDoc() {
      const res = await api.jsondoc.get(this.fileUid);
      if (!res.data) {
        this.loading = false;
        return;
      };
      try {
        this.jsondoc = JSON.stringify(JSON.parse(res.data.jsondoc), null, 2);
      } catch (error) {
        this.jsondoc = res.data.jsondoc;
      }
      this.loading = false;
    },
  },
};
</script>

<style scoped>
.edit-viewport {
  flex-wrap: nowrap;
  overflow: hidden;
  max-height: 100%;
  max-width: 100%;
}

.output {
  overflow: auto;
  max-height: 100%;
  max-width: 100%;
  padding: 0px 5px 0px 10px;
  min-width: 50%;
  box-sizing: border-box;
  word-wrap: break-word;
}

.input {
  resize: none;
  min-width: 50%;
  max-height: 100%;
}

.back-grey {
  background-color: #172830;
}
</style>
