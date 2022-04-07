<template>
  <q-dialog ref="dialogRef" @hide="onDialogHide">
    <q-card class="column" style="max-width: 80vw; max-height: 80vh; width: 800px; height: 800px">
      <q-card-section class="col row q-pa-none">
        <q-scroll-area class="col-6 scroll q-pa-md">
          <pre v-html="md"></pre>
        </q-scroll-area>
        <q-scroll-area class="col-6 scroll q-pa-md">
          <div v-html="output"></div>
        </q-scroll-area>
      </q-card-section>
      <q-separator />
      <q-card-actions align="right" class="bg-white text-teal">
        <q-btn color="primary" label="OK" @click="onOKClick" />
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<script>
import { useDialogPluginComponent } from "quasar";
import marked from "marked";

export default {
  data: function () {
    return {
      md:
        `# Head 1
###### Head 6

**Bold** *Italic* ~The world is flat.~

> blockquote

\\* escaping \\*.

---

1. First item
1. Second item
1. Third item

* First item
  * Second item
* Third item

- [x] Write the press release
- [ ] Update the website
- [ ] Contact the media

\`*code*\`

[title](https://www.example.com)

![alt text](` +
        require("@/assets/tranquility.png") +
        `)

\`\`\`

{
  "firstName": "John",
  "lastName": "*Smith*",
  "age": 25
}
\`\`\`

`,
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
    onDialogHide: function () {},
    onOKClick: function () {
      this.onDialogOK();
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
.input,
.output {
  overflow: auto;
  width: 50%;
  height: 90%;
  box-sizing: border-box;
  padding: 0 20px;
}

.input {
  border: none;
  border-right: 1px solid #ccc;
  resize: none;
  outline: none;
  background-color: #f6f6f6;
  font-size: 14px;
  font-family: "Monaco", courier, monospace;
  padding: 20px;
}

.editor {
  display: flex;
}
</style>
