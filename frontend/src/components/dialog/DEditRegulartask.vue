<template>
  <q-dialog ref="dialogEditRTRef" full-height>
    <q-card class="column" style="width: 1000px; max-width: 80vw">
      <q-card-section>
        <div class="text-bold">Edit regular task list</div>
      </q-card-section>
      <q-separator />
      <q-card-section class="col row">
        <q-scroll-area class="col-12 scroll">
          <q-markup-table dense bordered class="text-left">
            <!--   Table header   -->
            <thead class="bg-indigo-3 text-center">
              <tr>
                <th>Actions</th>
                <th class="pointer_cursor" @click="set_sort('nextdate')">
                  Next Date
                  <q-icon :name="order == 1 ? 'arrow_drop_down' : 'arrow_drop_up'" v-if="sort == 'nextdate'" />
                </th>
                <th class="pointer_cursor" @click="set_sort('period')">
                  Period
                  <q-icon :name="order == 1 ? 'arrow_drop_down' : 'arrow_drop_up'" v-if="sort == 'period'" />
                </th>
                <th class="pointer_cursor" @click="set_sort('name')" width="99%">
                  Task name
                  <q-icon :name="order == 1 ? 'arrow_drop_down' : 'arrow_drop_up'" v-if="sort == 'name'" />
                </th>
              </tr>
            </thead>
            <tbody>
              <!--   Table content   -->
              <template v-for="t in sortedtasks" :key="t">
                <tr
                  :class="!regulartask[t].is_active ? 'qtable_inactive_row' : ''"
                  v-if="!this.hide_disabled || regulartask[t].is_active"
                >
                  <td>
                    <q-btn-group flat>
                      <q-btn dense flat round size="sm" icon="edit" @click="edit_regulartask(t)" />
                      <q-btn
                        dense
                        flat
                        round
                        size="sm"
                        icon="block"
                        @click="disable_regulartask(t)"
                        v-if="regulartask[t].is_active"
                      />
                      <q-btn
                        dense
                        flat
                        round
                        size="sm"
                        icon="add_circle_outline"
                        @click="enable_regulartask(t)"
                        v-else
                      />
                      <q-btn dense flat round size="sm" icon="delete" color="red" @click="delete_regulartask(t)" />
                    </q-btn-group>
                  </td>
                  <td>{{ regulartask[t].nextdate }}</td>
                  <td>{{ regulartask[t].period }}</td>
                  <td>{{ regulartask[t].name }}</td>
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
        <q-btn color="primary" no-caps label="Create task" @click="create_regulartask" icon="add" />
        <q-btn color="primary" no-caps label="Close" @click="onOKClick" />
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<script>
import { mapState } from "vuex";
import { Dialog } from "quasar";
import DEditRegularTaskItem from "@/components/dialog/DEditRegularTaskItem";

export default {
  name: "DEditRegulartask",
  created: async function () {},
  emits: ["ok", "hide"],
  data: function () {
    return {
      sort: "name",
      order: 1,
      hide_disabled: true,
    };
  },
  components: {},
  methods: {
    show() {
      this.$refs.dialogEditRTRef.show();
    },
    hide() {
      this.$refs.dialogEditRTRef.hide();
    },
    onOKClick() {
      this.$emit("ok");
      this.hide();
    },
    onCancelClick() {
      this.hide();
    },
    set_sort(newsort) {
      if (this.sort != newsort) {
        this.sort = newsort;
        this.order = 1;
      } else if (this.order == -1) {
        this.sort = "uid";
        this.order = 1;
      } else this.order = -1;
    },
    async edit_regulartask(uid) {
      Dialog.create({
        component: DEditRegularTaskItem,
        componentProps: {
          uid,
        },
      });
    },
    async enable_regulartask(uid) {
      this.$store.dispatch("aRegulartaskUpdate", { uid, data: { is_active: true } });
    },
    async disable_regulartask(uid) {
      this.$store.dispatch("aRegulartaskUpdate", { uid, data: { is_active: false } });
    },
    async delete_regulartask(uid) {
      Dialog.create({
        dark: true,
        title: "Confirm delete",
        message: `Would you like to delete regular task: ${this.regulartask[uid].name}?`,
        cancel: true,
        persistent: true,
      }).onOk(() => {
        this.$store.dispatch("aRegulartaskDelete", { uid });
      });
    },
    async create_regulartask() {
      Dialog.create({
        component: DEditRegularTaskItem,
      });
    },
  },
  computed: mapState({
    regulartask: (state) => state.regulartask.lst,
    sortedtasks: function (state) {
      var lst = state.regulartask.lst;
      const sort = this.sort;
      const order = this.order;
      return Object.keys(lst).sort(function (a, b) {
        if (lst[a][sort] < lst[b][sort]) return -1 * order;
        if (lst[a][sort] > lst[b][sort]) return 1 * order;
        return 0;
      });
    },
  }),
};
</script>
