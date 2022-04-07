<template>
  <q-page class="fit scroll">
    <div>
      <q-tabs v-model="tab" no-caps dense align="left" narrow-indicator class="bg-topbar text-white">
        <q-route-tab name="tasks" label="Tasks" to="/planing/tasks" />
        <q-route-tab name="summary" label="Summary" to="/planing/summary" />
        <q-route-tab name="retrospective" label="Retrospective" to="/planing/retrospective" />
      </q-tabs>
    </div>
    <div class="col row no-wrap scroll q-pa-sm" v-if="tab == 'tasks'">
      <PlaningTasks />
    </div>
    <div class="col row no-wrap" v-if="tab == 'summary'">
      <PlaningSummary />
    </div>
    <div class="row fit no-wrap items-start content-start" v-if="tab == 'retrospective'">
      <PlaningRetrospective />
    </div>
  </q-page>
</template>

<script>
import { mapState } from "vuex";
import { ref } from "vue";
import PlaningTasks from "@/views/PlaningTasks";
import PlaningSummary from "@/views/PlaningSummary";
import PlaningRetrospective from "@/views/PlaningRetrospective";

export default {
  name: "Planing",

  components: {
    PlaningTasks,
    PlaningSummary,
    PlaningRetrospective,
  },
  created: async function () {},
  methods: {},
  computed: mapState({}),

  setup() {
    return {
      tab: ref("tasks"),
    };
  },
};
</script>
