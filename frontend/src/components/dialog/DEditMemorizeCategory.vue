<template>
  <q-dialog ref="dialogEditRTRef" @hide="onDialogHide" full-height>
    <q-card class="column" style="width: 1000px; max-width: 80vw">
      <q-card-section>
        <div class="text-bold">Edit Memorize Card Category</div>
      </q-card-section>
      <q-separator />
      <q-card-section class="col row">
        <q-scroll-area class="col-12 scroll">
          <q-markup-table dense bordered class="text-left">
            <!--   Table header   -->
            <thead class="bg-indigo-3 text-center">
              <tr>
                <th>Actions</th>
                <th>Name</th>
                <th>Color</th>
                <th width="99%">Description</th>
              </tr>
            </thead>
            <tbody>
              <!--   Table content   -->
              <template v-for="t in category" :key="t">
                <tr>
                  <td>
                    <q-btn-group flat>
                      <q-btn dense flat round size="sm" icon="delete" color="red" @click="deleteCategory(t.uid)" />
                    </q-btn-group>
                  </td>
                  <td class="pointer">
                    {{ t.name }}
                    <q-popup-edit
                      buttons
                      lazy-rule
                      @save="(val) => setName(val, t.uid)"
                      v-slot="scope"
                      v-model="t.name"
                    >
                      <q-input v-model="scope.value" dense autofocus counter @keyup.enter="scope.set" />
                    </q-popup-edit>
                  </td>
                  <td>
                    <div class="color-box pointer" :style="'background-color: ' + t.hex">&nbsp;</div>
                    <q-popup-edit
                      buttons
                      lazy-rule
                      @save="(val) => setColor(val, t.uid)"
                      v-model="t.hex"
                      v-slot="scope"
                    >
                      <q-color
                        no-header-tabs
                        default-view="palette"
                        :default-value="'#' + t.color.toString(16).padStart(6, '0')"
                        v-model="scope.value"
                      />
                    </q-popup-edit>
                  </td>
                  <td class="pointer">
                    {{ t.description }}
                    <q-popup-edit
                      buttons
                      lazy-rule
                      @save="(val) => setDescription(val, t.uid)"
                      v-slot="scope"
                      v-model="t.description"
                    >
                      <q-input v-model="scope.value" dense autofocus counter @keyup.enter="scope.set" />
                    </q-popup-edit>
                  </td>
                </tr>
              </template>
            </tbody>
          </q-markup-table>
        </q-scroll-area>
      </q-card-section>
      <q-separator />
      <q-card-actions align="right" class="bg-white text-primary row">
        <!--   Button area   -->
        <q-space />
        <q-btn color="primary" no-caps label="Create category" @click="createCategory" icon="add" />
        <q-btn color="primary" no-caps label="Close" @click="onOKClick" />
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<script>
import { mapState } from "vuex";

export default {
  name: "DEditMemorizeStack",
  props: ["uid"],
  created: async function () {},
  emits: ["ok", "hide"],
  data: function () {
    return {};
  },
  components: {},
  methods: {
    show() {
      this.$refs.dialogEditRTRef.show();
    },
    hide() {
      this.$refs.dialogEditRTRef.hide();
    },
    onDialogHide() {},
    onOKClick() {
      this.$emit("ok");
      this.hide();
    },
    createCategory() {
      this.$store.dispatch("aMemorizeCategoryCreate");
    },
    deleteCategory(uid) {
      this.$store.dispatch("aMemorizeCategoryDelete", uid);
    },
    setName(val, uid) {
      this.$store.dispatch("aMemorizeCategoryUpdate", { uid, data: { name: val } });
    },
    setDescription(val, uid) {
      this.$store.dispatch("aMemorizeCategoryUpdate", { uid, data: { description: val } });
    },
    setColor(val, uid) {
      this.$store.dispatch("aMemorizeCategoryUpdate", { uid, data: { color: parseInt(val.substr(1, 6), 16) } });
    },
  },
  computed: mapState({
    category: (state) => state.memorize.category,
  }),
};
</script>
<style scoped>
.color-box {
  width: 40px;
  border-radius: 3px;
}
</style>
