<template>
  <q-card class="q-mb-sm q-pa-none">
    <q-card-section class="text-center" v-if="tasklist === undefined">
      Loading... <q-spinner-rings color="grey" size="md" />
    </q-card-section>
    <template v-else>
      <q-bar dense class="bg-white hover_ctrl q-pa-none">
        <div class="drag_handler q-space" style="text-align: left; font-weight: bold">TaskList</div>
        <q-btn flat dense round color="orange" v-on:click="save" icon="save" size="xs" v-if="tasklist.saved === false">
          <q-tooltip :delay="550" anchor="top middle" self="center middle"> Save list </q-tooltip>
        </q-btn>
        <q-btn dense flat v-on:click="$emit('delBlock')" icon="delete" size="xs" v-if="actions.delblock === true">
          <q-tooltip :delay="550" anchor="top middle" self="center middle"> Delete block </q-tooltip>
        </q-btn>
      </q-bar>
      <q-card-section class="text-left q-pt-none q-xa-sm">
        <q-list dense padding>
          <TaskListLine
            v-for="(name, index) in tasklist.jsondoc"
            :uid="tluid"
            :index="index"
            :key="index"
          ></TaskListLine>
        </q-list>
        <div class="q-gutter-xs">
          <q-btn color="blue" v-on:click="add(1)" size="sm">+1 </q-btn>
          <q-btn color="blue" v-on:click="add(4)" size="sm">+4 </q-btn>
          <q-btn color="blue" v-on:click="add(8)" size="sm">+8 </q-btn>
        </div>
      </q-card-section>
    </template>
  </q-card>
</template>

<script>
import { mapState } from "vuex";
import TaskListLine from "@/components/items/TaskListLine";

export default {
  name: "TaskList",
  props: ["uid", "actions"],
  emits: ["delBlock"],
  data() {
    return {
      tluid: this.uid,
    };
  },
  created: async function () {
    if (this.tluid === undefined) this.tluid = this.$store.state.auth.userProfile.coretasklist;
    if (this.$store.state.tasklist.lst[this.tluid] === undefined) {
      await this.$store.dispatch("aTasklistLoad", this.tluid);
    }
  },
  components: {
    TaskListLine,
  },
  computed: mapState({
    tasklist: function (state) {
      return state.tasklist.lst[this.tluid];
    },
  }),
  methods: {
    async add(count) {
      await this.$store.dispatch("aTasklistAddRows", {
        uid: this.tluid,
        count,
      });
    },
    async save() {
      await this.$store.dispatch("aTasklistSave", this.tluid);
    },
  },
};
</script>
