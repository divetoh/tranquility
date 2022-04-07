<template>
  <q-dialog ref="dialogRef" @hide="onDialogHide" full-height full-width>
    <q-card class="column">
      <q-card-section class="col row">
        <textarea class="input col-6" :value="md" @input="update"></textarea>
        <div class="output col-6 q-pl-lg" v-html="output"></div>
      </q-card-section>
      <q-separator />
      <q-card-actions align="right" class="bg-white text-teal">
        <q-btn icon="info" color="primary" no-caps label="Markdown syntax" @click="show_md_help" />
        <q-space />
        <q-btn color="primary" label="OK" @click="onOKClick" />
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<script>
import { useDialogPluginComponent, Dialog } from "quasar";
import { debounce } from "lodash-es";
import marked from "marked";
import DHelpMarkdown from "@/components/dialog/DHelpMarkdown";

export default {
  props: ["uid"],
  data: function () {
    return {
      md: "",
      name: "",
    };
  },
  computed: {
    output() {
      return marked(this.md);
    },
  },
  created: async function () {
    this.marked = marked;
    if (this.$store.state.markdown.markdown_data[this.uid] === undefined) {
      await this.$store.dispatch("aMarkdownLoad", this.uid);
    }
    this.md = this.$store.state.markdown.markdown_data[this.uid].md;
    this.name = this.$store.state.markdown.markdown_data[this.uid].name;
  },
  methods: {
    update: debounce(function (e) {
      this.md = e.target.value;
    }, 100),
    onDialogHide: function () {
      this.saveData();
    },
    onOKClick: function () {
      this.onDialogOK();
    },
    saveData: function () {
      this.$store.dispatch("aMarkdownSave", {
        md: this.md,
        name: this.name,
        uid: this.uid,
      }).auth;
    },
    show_md_help() {
      Dialog.create({
        component: DHelpMarkdown,
      });
    },
  },
  setup() {
    const { dialogRef, onDialogOK } = useDialogPluginComponent();
    return {
      dialogRef,
      onDialogOK,
    };
  },
};
</script>

<style scoped>
.input1,
.output1 {
  overflow: auto;
  width: 50%;
  height: 90%;
  box-sizing: border-box;
  padding: 0 20px;
}

.input1 {
  border: none;
  border-right: 1px solid #ccc;
  resize: none;
  outline: none;
  background-color: #f6f6f6;
  font-size: 14px;
  font-family: "Monaco", courier, monospace;
  padding: 20px;
}

.editor1 {
  display: flex;
}
</style>
