<template>
  <q-page
    class="flex full-width full-height q-ma-none"
    style="
      overflow: hidden;
      max-width: 100%;
      max-height: 100%;
      min-width: 100%;
      min-height: 100%;
      box-sizing: border-box;
      flex-wrap: nowrap;
      flex-direction: row;
    "
    v-if="loaded"
  >
    <FileSelector
      @select="selectFile"
      @selectFolder="selectFolder"
      :startFolder="folderUid"
      :startFile="fileUid"
      :startFileSource="fileSource"
    />
    <div class="column q-ma-sm" style="flex-wrap: nowrap; flex: 1 1; max-height: 100%">
      <OutlinerViewport ref="viewport" :startFile="fileUid" :startFileSource="fileSource" />
    </div>
  </q-page>
</template>

<script>
import FileSelector from "@/components/FileSelector";
import OutlinerViewport from "@/components/OutlinerViewport";
import { mapState } from "vuex";

export default {
  name: "Outliner",
  components: {
    FileSelector,
    OutlinerViewport,
  },
  created: function () {
    if (this.$route.params.fld_uid != undefined) {
      // Folder set in URL, update store
      if (this.$store.state.current.folderUid != this.$route.params.fld_uid)
        this.$store.dispatch("aCurrentSetFolder", this.$route.params.fld_uid);
      this.folderUid = this.$route.params.fld_uid;

      if (this.$route.params.file_uid) {
        // File set in URL
        const file = this.$route.params.file_uid.split(".");
        if (file[0] == "markdown" || file[0] != "json") {
          this.$store.dispatch("aCurrentSetFile", { uid: file[1], source: file[0] });
        }
      }
    }
    this.updateUrl();
  },
  data: function () {
    return {};
  },
  methods: {
    updateUrl() {
      // Update URL with values from store
      if (this.$store.state.current.fileUid)
        this.$router.replace({
          path:
            "/ol/" +
            this.$store.state.current.folderUid +
            "/" +
            this.$store.state.current.fileSource +
            "." +
            this.$store.state.current.fileUid,
        });
      else this.$router.replace({ path: "/ol/" + this.$store.state.current.folderUid });
    },
    async selectFile(uid, source, type) {
      await this.$refs.viewport.setFile(uid, source, type);
      await this.$store.dispatch("aCurrentSetFile", { source, uid });
      this.updateUrl();
    },
    async selectFolder(uid) {
      if (!uid) uid = 0;
      await this.$store.dispatch("aCurrentSetFolder", uid);
      this.updateUrl();
    },
  },
  computed: mapState({
    loaded: (state) => state.folder.root.length > 0,
    folderUid: (state) => state.current.folderUid,
    fileUid: (state) => state.current.fileUid,
    fileSource: (state) => state.current.fileSource,
  }),
};
</script>
