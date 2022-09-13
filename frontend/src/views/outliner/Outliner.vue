<template>
  <q-page
    class="flex full-width full-height q-ma-none"
    style="overflow: hidden; max-width: 100%; max-height: 100%; box-sizing: border-box"
    v-if="loaded"
  >
    <FileSelector @select="selectFile" />
    <div class="column col-grow q-ma-sm">
      <OutlinerViewport ref="viewport" />
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
  data: function () {
    return {};
  },
  methods: {
    async selectFile(uid, source, type) {
      await this.$refs.viewport.setFile(uid, source, type);
    },
  },
  computed: mapState({
    loaded: function (state) {
      return state.folder.root.length > 0;
    },
  }),
};
</script>
