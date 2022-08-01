<template>
  <div class="row full-width">
    <q-card class="col-xs-12 q-pa-md">
      <div class="q-mb-md">
        <q-btn @click="prevMonth" icon="navigate_before" flat />
        <span class="q-mx-xl">{{ date_v }}</span>
        <q-btn @click="nextMonth" icon="navigate_next" flat />
      </div>
      <div class="full-width text-center" v-if="loaded == false">
        <q-chip square text-color="white" class="bg-topbar q-pa-xs q-mb-md" style="width: 100%">
          <div class="text-center">Loading... <q-spinner-rings color="grey" size="md" /></div>
        </q-chip>
      </div>
      <template v-else>
        <!-- Table with DailyTask and RegularTask -->
        <div class="q-mb-lg">
          <q-markup-table dense bordered class="text-left" separator="cell">
            <thead class="bg-indigo-3 text-center">
              <tr>
                <th>Daily task</th>
                <th v-for="d in days" :key="d" @click="showSummary(d)">{{ d.substring(8, 10) }}</th>
                <th>Total</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="t in dailyTaskNonempty()" :key="t">
                <td>{{ t.name }}</td>
                <td v-for="d in days" :key="d" :class="dailyColor(d, t.uid)">&nbsp;</td>
                <td>
                  <span class="text-green-8">{{ t.count[1] }}</span> /
                  <span class="text-blue-8">{{ t.count[2] }}</span> /
                  <span class="text-grey-8">{{ t.count[0] }}</span>
                </td>
              </tr>
              <tr>
                <td style="border-top: solid 1px grey">Complited regular tasks</td>
                <td style="border-top: solid 1px grey" v-for="d in days" :key="d" class="text-center">
                  {{ countRegularTask(d) }}
                </td>
                <td style="border-top: solid 1px grey">{{ countAllRegularTask() }}</td>
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
                <tr v-if="dayState[d] != undefined">
                  <td @click="showSummary(d)">{{ d }}</td>
                  <td v-if="dayState[d].rating != 0" :class="rangeColor(dayState[d].rating) + ' text-center'">
                    {{ dayState[d].rating }}
                  </td>
                  <td v-else>&nbsp;</td>
                  <td>{{ dayState[d].description }}</td>
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
      </template>
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
      date: undefined,
      date_v: "",
      enddate: undefined,
      loaded: false,
    };
  },
  components: {},
  created: async function () {
    var dt = new Date(this.$store.state.current.date);
    await this.prepareData(dt);
  },
  methods: {
    async prepareData(dt) {
      this.loaded = false;
      dt.setDate(1);
      this.date = new Date(dt.getTime());
      this.date_v = this.$monthNames[dt.getMonth()] + " " + dt.getFullYear();
      this.days = [];
      const month = dt.getMonth();

      while (dt.getMonth() === month) {
        this.days.push(dt.toISOString().substring(0, 10));
        dt.setDate(dt.getDate() + 1);
      }
      // Load DayState, DailyTaskState, RegularTaskState for this range
      const dayrange = { start: this.days[0], end: this.days[this.days.length - 1] };
      await this.$store.dispatch("aDaystateLoadRng", dayrange);
      await this.$store.dispatch("aDailytaskstateLoadRng", dayrange);
      await this.$store.dispatch("aRegulartaskstateLoadRng", dayrange);
      this.loaded = true;
    },
    async prevMonth() {
      this.date.setMonth(this.date.getMonth() - 1);
      await this.prepareData(this.date);
    },
    async nextMonth() {
      this.date.setMonth(this.date.getMonth() + 1);
      await this.prepareData(this.date);
    },
    rangeColor(color) {
      return ["", "bg-yellow-1", "bg-yellow-2", "bg-lime-3", "bg-lime-4", "bg-light-green-4"][color];
    },
    dailyColor(day, task) {
      if (this.dailyTaskState[day] != undefined && this.dailyTaskState[day][task] != undefined)
        return ["bg-grey-7", "bg-light-green-4", "bg-light-blue-4"][this.dailyTaskState[day][task]];
      return "bg-grey-2";
    },
    countRegularTask(day) {
      if (this.regularTaskState[day] == undefined || Object.keys(this.regularTaskState[day]).length == 0) return " ";
      return Object.keys(this.regularTaskState[day]).length;
    },
    countAllRegularTask() {
      var count = 0;
      for (var j in this.days) {
        if (this.regularTaskState[this.days[j]] == undefined) continue;
        count += Object.keys(this.regularTaskState[this.days[j]]).length;
      }
      return count;
    },
    dailyTaskNonempty() {
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
    async showSummary(summary_date) {
      Dialog.create({
        component: DDaySummary,
        componentProps: {
          summary_date,
        },
      });
    },
  },
  computed: mapState({
    dayState: (state) => state.daystate.lst,
    dailyTask: (state) => state.dailytask.lst,
    dailyTaskState: (state) => state.dailytaskstate.lst,
    regularTaskState: (state) => state.regulartaskstate.lst,
  }),
};
</script>
