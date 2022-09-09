<template>
  <div
    class="w600 column q-py-sm q-pl-sm"
    style="overflow: hidden; max-height: 100%; flex-wrap: nowrap; max-width: 600px; box-model: border-box"
  >
    <q-bar class="row text-white q-mb-sm shadow-2 full-width" style="background-color: #394454ce" size="xs">
      <q-space />
      <q-btn
        icon="keyboard_arrow_up"
        size="sm"
        dense
        flat
        no-caps
        style="background-color: #172830"
        :disabled="selectedFolder === undefined"
      />
      <q-btn-dropdown dropdown-icon="add_circle" dense size="sm" flat no-caps style="background-color: #172830">
        <q-list dense>
          <q-item clickable v-close-popup dense>
            <q-item-section side>
              <q-icon name="folder" color="primary" />
            </q-item-section>
            <q-item-section>
              <q-item-label>Folder</q-item-label>
            </q-item-section>
          </q-item>
          <q-item clickable v-close-popup dense :disabled="selectedFolder === undefined">
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
          <FolderTree @select="selectFolder" />
        </div>
      </div>
      <div
        class="column q-pl-sm"
        style="overflow: hidden; max-width: 50%; max-height: 100%; width: 50%; box-sizing: border-box"
      >
        <div style="background-color: #394454ce; overflow-y: auto" class="full-width full-height scroll6">
          <FileList ref="filelist" @select="selectFile" />
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
    };
  },
  methods: {
    selectFolder(uid) {
      this.selectedFolder = uid;
      this.$refs.filelist.setFolder(uid);
    },
    selectFile(uid, source, type) {
      this.$emit("select", uid, source, type);
    },
  },
};
</script>
