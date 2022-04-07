<template>
  <q-item clickable dense class="q-gutter-xs">
    <q-item-section side>
      <div class="q-gutter-xs">
        <q-btn color="blue" flat dense round v-on:click="done" icon="done" size="sm">
          <q-tooltip :delay="550" anchor="top middle" self="center middle">Complete task</q-tooltip>
        </q-btn>
        <q-btn color="blue" flat dense round v-on:click="deltask" icon="delete" size="sm">
          <q-tooltip :delay="550" anchor="top middle" self="center middle">Delete task</q-tooltip>
        </q-btn>
      </div>
    </q-item-section>
    <q-item-section>
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
  props: ["uid", "index"],
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
      await this.deltask();
    },
    deltask: async function () {
      await this.$store.dispatch("aTaskListDelItem", { uid: this.uid, index: this.index });
    },
    edit: async function () {
      console.log(this.uid);
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
