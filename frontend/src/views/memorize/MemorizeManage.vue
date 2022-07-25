<template>
  <div class="column" style="height: 100%; owerflow: auto">
    <q-card class="q-pa-md">
      <div style="text-align: left">
        <q-markup-table dense bordered class="text-left">
          <thead class="bg-indigo-3">
            <tr>
              <th>Actions</th>
              <th>Name</th>
              <th width="90%">Description</th>
            </tr>
          </thead>
          <tbody>
            <template v-for="(cat, index) in stackBySection" :key="cat">
              <tr class="bg-grey-3 text-grey-6">
                <td colspan="3">
                  <b>{{ index }}</b>
                </td>
              </tr>
              <tr v-for="st in cat" :key="st">
                <td>
                  <q-btn-group dense flat>
                    <q-btn dense size="sm" icon="edit" @click="editStack(st)" />
                    <q-btn dense size="sm" icon="delete" @click="deleteStack(st)" />
                  </q-btn-group>
                </td>
                <td>{{ stack[st].name }}</td>
                <td>{{ stack[st].description }}</td>
              </tr>
            </template>
          </tbody>
        </q-markup-table>
        <q-btn-group class="q-mx-md bg-grey-3">
          <q-btn icon="add" label="Add" no-caps class="q-px-md" @click="addStack" size="md" dense />
          <q-btn icon="class" label="Edit category" no-caps class="q-px-md" @click="editCategory" size="md" dense />
        </q-btn-group>
      </div>
    </q-card>
  </div>
</template>

<script>
import { Dialog } from "quasar";
import { mapState } from "vuex";
import DEditMemorizeStack from "@/components/dialog/DEditMemorizeStack";
import DEditMemorizeCategory from "@/components/dialog/DEditMemorizeCategory";
export default {
  name: "MemorizeManage",
  components: {},
  created: async function () {},
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
  methods: {
    async editStack(uid) {
      Dialog.create({
        component: DEditMemorizeStack,
        componentProps: {
          uid,
        },
      });
    },
    async deleteStack(uid) {
      this.$q
        .dialog({
          title: "Confirm",
          dark: true,
          message: "Confirm stack delete?",
          options: {
            type: "checkbox",
            model: [],
            items: [{ label: "Sure? All cards will be deleted.", value: "delmd" }],
          },
          cancel: true,
          persistent: true,
        })
        .onOk((data) => {
          if (data[0] == "delmd") this.$store.dispatch("aMemorizeStackDelete", uid);
        });
    },
    async addStack() {
      var uid = await this.$store.dispatch("aMemorizeStackCreate");
      await this.editStack(uid);
    },
    async editCategory() {
      Dialog.create({ component: DEditMemorizeCategory });
    },
  },
};
</script>
