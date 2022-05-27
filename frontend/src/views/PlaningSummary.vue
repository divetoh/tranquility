<template>
  <div class="full-width text-center" v-if="daystate == undefined">
    <q-chip square text-color="white" class="bg-topbar q-pa-xs q-mb-md" style="width: 100%">
      <div class="text-center">Loading... <q-spinner-rings color="grey" size="md" /></div>
    </q-chip>
  </div>
  <div class="row full-width" v-else>
    <q-card class="col-xs-12 q-pa-md">
      <div class="text-h6">Day summary. {{ current_date }}.</div>
      <q-input
        outlined
        bottom-slots
        @change="saveDescription"
        :model-value="daystate.description"
        counter
        maxlength="2048"
        debounce="2000"
      >
        <template v-slot:before>
          <q-rating
            size="18px"
            :model-value="daystate.rating"
            @update:model-value="saveRating"
            :max="5"
            color="primary"
          />
        </template>
        <template v-slot:append>
          <q-btn round dense flat icon="save" />
        </template>
      </q-input>
    </q-card>
    <div class="q-pa-sm col row">
      <div v-if="hide_tasklist != true" class="col-xs-10 col-sm-6 col-md-4 q-pa-sm block_wrapper">
        <TaskList :actions="{ delblock: false }" />
      </div>
      <div class="col-xs-10 col-sm-6 col-md-4 q-pa-sm">
        <q-card class="q-mb-sm">
          <q-bar dense class="bg-card-head">
            <div class="text-weight-bold">Complited Task</div>
          </q-bar>
          <q-card-section class="text-left q-pa-sm">
            <q-list dense padding>
              <q-separator />
              <q-item-label caption>Regular task</q-item-label>
              <template v-if="regulartask != undefined">
                <q-item v-for="(value, name) in regulartaskstate" :key="name">
                  {{ regulartask[name].name }}
                </q-item>
              </template>
              <q-separator />
              <q-item-label caption>Planed task</q-item-label>
              <template v-if="comlitedtask != undefined">
                <q-item v-for="(value, index) in comlitedtask" :key="index">
                  {{ value }}
                </q-item>
              </template>
            </q-list>
          </q-card-section>
        </q-card>
      </div>
      <div class="col-xs-10 col-sm-6 col-md-4 q-pa-sm">
        <DailyTasks noadd :date="current_date" />
      </div>
    </div>
  </div>
</template>

<script>
import { mapState } from "vuex";
import TaskList from "@/components/TaskList";
import DailyTasks from "@/components/DailyTasks";

export default {
  name: "PlaningSummary",
  props: ["summary_date", "hide_tasklist"],
  components: {
    TaskList,
    DailyTasks,
  },
  data: function () {
    return {
      current_date: undefined,
    };
  },
  created: async function () {
    if (!this.summary_date) {
      if (this.$store.state.current.date == undefined) await this.$store.dispatch("aCurrentSetDate");
      this.current_date = this.$store.state.current.date;
    } else {
      this.current_date = this.summary_date;
    }
    if (this.$store.state.daystate.lst[this.current_date] === undefined)
      await this.$store.dispatch("aDaystateLoad", this.current_date);
    if (this.$store.state.regulartaskstate.lst[this.current_date] === undefined)
      await this.$store.dispatch("aRegulartaskstateLoad", this.current_date);
  },
  methods: {
    saveRating: async function (rating) {
      await this.$store.dispatch("aDaystateSetRating", { statedate: this.current_date, rating });
    },
    saveDescription: async function (description) {
      await this.$store.dispatch("aDaystateSetDescription", { statedate: this.current_date, description });
    },
  },
  computed: mapState({
    daystate: function (state) {
      if (this.current_date == undefined) return undefined;
      return state.daystate.lst[this.current_date];
    },
    regulartaskstate: function (state) {
      if (this.current_date == undefined) return undefined;
      return state.regulartaskstate.lst[this.current_date];
    },
    regulartask: function (state) {
      if (state.regulartask.lst == undefined) return undefined;
      return state.regulartask.lst;
    },
    comlitedtask: function (state) {
      if (this.current_date == undefined) return undefined;
      return state.daystate.lst[this.current_date].complited;
    },
  }),
};
</script>
