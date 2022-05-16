<template>
  <div class="q-pa-md row">
    <!-- Cards by section Block -->
    <q-card class="col-4 q-pa-none">
      <q-card-section class="splash1">Cards by section</q-card-section>
      <q-card-section class="q-pa-none">
        <!-- Sections list -->
        <q-list v-if="!section">
          <q-item clickable v-for="c in sectionList" :key="c" @click="setSection(c)">
            <q-item-section>
              <q-item-label>{{ c }}</q-item-label>
            </q-item-section>
          </q-item>
        </q-list>
        <!-- Stack list -->
        <q-list v-else>
          <q-item clickable @click="setSection(undefined)" class="bg-blue-grey-2">
            <q-item-section>
              <q-item-label>{{ section }}</q-item-label>
            </q-item-section>
          </q-item>
          <q-item clickable v-for="s in stackList" :key="s">
            <q-item-section>
              <q-item-label @click="testStack(s)">{{ stack[s].name }}</q-item-label>
            </q-item-section>
          </q-item>
        </q-list>
      </q-card-section>
    </q-card>
  </div>
</template>

<script>
import { mapState } from "vuex";
import { Dialog } from "quasar";
import DMemorizeTest from "@/components/dialog/DMemorizeTest";

export default {
  name: "MemorizeLearn",
  data: function () {
    return {
      section: undefined,
    };
  },
  components: {},
  created: async function () {},
  methods: {
    async setSection(section) {
      this.section = section;
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
      });
    },
  },
  computed: mapState({
    stack: (state) => state.memorize.stack,
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
      var stack_list = [];
      for (var st in state.memorize.stack) {
        const stack = state.memorize.stack[st];
        if (!stack.is_active) continue;
        if (!stack_list.includes(stack.section)) stack_list.push(stack.section);
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
