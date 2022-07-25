<template>
  <q-card-section class="text-center" v-if="loading">
    Loading... <q-spinner-rings color="grey" size="md" />
  </q-card-section>
  <div class="column" style="height: 100%; owerflow: auto" v-else>
    <q-card class="q-pa-md">
      <div style="text-align: left">
        <q-markup-table dense bordered class="text-left">
          <thead class="bg-indigo-3">
            <tr>
              <th rowspan="2">Section</th>
              <th rowspan="2">Name</th>
              <th rowspan="2">Cards</th>
              <th rowspan="2">Unanswered</th>
              <th colspan="10" align="center">Number of cards by continuous correct answers</th>
            </tr>
            <tr>
              <th class="bl" v-for="i in 9" :key="i">{{ i - 1 }}</th>
              <th class="bl">more</th>
            </tr>
          </thead>
          <tbody>
            <template v-for="stack in stat" :key="stack">
              <tr>
                <td>{{ stack.section }}</td>
                <td>{{ stack.name }}</td>
                <td>{{ stack.count }}</td>
                <td>{{ stack.unanswered }}</td>
                <td class="bl" v-for="(val, idx) in stack.correct" :key="idx">
                  <span v-if="val == 0">&nbsp;</span>
                  <span v-else>{{ val }}</span>
                </td>
              </tr>
            </template>
          </tbody>
        </q-markup-table>
      </div>
    </q-card>
  </div>
</template>

<script>
import { api } from "@/api";
// import { Dialog } from "quasar";
import { mapState } from "vuex";
export default {
  name: "MemorizeManage",
  components: {},
  created: async function () {
    const stat = await api.getMemorizeStackStatistics();
    this.stat = stat.data;
    this.loading = false;
  },
  data: function () {
    return {
      loading: true,
    };
  },
  computed: mapState({
    stackBySection: function (state) {
      var stack_order = {};
      for (var st in state.memorize.stack) {
        const stack = state.memorize.stack[st];
        if (!stack_order[stack.section]) stack_order[stack.section] = [];
        stack_order[stack.section].push(stack.uid);
      }
      return stack_order;
    },
    stack: (state) => state.memorize.stack,
  }),
  methods: {},
};
</script>

<style scoped>
.bl {
  border-left: 1px solid rgba(0, 0, 0, 0.12);
}
</style>
