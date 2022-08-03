<template>
  <div class="q-pa-md q-gutter-md row">
    <!-- Cards by section Block -->
    <q-card class="col-xs-10 col-sm-6 col-md-4 q-pa-none">
      <q-card-section class="splash1">Cards by section</q-card-section>
      <q-card-section class="q-pa-none">
        <!-- Sections list -->
        <q-list v-if="!section" dense>
          <q-item v-for="(c, r) in sectionList" :key="r">
            <q-btn dense flat no-caps class="full-width" @click="setSection(r)">
              <q-item-section avatar>
                <q-icon name="folder" />
              </q-item-section>
              <q-item-section align="left">
                <q-item-label>
                  {{ r }}
                  <q-badge outline align="middle" :color="c > 0 ? 'primary' : 'grey'" v-if="c !== null">
                    {{ c }}
                  </q-badge>
                </q-item-label>
              </q-item-section>
            </q-btn>
          </q-item>
        </q-list>
        <!-- Stack list -->
        <q-list v-else dense>
          <q-item class="bg-blue-grey-2">
            <q-btn dense flat no-caps class="full-width" @click="setSection(undefined)">
              <q-item-section avatar>
                <q-icon name="reply" />
              </q-item-section>
              <q-item-section align="left">
                <q-item-label>.. ({{ section }})</q-item-label>
              </q-item-section>
            </q-btn>
          </q-item>

          <q-item v-for="s in stackList" :key="s">
            <q-btn dense flat no-caps class="full-width" @click="testStack(s)">
              <q-item-section avatar>
                <q-icon name="note" />
              </q-item-section>
              <q-item-section align="left">
                <q-item-label>
                  {{ stack[s].name }}
                  <q-badge
                    outline
                    align="middle"
                    :color="ready[s].ready > 0 ? 'primary' : 'grey'"
                    v-if="ready[s] !== undefined"
                  >
                    {{ ready[s].ready }}
                  </q-badge>
                </q-item-label>
              </q-item-section>
            </q-btn>
          </q-item>
        </q-list>
      </q-card-section>
    </q-card>
    <!-- Cards by category -->
    <q-card class="col-xs-10 col-sm-6 col-md-4 q-pa-none">
      <q-card-section class="splash1">Cards by category</q-card-section>
      <q-card-section class="q-pa-none">
        <!-- Category list -->
        <q-list dense>
          <q-item v-for="(c, r) in category" :key="r">
            <q-btn dense flat no-caps class="full-width" @click="testCategory(r)">
              <q-item-section avatar>
                <q-icon name="note" :style="'color:' + c.hex" />
              </q-item-section>
              <q-item-section align="left">
                <q-item-label>
                  {{ c.name }}
                  <q-badge
                    outline
                    align="middle"
                    :color="ready_cat[r].ready > 0 ? 'primary' : 'grey'"
                    v-if="ready_cat[r]"
                  >
                    {{ ready_cat[r].ready }}
                  </q-badge>
                </q-item-label>
              </q-item-section>
            </q-btn>
          </q-item>
        </q-list>
      </q-card-section>
    </q-card>
  </div>
</template>

<script>
import { mapState } from "vuex";
import { Dialog } from "quasar";
import { api } from "@/api";
import DMemorizeTest from "@/components/dialog/DMemorizeTest";

export default {
  name: "MemorizeLearn",
  data: function () {
    return {
      section: undefined,
      ready: {},
      ready_cat: {},
    };
  },
  components: {},
  created: async function () {
    await this.updateCounters();
  },
  methods: {
    async setSection(section) {
      this.section = section;
    },
    async updateCounters() {
      this.ready = (await api.getMemorizeStackReadyCount(this.$store.state.current.date)).data;
      this.ready_cat = (await api.memorize_category.ready_count(this.$store.state.current.date)).data;
    },
    async testStack(stack) {
      Dialog.create({
        component: DMemorizeTest,
        componentProps: {
          test: {
            mode: "fullstack",
            stack,
          },
        },
      }).onOk(() => {
        this.updateCounters();
      });
    },
    async testCategory(category) {
      Dialog.create({
        component: DMemorizeTest,
        componentProps: {
          test: {
            mode: "fullcategory",
            category,
          },
        },
      }).onOk(() => {
        this.updateCounters();
      });
    },
  },
  computed: mapState({
    stack: (state) => state.memorize.stack,
    category: (state) => state.memorize.category,
    stackList: function (state) {
      var stacks = [];
      for (var st in state.memorize.stack) {
        const stack = state.memorize.stack[st];
        if (!stack.is_active) continue;
        if (stack.section == this.section) stacks.push(st);
      }
      return stacks;
    },
    sectionList: function (state) {
      var stack_list = {};
      for (var st in state.memorize.stack) {
        const stack = state.memorize.stack[st];
        if (!stack.is_active) continue;
        if (stack_list[stack.section] == undefined) stack_list[stack.section] = null;
        if (this.ready[st] != undefined) stack_list[stack.section] += this.ready[st].ready;
      }
      return stack_list;
    },
  }),
};
</script>

<style scoped>
.splash1 {
  background-image: url(../../assets/splash1.jpg);
  padding: 50px 20px;
  color: #ffffff;
  font-size: 180%;
  text-shadow: #171830 0 0 3px;
}
</style>
