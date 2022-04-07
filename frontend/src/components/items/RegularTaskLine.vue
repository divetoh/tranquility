<template>
  <q-item clickable dense class="q-gutter-xs">
    <q-item-section side>
      <div class="q-gutter-xs">
        <q-btn color="blue" flat dense round v-on:click="add" icon="playlist_add" size="sm">
          <q-tooltip :delay="550" anchor="top middle" self="center middle">Add to task List</q-tooltip>
        </q-btn>
        <q-btn color="blue" flat dense round v-on:click="done" icon="done" size="sm">
          <q-tooltip :delay="550" anchor="top middle" self="center middle">Complete task</q-tooltip>
        </q-btn>
      </div>
    </q-item-section>
    <q-item-section>
      {{ regulartask.name }}
    </q-item-section>
  </q-item>
</template>

<script>
import { mapState } from "vuex";

export default {
  name: "RegularTaskLine",
  props: ["uid"],
  components: {},
  methods: {
    done: async function () {
      await this.$store.dispatch("aRegulartaskDone", this.uid);
      await this.$store.dispatch("aTaskListRemoveRegularTask", {
        uid: this.$store.state.auth.userProfile.coretasklist,
        regulartask: this.uid,
      });
    },
    add: async function () {
      await this.$store.dispatch("aTaskListAddItem", {
        uid: this.$store.state.auth.userProfile.coretasklist,
        item: {
          text: this.$store.state.regulartask.lst[this.uid].name,
          regulartask: this.uid,
          type: "regulartask",
          noedit: true,
        },
      });
    },
  },
  computed: mapState({
    regulartask(state) {
      return state.regulartask.lst[this.uid];
    },
  }),
};
</script>
