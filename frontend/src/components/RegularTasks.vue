<template>
  <q-card class="q-mb-sm">
    <q-card-section class="text-center" v-if="sortedtasks === null">
      Loading... <q-spinner-rings color="grey" size="md" />
    </q-card-section>
    <template v-else>
      <q-bar dense class="bg-card-head">
        <div class="text-weight-bold">Regular Task</div>
        <q-space />
        <q-btn flat dense round color="blue" v-on:click="edit" icon="edit" size="xs">
          <q-tooltip :delay="550" anchor="top middle" self="center middle"> Edit </q-tooltip>
        </q-btn>
      </q-bar>
      <q-card-section class="text-left q-pa-sm">
        <template v-for="(n, index) in sortedtasks" :key="index">
          <q-list dense padding>
            <q-separator />
            <q-item-label caption>{{ n.name }}</q-item-label>
            <RegularTaskLine v-for="regulartask in n.tasks" :uid="regulartask" :key="regulartask"></RegularTaskLine>
          </q-list>
        </template>
      </q-card-section>
    </template>
  </q-card>
</template>

<script>
import { mapState } from "vuex";
import RegularTaskLine from "@/components/items/RegularTaskLine";
import { Dialog } from "quasar";
import DEditRegulartask from "@/components/dialog/DEditRegulartask";

export default {
  name: "RegularTasks",
  created: async function () {
    if (this.$store.state.regulartask.lst === null) {
      await this.$store.dispatch("aRegulartasksLoad");
    }
  },
  components: {
    RegularTaskLine,
  },
  computed: mapState({
    sortedtasks: function (state) {
      var regtasks = state.regulartask.lst;
      // Prepare list
      var d = new Date();
      d.setHours(d.getHours() - 2);
      d.setHours(0);
      d.setMinutes(0);
      d.setSeconds(0);
      var start_ts = parseInt(d.getTime() / 1000);
      var daily_plan = [];
      var d_names = [
        "Missed tasks",
        "Today",
        "Tomorrow",
        "After 1 day",
        "After 2 days",
        "After 3 days",
        "After 4 days",
        "After 5 days",
      ];
      for (var i = 0; i < 7; i++) {
        daily_plan.push({
          ts: start_ts + 24 * 60 * 60 * i,
          name: d_names[i],
          tasks: [],
        });
      }
      for (var j in regtasks) {
        var task = regtasks[j];
        if (!task.is_active) continue;
        var ts = new Date(task.nextdate).getTime() / 1000;
        for (i = 0; i < 7; i++) {
          if (ts >= daily_plan[i].ts) continue;
          daily_plan[i].tasks.push(task.uid);
          break;
        }
      }
      return daily_plan;
    },
  }),
  methods: {
    async edit() {
      Dialog.create({
        component: DEditRegulartask,
        componentProps: {
          uid: this.$props.uid,
        },
      });
    },
  },
};
</script>
