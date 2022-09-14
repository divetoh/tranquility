<template>
  <div
    class="w600 column q-py-sm q-pl-sm"
    style="overflow: hidden; max-height: 100%; flex-wrap: nowrap; max-width: 600px; box-model: border-box"
  >
    <q-bar class="row text-white q-mb-sm shadow-2 full-width" style="background-color: #394454ce" size="xs">
      <q-space />
      <q-btn
        size="sm"
        dense
        flat
        no-caps
        color="white"
        style="background-color: #172830"
        icon="drive_file_rename_outline"
        :disabled="selectedFile === undefined"
        @click="renameFile"
      />
      <q-btn
        size="sm"
        dense
        flat
        no-caps
        color="white"
        style="background-color: #172830"
        icon="drive_file_move"
        :disabled="selectedFile === undefined"
      >
        <q-menu dark ref="moveMenuRef">
          <div class="column w300 q-pa-md" style="max-height: 70vh">
            <FolderTree ref="movetofolderlist" @select="selectMoveDestination" />
          </div>
        </q-menu>
      </q-btn>
      <q-btn
        size="sm"
        dense
        flat
        no-caps
        color="white"
        style="background-color: #172830"
        icon="delete"
        :disabled="selectedFile === undefined"
        @click="removeFile"
      />
      <q-btn
        icon="keyboard_arrow_up"
        size="sm"
        dense
        flat
        no-caps
        style="background-color: #172830"
        :disabled="selectedFolder === undefined"
        @click="parentFolder"
      />
      <q-btn-dropdown dropdown-icon="add_circle" dense size="sm" flat no-caps style="background-color: #172830">
        <q-list dense>
          <q-item clickable v-close-popup dense @click="createFolder">
            <q-item-section side>
              <q-icon name="folder" color="primary" />
            </q-item-section>
            <q-item-section>
              <q-item-label>Folder</q-item-label>
            </q-item-section>
          </q-item>
          <q-item clickable v-close-popup dense v-if="selectedFolder !== undefined" @click="createMarkdown">
            <q-item-section side>
              <q-icon name="note" color="primary" />
            </q-item-section>
            <q-item-section>
              <q-item-label>Markdown</q-item-label>
            </q-item-section>
          </q-item>
        </q-list>
      </q-btn-dropdown>
    </q-bar>
    <div class="row" style="overflow: hidden; box-sizing: border-box; max-height: 100%; height: 100%">
      <div class="column" style="overflow: hidden; width: 50%">
        <div
          style="background-color: #394454ce; overflow-y: auto; box-sizing: border-box"
          class="full-width full-height scroll6"
        >
          <FolderTree ref="folderlist" @select="selectFolder" />
        </div>
      </div>
      <div
        class="column q-pl-sm"
        style="overflow: hidden; max-width: 50%; max-height: 100%; width: 50%; box-sizing: border-box"
      >
        <div style="background-color: #394454ce; overflow-y: auto" class="full-width full-height scroll6">
          <FileList ref="filelist" @select="selectFile" @selectFolder="selectFolderFromFilePanel" />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import FolderTree from "@/components/FolderTree";
import FileList from "@/components/FileList";

export default {
  name: "FileSelector",
  components: {
    FolderTree,
    FileList,
  },
  emits: ["select"],
  data: function () {
    return {
      selectedFolder: undefined,
      selectedFile: undefined,
      selectedSource: undefined,
      selectedType: undefined,
    };
  },
  methods: {
    async selectFolder(uid) {
      this.selectedFolder = uid;
      this.$refs.filelist.setFolder(uid);
    },
    async selectFolderFromFilePanel(uid) {
      this.selectedFolder = uid;
      this.$refs.folderlist.setFolder(this.selectedFolder);
    },
    async selectFile(uid, source, type) {
      this.selectedFile = uid;
      this.selectedSource = source;
      this.selectedType = type;
      if (uid) this.$emit("select", uid, source, type);
    },
    async createMarkdown() {
      if (!this.selectedFolder) return;
      var markdown = await this.$store.dispatch("aMarkdownCreate", {
        name: "New markdown",
        md: "New markdown.",
        folder: this.selectedFolder,
      });
      await this.$refs.filelist.appendFile(markdown, "markdown", "markdown", "New markdown");
      await this.$refs.filelist.fileSelect(markdown, "markdown", "markdown");
    },
    async createFolder() {
      const data = { name: "New folder", foldertype: 1 };
      if (this.selectedFolder) data.parent = this.selectedFolder;
      var folder = await this.$store.dispatch("aFolderCreate", data);
      await this.$refs.filelist.appendFolder(folder);
      await this.$refs.filelist.folderSelect(folder);
    },
    async parentFolder() {
      if (this.selectedFolder === undefined) return;
      this.selectedFolder = this.$store.state.folder.lst[this.selectedFolder].parent;
      this.$refs.filelist.setFolder(this.selectedFolder);
      this.$refs.folderlist.setFolder(this.selectedFolder);
    },
    async renameFile() {
      this.$refs.filelist.rename();
    },
    async removeFile() {
      this.$refs.filelist.remove();
    },
    async selectMoveDestination(uid) {
      this.$refs.moveMenuRef.hide();
      this.$refs.filelist.move(uid);
    },
  },
};
</script>
