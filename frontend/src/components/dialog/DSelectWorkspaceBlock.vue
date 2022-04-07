<template>
  <q-dialog ref="dialogRef">
    <q-card class="column editor">
      <q-list bordered style="height: 600px; width: 400px">
        <q-item
          clickable
          v-ripple
          :active="item === 'coretasklist'"
          @click="item = 'coretasklist'"
          active-class="dialog-menu-link"
        >
          <q-item-section avatar>
            <q-avatar color="teal" text-color="white" icon="fact_check" />
          </q-item-section>

          <q-item-section>Core Tasklist</q-item-section>
        </q-item>

        <q-item
          clickable
          v-ripple
          :active="item === 'markdown'"
          @click="item = 'markdown'"
          active-class="dialog-menu-link"
        >
          <q-item-section avatar>
            <q-avatar color="teal" text-color="white" icon="article" />
          </q-item-section>

          <q-item-section>Markdown Article</q-item-section>
        </q-item>
      </q-list>
      <q-btn color="primary" label="OK" @click="onOKClick" />
    </q-card>
  </q-dialog>
</template>

<script>
import { useDialogPluginComponent } from "quasar";
import { debounce } from "lodash-es";

export default {
  name: "DSelectWorkspaceBlock",
  created: async function () {},
  data: function () {
    return {
      item: "coretasklist",
    };
  },
  methods: {
    update: debounce(function (e) {
      this.md = e.target.value;
    }, 100),
    onOKClick: function () {
      this.onDialogOK(this.item);
    },
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

<style>
.dialog-menu-link {
  color: white;
  background-color: #f2c037;
}
</style>
