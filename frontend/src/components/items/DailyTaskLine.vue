<template>
  <q-item clickable dense class="q-gutter-xs">
    <q-item-section side>
      <div class="q-gutter-xs">
        <q-btn color="blue" flat dense round v-on:click="add" icon="playlist_add" size="sm" v-if="noadd == undefined">
          <q-tooltip :delay="550" anchor="top middle" self="center middle">Add to task List</q-tooltip>
        </q-btn>
        <q-checkbox
          size="sm"
          toggle-indeterminate
          dense
          toggle-order="ft"
          :model-value="dailytaskstate"
          @update:model-value="done"
          color="blue"
          checked-icon="task_alt"
          indeterminate-icon="not_interested"
          unchecked-icon="highlight_off"
        />
      </div>
    </q-item-section>
    <q-item-section>
      {{ dailytask.name }}
    </q-item-section>
  </q-item>
</template>

<script>
import { mapState } from "vuex";

export default {
  name: "DailyTaskLine",
  props: ["uid", "noadd", "date"],
  data: function () {
    return {
      dtl_date: "",
    };
  },
  created: async function () {
    if (this.date != null) this.dtl_date = this.date;
    else this.dtl_date = this.$store.state.current.date;
  },
  components: {},
  methods: {
    done: async function (data) {
      await this.$store.dispatch("aDailytaskstateSet", {
        statedate: this.dtl_date,
        taskstate: { null: 2, true: 1, false: 0 }[data],
        dailytask: this.uid,
      });
      if (data != false)
        await this.$store.dispatch("aTaskListRemoveDailyTask", {
          uid: this.$store.state.auth.userProfile.coretasklist,
          dailytask: this.uid,
        });
    },
    add: async function () {
      await this.$store.dispatch("aTaskListAddItem", {
        uid: this.$store.state.auth.userProfile.coretasklist,
        item: {
          text: this.$store.state.dailytask.lst[this.uid].name,
          dailytask: this.uid,
          type: "dailytask",
          noedit: true,
        },
      });
    },
  },
  computed: mapState({
    dailytask(state) {
      return state.dailytask.lst[this.uid];
    },
    dailytaskstate(state) {
      if (
        state.dailytaskstate.lst[this.dtl_date] == undefined ||
        state.dailytaskstate.lst[this.dtl_date][this.uid] == undefined
      )
        return undefined;
      return [false, true, null][state.dailytaskstate.lst[this.dtl_date][this.uid]];
    },
  }),
};
</script>
