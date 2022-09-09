<template>
  <div class="full-width full-height">
    <q-list bordered class="text-white text-left" dense>
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
          <q-icon name="note" dense size="xs" />
        </q-item-section >
        <q-item-section>{{ item.name }}.{{ item.type }}</q-item-section>
      </q-item>
    </q-list>
  </div>
</template>

<script>
import { mapState } from "vuex";
import { api } from "@/api";

export default {
  name: "FileList",
  created: async function () {},
  data: function () {
    return {
      folder: undefined,
      folderContent: [],
      fileSelected: undefined,
      fileSource: undefined,
      fileUid: undefined,
    };
  },
  emits: ["select"],
  components: {},
  computed: mapState({}),
  methods: {
    async setFolder(uid) {
      if (this.folder == uid) return;
      this.folder = uid;
      this.folderContent = [];
      this.fileSelect();
      if (uid) {
        this.folderContent = (await api.folder.get_content(uid)).data;
      }
    },
    async fileSelect(uid, source, type) {
      this.fileSelected = source + "." + uid;
      this.fileUid = uid;
      this.fileSource = source;
      this.$emit("select", uid, source, type);
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
