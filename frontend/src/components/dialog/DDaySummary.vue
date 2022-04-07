<template>
  <q-dialog ref="dialogRef" full-height full-width>
    <q-card class="q-dialog-plugin q-pa-md">
      <div class="text-right">
        <q-space />
        <q-btn icon="close" flat round dense v-close-popup />
      </div>
      <PlaningSummary :summary_date="summary_date" :hide_tasklist="true" />
    </q-card>
  </q-dialog>
</template>

<script>
import { useDialogPluginComponent } from "quasar";
import PlaningSummary from "@/views/PlaningSummary";

export default {
  name: "DDaySummary",
  created: async function () {},
  props: ["summary_date"],
  components: {
    PlaningSummary,
  },
  setup() {
    const { dialogRef, onDialogOK } = useDialogPluginComponent();
    return {
      dialogRef,
      onDialogOK,
    };
  },
};
</script>
