<template>
  <div class="full-width text-center" v-if="loaded == false">
    <q-chip square text-color="white" class="bg-topbar q-pa-xs q-mb-md" style="width: 100%">
      <div class="text-center">Loading... <q-spinner-rings color="grey" size="md" /></div>
    </q-chip>
  </div>
  <div class="row full-width" v-else>
    <q-card class="col-xs-12 q-pa-md">
      <!-- Table with DailyTask and RegularTask -->
      <div class="q-mb-lg">
        <q-markup-table dense bordered class="text-left" separator="cell">
          <thead class="bg-indigo-3 text-center">
            <tr>
              <th>Daily task</th>
              <th v-for="d in days" :key="d" @click="showsummary(d)">{{ d.substring(8, 10) }}</th>
              <th>Total</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="t in dailytask_nonempty()" :key="t">
              <td>{{ t.name }}</td>
              <td v-for="d in days" :key="d" :class="dailycolor(d, t.uid)">&nbsp;</td>
              <td>
                <span class="text-green-8">{{ t.count[1] }}</span> /
                <span class="text-blue-8">{{ t.count[2] }}</span> /
                <span class="text-grey-8">{{ t.count[0] }}</span>
              </td>
            </tr>
            <tr>
              <td style="border-top: solid 1px grey">Complited regular tasks</td>
              <td style="border-top: solid 1px grey" v-for="d in days" :key="d" class="text-center">
                {{ countregulartask(d) }}
              </td>
              <td style="border-top: solid 1px grey">{{ countallregulartask() }}</td>
            </tr>
          </tbody>
        </q-markup-table>
      </div>
      <!--  Table with DailyState  -->
      <div>
        <q-markup-table dense bordered class="text-left">
          <thead class="bg-indigo-3">
            <tr>
              <th>Date</th>
              <th>Rate</th>
              <th style="width: 99%">Summary</th>
            </tr>
          </thead>
          <tbody>
            <template v-for="d in days" :key="d">
              <tr v-if="daystate[d] != undefined">
                <td @click="showsummary(d)">{{ d }}</td>
                <td v-if="daystate[d].rating != 0" :class="rangecolor(daystate[d].rating) + ' text-center'">
                  {{ daystate[d].rating }}
                </td>
                <td v-else>&nbsp;</td>
                <td>{{ daystate[d].description }}</td>
              </tr>
              <tr v-else class="bg-grey-2 text-grey-6">
                <td>{{ d }}</td>
                <td>&nbsp;</td>
                <td>&nbsp;</td>
              </tr>
            </template>
          </tbody>
        </q-markup-table>
      </div>
    </q-card>
  </div>
</template>

<script>
import { mapState } from "vuex";
import { Dialog } from "quasar";
import DDaySummary from "@/components/dialog/DDaySummary";

export default {
  name: "PlaningRetrospective",
  props: [],
  data: function () {
    return {
      days: [],
      enddate: undefined,
      loaded: false,
    };
  },
  components: {},
  created: async function () {
    var date = new Date(this.$store.state.current.date);
    date.setDate(1);
    const month = date.getMonth();

    while (date.getMonth() === month) {
      this.days.push(date.toISOString().substring(0, 10));
      date.setDate(date.getDate() + 1);
    }
    // Load DayState, DailyTaskState, RegularTaskState for this range
    const dayrange = { start: this.days[0], end: this.days[this.days.length - 1] };
    await this.$store.dispatch("aDaystateLoadRng", dayrange);
    await this.$store.dispatch("aDailytaskstateLoadRng", dayrange);
    await this.$store.dispatch("aRegulartaskstateLoadRng", dayrange);
    // TODO: Format daily task list

    this.loaded = true;
  },
  methods: {
    rangecolor(color) {
      return ["", "bg-yellow-1", "bg-yellow-2", "bg-lime-3", "bg-lime-4", "bg-light-green-4"][color];
    },
    dailycolor(day, task) {
      if (this.dailytaskstate[day] != undefined && this.dailytaskstate[day][task] != undefined)
        return ["bg-grey-7", "bg-light-green-4", "bg-light-blue-4"][this.dailytaskstate[day][task]];
      return "bg-grey-2";
    },
    countregulartask(day) {
      if (this.regulartaskstate[day] == undefined || Object.keys(this.regulartaskstate[day]).length == 0) return " ";
      return Object.keys(this.regulartaskstate[day]).length;
    },
    countallregulartask() {
      var count = 0;
      for (var j in this.days) {
        if (this.regulartaskstate[this.days[j]] == undefined) continue;
        count += Object.keys(this.regulartaskstate[this.days[j]]).length;
      }
      return count;
    },
    dailytask_nonempty() {
      var lst = [];
      const tasks = this.$store.state.dailytask.lst;
      const states = this.$store.state.dailytaskstate.lst;
      for (var i in tasks) {
        const tsk = tasks[i];
        var count = [0, 0, 0];
        for (var j in this.days) {
          if (states[this.days[j]] == undefined) continue;
          if (states[this.days[j]][i] == undefined) continue;
          count[parseInt(states[this.days[j]][i])] += 1;
        }
        if (count[0] + count[1] + count[2] > 0) lst.push({ name: tsk.name, uid: i, count: count });
      }
      return lst;
    },
    async showsummary(summary_date) {
      Dialog.create({
        component: DDaySummary,
        componentProps: {
          summary_date,
        },
      });
    },
  },
  computed: mapState({
    daystate: (state) => state.daystate.lst,
    dailytask: (state) => state.dailytask.lst,
    dailytaskstate: (state) => state.dailytaskstate.lst,
    regulartaskstate: (state) => state.regulartaskstate.lst,
  }),
};
</script>
