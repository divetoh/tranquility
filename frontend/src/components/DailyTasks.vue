<template>
  <q-card class="q-mb-sm">
    <q-card-section class="text-center" v-if="dailytasks === null">
      Loading... <q-spinner-rings color="grey" size="md" />
    </q-card-section>
    <template v-else>
      <q-bar dense class="bg-card-head">
        <div class="text-weight-bold">Daily Task</div>
        <q-space />
        <q-btn flat dense round color="blue" @click="edit" icon="edit" size="xs">
          <q-tooltip :delay="550" anchor="top middle" self="center middle">Edit</q-tooltip>
        </q-btn>
      </q-bar>
      <q-card-section class="text-left q-pa-sm">
        <q-list dense padding>
          <template v-for="dailytask in dailytasks" :key="dailytask">
            <DailyTaskLine :noadd="noadd" :uid="dailytask.uid" :date="date" v-if="dailytask.is_active" />
          </template>
        </q-list>
      </q-card-section>
    </template>
  </q-card>
</template>

<script>
import { mapState } from "vuex";
import { Dialog } from "quasar";
import DailyTaskLine from "@/components/items/DailyTaskLine";
import DEditDailyTask from "@/components/dialog/DEditDailyTask";

export default {
  name: "DailyTasks",
  created: async function () {
    if (this.$store.state.dailytask.lst === null) {
      await this.$store.dispatch("aDailytasksLoad");
    }
  },
  props: ["noadd", "date"],
  components: {
    DailyTaskLine,
  },
  computed: mapState({
    dailytasks: function (state) {
      // TODO: list daily task actual for target date
      return state.dailytask.lst;
    },
  }),
  methods: {
    async edit() {
      Dialog.create({
        component: DEditDailyTask,
      });
    },
  },
};
</script>
