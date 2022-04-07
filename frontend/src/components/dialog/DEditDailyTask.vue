<template>
  <q-dialog ref="dialogEditDTRef" full-height>
    <q-card class="column" style="width: 1000px; max-width: 80vw">
      <q-card-section>
        <div class="text-bold">Edit daily task list</div>
      </q-card-section>
      <q-separator />
      <q-card-section class="col row">
        <q-scroll-area class="col-12 scroll">
          <q-markup-table dense bordered class="text-left">
            <!--   Table header   -->
            <thead class="bg-indigo-3 text-center">
              <tr>
                <th>Actions</th>
                <th width="99%">Task name</th>
              </tr>
            </thead>
            <tbody>
              <!--   Table content   -->
              <template v-for="t in sortedtasks" :key="t">
                <tr
                  :class="!dailytask[t].is_active ? 'qtable_inactive_row' : ''"
                  v-if="!this.hide_disabled || dailytask[t].is_active"
                >
                  <td>
                    <q-btn-group flat>
                      <q-btn
                        dense
                        flat
                        round
                        size="sm"
                        icon="block"
                        @click="disable_dailytask(t)"
                        v-if="dailytask[t].is_active"
                      />
                      <q-btn dense flat round size="sm" icon="add_circle_outline" @click="enable_dailytask(t)" v-else />
                      <q-btn dense flat round size="sm" icon="delete" color="red" @click="delete_dailytask(t)" />
                    </q-btn-group>
                  </td>
                  <td>{{ dailytask[t].name }}</td>
                </tr>
              </template>
            </tbody>
          </q-markup-table>
        </q-scroll-area>
      </q-card-section>
      <q-separator />
      <q-card-actions align="right" class="bg-white text-primary row">
        <!--   Button area   -->
        <q-toggle v-model="hide_disabled" label="Hide disabled" />
        <q-space />
        <q-btn color="primary" no-caps label="Create task" @click="create_dailytask" icon="add" />
        <q-btn color="primary" no-caps label="Close" @click="onOKClick" />
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<script>
import { mapState } from "vuex";
import { Dialog } from "quasar";

export default {
  name: "DEditDailyTask",
  created: async function () {},
  emits: ["ok", "hide"],
  data: function () {
    return {
      hide_disabled: true,
    };
  },
  components: {},
  methods: {
    show() {
      this.$refs.dialogEditDTRef.show();
    },
    hide() {
      this.$refs.dialogEditDTRef.hide();
    },
    onOKClick() {
      this.$emit("ok");
      this.hide();
    },
    onCancelClick() {
      this.hide();
    },
    async edit_dailytask() {},
    async enable_dailytask(uid) {
      this.$store.dispatch("aDailytaskUpdate", { uid, data: { is_active: true } });
    },
    async disable_dailytask(uid) {
      this.$store.dispatch("aDailytaskUpdate", { uid, data: { is_active: false } });
    },
    async delete_dailytask(uid) {
      Dialog.create({
        dark: true,
        title: "Confirm delete",
        message: `Would you like to delete daily task: ${this.dailytask[uid].name}?`,
        cancel: true,
        persistent: true,
      }).onOk(() => {
        this.$store.dispatch("aDailytaskDelete", { uid });
      });
    },
    async create_dailytask() {
      Dialog.create({
        title: "Create daily task",
        message: "New daily task name:",
        prompt: {
          model: "",
          isValid: (val) => val.length > 3,
        },
        cancel: true,
        persistent: true,
      }).onOk((data) => {
        this.$store.dispatch("aDailytaskCreate", { name: data, is_active: true });
      });
    },
  },
  computed: mapState({
    dailytask: (state) => state.dailytask.lst,
    sortedtasks: function (state) {
      var lst = state.dailytask.lst;
      return Object.keys(lst).sort(function (a, b) {
        if (lst[a].name < lst[b].name) return -1;
        if (lst[a].name > lst[b].name) return 1;
        return 0;
      });
    },
  }),
};
</script>
