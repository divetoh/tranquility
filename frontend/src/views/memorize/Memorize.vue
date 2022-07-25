<template>
  <q-page class="">
    <div class="column">
      <q-tabs v-model="tab" no-caps dense align="left" narrow-indicator class="bg-topbar text-white">
        <q-route-tab name="learn" label="Learn" to="/memorize/learn" />
        <q-route-tab name="manage" label="Manage" to="/memorize/manage" />
        <q-route-tab name="statistics" label="Statistics" to="/memorize/statistics" />
      </q-tabs>
    </div>
    <div v-if="tab == 'learn'">
      <MemorizeLearn />
    </div>
    <div v-if="tab == 'manage'">
      <MemorizeManage />
    </div>
    <div v-if="tab == 'statistics'">
      <MemorizeStatistics />
    </div>
  </q-page>
</template>

<script>
import { mapState } from "vuex";
import MemorizeLearn from "@/views/memorize/MemorizeLearn";
import MemorizeManage from "@/views/memorize/MemorizeManage";
import MemorizeStatistics from "@/views/memorize/MemorizeStatistics";

export default {
  name: "Memorize",
  data: function () {
    return {
      tab: "learn",
    };
  },
  components: {
    MemorizeLearn,
    MemorizeManage,
    MemorizeStatistics,
  },
  created: async function () {
    await this.$store.dispatch("aMemorizeCategoryLoad");
    await this.$store.dispatch("aMemorizeStackLoad");
  },
  methods: {},
  computed: mapState({}),
};
</script>
