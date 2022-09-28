<template>
  <div class="full-width full-height">
    <q-list bordered class="text-white text-left" dense>
      <template v-for="item in subFolders" :key="item">
        <q-item
          clickable
          v-ripple
          active-class="act-menu-link"
          dense
          :active="fileSelected == 'folder.' + item.uid"
          @click="folderSelect(item.uid)"
          v-if="!filter || item.foldertype < 64"
        >
          <q-item-section side dense style="padding-right: 4px">
            <q-icon name="folder" dense size="xs" color="white" />
          </q-item-section>
          <q-item-section>{{ item.name }}</q-item-section>
        </q-item>
      </template>
      <q-item
        clickable
        v-ripple
        active-class="act-menu-link"
        dense
        v-for="item in folderContent"
        :key="item"
        :active="fileSelected == item.source + '.' + item.uid"
        @click="fileSelect(item.uid, item.source, item.type)"
      >
        <q-item-section side dense style="padding-right: 4px">
          <q-icon name="note" dense size="xs" color="blue-4" />
        </q-item-section >
        <q-item-section>{{ item.name }}.{{ item.type }}</q-item-section>
      </q-item>
    </q-list>
  </div>
</template>

<script>
import { mapState } from "vuex";
import { api } from "@/api";
import { Dialog } from "quasar";

export default {
  name: "FileList",
  created: async function () {
    await this.setFolder(undefined);
  },
  data: function () {
    return {
      folder: null,
      folderContent: [],
      subFolders: [],
      fileSelected: undefined,
      fileSource: undefined,
      fileUid: undefined,
    };
  },
  emits: ["select", "selectFolder"],
  components: {},
  computed: mapState({
    filter: (state) => state.current.folderFilter,
  }),
  methods: {
    async setFolder(uid) {
      if (this.folder === uid) return;
      this.folder = uid;
      this.folderContent = [];
      this.subFolders = [];
      await this.setFile();
      if (uid) {
        this.folderContent = (await api.folder.get_content(uid)).data;
        for (const i in this.$store.state.folder.lst) {
          const f = this.$store.state.folder.lst[i];
          if (f.parent == uid) this.subFolders.push({ uid: f.uid, name: f.name, foldertype: f.foldertype });
        }
      } else {
        for (const i of this.$store.state.folder.root) {
          const f = this.$store.state.folder.lst[i];
          this.subFolders.push({ uid: f.uid, name: f.name, foldertype: f.foldertype });
        }
      }
      this.subFolders.sort((a, b) => {
        if (a.name > b.name) return 1;
        if (a.name < b.name) return -1;
        return 0;
      });
    },
    async fileSelect(uid, source, type) {
      // Event: user select file
      await this.setFile(uid, source);
      this.$emit("select", uid, source, type);
    },
    async setFile(uid, source) {
      this.fileSelected = source + "." + uid;
      this.fileUid = uid;
      this.fileSource = source;
    },
    async folderSelect(uid) {
      if (this.fileSelected != "folder." + uid) {
        // First click
        this.fileSelected = "folder." + uid;
        this.fileUid = uid;
        this.fileSource = "folder";
        if (uid) this.$emit("select", uid, "folder", "folder");
      } else {
        // Second click
        await this.setFolder(uid);
        this.$emit("selectFolder", uid);
      }
    },
    async appendFile(uid, source, type, name) {
      this.folderContent.push({ uid, source, type, name });
      // TODO: scroll to file
    },
    async appendFolder(uid) {
      const f = this.$store.state.folder.lst[uid];
      this.subFolders.push({ uid: f.uid, name: f.name, foldertype: f.foldertype });
      // TODO: scroll to folder
    },
    async rename() {
      var oldname = "";
      if (this.fileSource == "folder") oldname = this.$store.state.folder.lst[this.fileUid].name;
      else {
        for (const i of this.folderContent)
          if (i.uid == this.fileUid && i.source == this.fileSource) {
            oldname = i.name;
            break;
          }
      }
      Dialog.create({
        title: "Rename",
        message: "New name",
        prompt: {
          model: oldname,
          isValid: (val) => val.length > 0,
          type: "text",
        },
        cancel: true,
        persistent: true,
      }).onOk((data) => {
        if (this.fileSource == "folder") {
          this.$store.dispatch("aFolderSetName", { uid: this.fileUid, name: data });
          for (const i of this.subFolders)
            if (i.uid == this.fileUid) {
              i.name = data;
              break;
            }
        } else {
          this.$store.dispatch("aFolderSetFileName", { uid: this.fileUid, source: this.fileSource, name: data });
          for (const i of this.folderContent)
            if (i.uid == this.fileUid && i.source == this.fileSource) {
              i.name = data;
              break;
            }
        }
      });
    },
    async remove() {
      var oldname = "";
      if (this.fileSource == "folder") {
        oldname = this.$store.state.folder.lst[this.fileUid].name;
        for (const i in this.$store.state.folder.lst)
          if (this.$store.state.folder.lst[i].parent == parseInt(this.fileUid)) {
            alert("Can't delete folder containing subfolders.");
            return;
          }
      } else {
        for (const i of this.folderContent)
          if (i.uid == this.fileUid && i.source == this.fileSource) {
            oldname = i.name;
            break;
          }
      }
      Dialog.create({
        title: "Confirm",
        dark: true,
        message: "Confirm delete: " + oldname + "?",
        cancel: true,
        persistent: true,
      }).onOk(() => {
        if (this.fileSource == "folder") {
          this.$store.dispatch("aFolderRemove", { uid: this.fileUid });
          for (const i in this.subFolders)
            if (this.subFolders[i].uid == this.fileUid) {
              this.subFolders.splice(i, 1);
              break;
            }
        } else {
          this.$store.dispatch("aFolderRemoveFile", { uid: this.fileUid, source: this.fileSource });
          for (const i in this.folderContent)
            if (this.folderContent[i].uid == this.fileUid && this.folderContent[i].source == this.fileSource) {
              this.folderContent.splice(i, 1);
              break;
            }
        }
      });
    },
    async move(folder) {
      if (folder == this.folder) return;
      if (this.fileSource == "folder") {
        this.$store.dispatch("aFolderMove", { uid: this.fileUid, folder });
        for (const i in this.subFolders)
          if (this.subFolders[i].uid == this.fileUid) {
            this.subFolders.splice(i, 1);
            break;
          }
      } else {
        this.$store.dispatch("aFolderMoveFile", { uid: this.fileUid, source: this.fileSource, folder });
        for (const i in this.folderContent)
          if (this.folderContent[i].uid == this.fileUid && this.folderContent[i].source == this.fileSource) {
            this.folderContent.splice(i, 1);
            break;
          }
      }
    },
  },
};
</script>

<style scoped>
.act-menu-link {
  background-color: #172830;
  color: white;
}
</style>
