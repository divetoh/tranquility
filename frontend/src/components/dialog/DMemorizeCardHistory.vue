<template>
  <q-dialog ref="dialogRef">
    <q-card class="q-dialog-plugin q-pa-md scroll6 w400" style="max-height: 60vh">
      <div v-if="loading">Loading... <q-spinner-rings color="grey" size="md" /></div>
      <div v-else>
        Attempts: {{ h.attempts }}<br />
        Correct: {{ h.correct }}<br />
        Incorrect: {{ h.attempts - h.correct }}<br />
        <br />
        <q-markup-table flat>
          <thead>
            <tr>
              <th>Time</th>
              <th>State</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="st in h.history" :key="st">
              <td>{{ st[0].substr(0, 10) }}, {{ st[0].substr(11, 5) }}</td>
              <td>{{ st[1] }}</td>
            </tr>
          </tbody>
        </q-markup-table>
      </div>
    </q-card>
  </q-dialog>
</template>

<script>
import { useDialogPluginComponent } from "quasar";
import { api } from "@/api";

export default {
  name: "DMemorizeCardHistory",
  data: function () {
    return {
      loading: true,
    };
  },
  created: async function () {
    this.h = (await api.getMemorizeCardHistory(this.uid)).data;
    this.loading = false;
  },
  props: ["uid"],
  setup() {
    const { dialogRef, onDialogOK } = useDialogPluginComponent();
    return {
      dialogRef,
      onDialogOK,
    };
  },
};
</script>
