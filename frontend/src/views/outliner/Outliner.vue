<template>
  <q-page
    class="flex full-width full-height q-ma-none"
    style="overflow: hidden; max-width: 100%; max-height: 100%; box-sizing: border-box"
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
    selectFile(uid, source, type) {
      this.$refs.viewport.setFile(uid, source, type);
    },
  },
};
</script>
