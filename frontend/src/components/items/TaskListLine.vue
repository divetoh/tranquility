<template>
  <q-item clickable dense class="q-pl-none q-py-xs">
    <q-item-section side>
      <div class="">
        <q-icon class="tldrag_handler q-pl-none" size="xs" flat dense name="drag_indicator" style="cursor: move" />
        <q-btn color="blue" flat dense round v-on:click="done" icon="done" size="sm" v-if="is_coretasklist">
          <q-tooltip :delay="550" anchor="top middle" self="center middle">Complete task</q-tooltip>
        </q-btn>
        <q-btn
          color="blue"
          flat
          dense
          round
          v-on:click="deleteTask"
          :icon="tasklistline.type == 'dailytask' || tasklistline.type == 'regulartask' ? 'playlist_remove' : 'delete'"
          size="sm"
        >
          <q-tooltip :delay="550" anchor="top middle" self="center middle">Delete task</q-tooltip>
        </q-btn>
      </div>
    </q-item-section>
    <q-item-section style="user-select: text">
      {{ tasklistlinetext }}
      <q-popup-edit buttons lazy-rule v-slot="scope" v-if="tasklistline.noedit != true" v-model="tasklistlinetext">
        <q-input v-model="scope.value" dense autofocus counter @keyup.enter="scope.set" />
      </q-popup-edit>
    </q-item-section>
  </q-item>
</template>

<script>
import { mapState } from "vuex";

export default {
  name: "TaskListLine",
  props: ["uid", "index", "is_coretasklist"],
  components: {},
  methods: {
    done: async function () {
      if (this.tasklistline.type == "dailytask") {
        await this.$store.dispatch("aDailytaskstateSet", {
          statedate: this.$store.state.current.date,
          taskstate: 1,
          dailytask: this.tasklistline.dailytask,
        });
      } else if (this.tasklistline.type == "regulartask") {
        await this.$store.dispatch("aRegulartaskDone", this.tasklistline.regulartask);
      } else if (this.tasklistline.text != "") {
        await this.$store.dispatch("aDaystateAddComplited", this.tasklistline.text);
      }
      await this.deleteTask();
    },
    deleteTask: async function () {
      await this.$store.dispatch("aTaskListDelItem", { uid: this.uid, index: this.index });
    },
  },
  computed: {
    tasklistlinetext: {
      get() {
        return this.$store.state.tasklist.lst[this.uid].jsondoc[this.index].text;
      },
      set(value) {
        this.$store.dispatch("aTasklistSetText", { uid: this.uid, index: this.index, text: value });
      },
    },
    ...mapState({
      tasklistline(state) {
        return state.tasklist.lst[this.uid].jsondoc[this.index];
      },
    }),
  },
};
</script>
