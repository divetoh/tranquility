<template>
  <div class="col-xs-10 col-sm-6 col-md-4 q-pa-sm">
    <TaskList :actions="{ delblock: false }" />
  </div>
  <div class="col-xs-10 col-sm-6 col-md-4 q-pa-sm">
    <RegularTasks />
  </div>
  <div class="col-xs-10 col-sm-6 col-md-4 q-pa-sm">
    <DailyTasks />
  </div>
</template>

<script>
import { mapState } from "vuex";
import TaskList from "@/components/TaskList";
import RegularTasks from "@/components/RegularTasks";
import DailyTasks from "@/components/DailyTasks";

export default {
  name: "PlaningTasks",

  components: {
    RegularTasks,
    DailyTasks,
    TaskList,
  },
  created: async function () {},
  methods: {},
  computed: mapState({}),
};
</script>
