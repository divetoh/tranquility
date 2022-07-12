<template>
  <q-dialog ref="dialogEditRTRef" @hide="onDialogHide" full-height>
    <q-card class="row no-wrap" style="width: 1600px; max-width: 80vw">
      <!--   Left area   -->
      <div class="side-section col-3 column" style="height: 100%">
        <q-list>
          <q-item dense clickable v-ripple @click="selectCard(undefined)" :active="!selected">
            <q-item-section>Stack info</q-item-section>
          </q-item>
        </q-list>
        <q-separator color="white" />

        <!-- Left area. Card list -->
        <q-list class="col-grow col-shrink scroll6" style="overflow: auto; width: 100%; flex: 1">
          <template v-for="c in stackcard" :key="c">
            <q-item :active="selected == c" @click="selectCard(card[c].uid)" clickable v-ripple dense>
              <q-item-section side>
                <div
                  :style="'display: block; width: 24px; background-color:' + categorys[card[c].category].hex"
                  v-if="card[c].category"
                >
                  &nbsp;
                </div>
                <div style="display: block; width: 24px; border: solid white 1px" v-else>&nbsp;</div>
              </q-item-section>
              <q-item-section>
                {{ card[c].name }}
              </q-item-section>
            </q-item>
          </template>
        </q-list>

        <div style="width: 100%">
          <q-btn-group round style="width: 100%" spread>
            <q-btn color="primary" no-caps icon="add" label="Add" @click="addCard" />
            <q-btn color="primary" no-caps icon="delete" label="Delete" @click="deleteCard" :disabled="!selected" />
          </q-btn-group>
        </div>
      </div>

      <!-- Right area -->
      <div class="main-section column col-shrink col-grow">
        <div class="col-grow col-shrink scroll6 no-wrap" style="overflow: auto; width: 100%; flex: 1">
          <!-- Right area. Stack edit mode -->
          <div class="column q-py-none" v-if="!selected">
            <div class="q-gutter-md row" style="flex: 0; width: 100%">
              <q-input class="col-grow q-mb-sm" dense outlined label="Name" v-model="stackName" maxlength="250" />
              <q-toggle v-model="stackActive" checked-icon="check" unchecked-icon="pause" />
            </div>
            <q-select
              dense
              outlined
              v-model="stackSection"
              use-input
              hide-selected
              fill-input
              new-value-mode="add"
              input-debounce="0"
              :options="stackList"
              @input-value="setSection"
              label="Stack Section"
              class="q-mb-sm"
            >
              <template v-slot:no-option>
                <q-item dense>
                  <q-item-section class="text-grey">No results</q-item-section>
                </q-item>
              </template>
            </q-select>
            <q-input dense outlined label="Description" v-model="stackDescription" maxlength="1024" autogrow />
          </div>

          <!-- Right area. Card edit mode -->
          <div class="column q-py-none no-wrap" style="height: 100%; flex: 1" v-if="selected">
            <!-- Right area. Card edit mode. Name, category, active -->
            <div class="q-gutter-md row" style="flex: 0; width: 100%">
              <q-input class="col-grow" dense outlined v-model="cardName" maxlength="200" label="Short name" />
              <q-select
                class="col-3 single-line-select"
                options-html
                dense
                outlined
                v-model="cardCategory"
                :options="categoryList"
                label="Category"
                map-options
                emit-value
              >
              </q-select>
              <q-toggle v-model="cardActive" checked-icon="check" unchecked-icon="pause" />
            </div>

            <!-- Right area. Card edit mode. Question section -->
            <div class="sect_separator bg-blue-2">
              <q-btn
                color="primary"
                class="q-pa-none q-ma-none"
                flat
                icon="expand_less"
                size="md"
                v-if="showQuestion"
                @click="showQuestion = false"
              />
              <q-btn
                color="primary"
                class="q-pa-none q-ma-none"
                flat
                icon="expand_more"
                size="md"
                v-else
                @click="showQuestion = true"
              />
              Card Obverse (Question)
            </div>
            <div class="bg-blue-2 row col-grow q-py-sm md-edit-section" v-if="showQuestion">
              <textarea class="input" :value="cardObverse" @input="updateQ"></textarea>
              <div class="output" v-html="outputQ"></div>
            </div>

            <!-- Right area. Card edit mode. Answer section -->
            <div class="sect_separator bg-green-2">
              <q-btn
                color="primary"
                class="q-pa-none q-ma-none"
                flat
                icon="expand_less"
                size="md"
                v-if="showAnswer"
                @click="showAnswer = false"
              />
              <q-btn
                color="primary"
                class="q-pa-none q-ma-none"
                flat
                icon="expand_more"
                size="md"
                v-else
                @click="showAnswer = true"
              />
              Card Reverse (Answer)
            </div>
            <div class="bg-green-2 row col-grow q-py-sm md-edit-section" v-if="showAnswer">
              <textarea class="input" :value="cardReverse" @input="updateA"></textarea>
              <div class="output" v-html="outputA"></div>
            </div>

            <!-- Right area. Card edit mode. Hint section -->
            <div class="sect_separator bg-orange-2">
              <q-btn
                color="primary"
                class="q-pa-none q-ma-none"
                flat
                icon="expand_less"
                size="md"
                v-if="showHint"
                @click="showHint = false"
              />
              <q-btn
                color="primary"
                class="q-pa-none q-ma-none"
                flat
                icon="expand_more"
                size="md"
                v-else
                @click="showHint = true"
              />
              Card Hint (optional)
            </div>
            <div class="row col-grow q-py-sm md-edit-section bg-orange-2" v-if="showHint">
              <textarea class="input" :value="cardHint" @input="updateH"></textarea>
              <div class="output" v-html="outputH"></div>
            </div>
          </div>
        </div>

        <!-- Right area. Bottom buttons -->
        <q-separator class="q-my-xs" />
        <div width="100%" class="row">
          <q-btn icon="info" color="primary" no-caps label="Markdown syntax" @click="showMarkdownSyntax" />
          <q-space />
          <q-btn color="primary" no-caps label="Close" @click="onOKClick" />
        </div>
      </div>
    </q-card>
  </q-dialog>
</template>

<script>
import { mapState } from "vuex";
import { debounce } from "lodash-es";
import marked from "marked";
import DHelpMarkdown from "@/components/dialog/DHelpMarkdown";

export default {
  name: "DEditMemorizeStack",
  props: ["uid"],
  emits: ["ok", "hide"],
  data: function () {
    return {
      selected: undefined,
      showQuestion: true,
      showAnswer: true,
      showHint: false,

      cardName: "",
      cardCategory: undefined,
      cardObverse: "",
      cardReverse: "",
      cardActive: true,
      cardHint: "",

      stackName: "",
      stackSection: "",
      stackDescription: "",
      stackActive: "",
    };
  },
  created: async function () {
    this.marked = marked;
    await this.$store.dispatch("aMemorizeCardLoadByStack", { stack: this.uid });
    this.stackName = this.$store.state.memorize.stack[this.uid].name;
    this.stackSection = this.$store.state.memorize.stack[this.uid].section;
    this.stackActive = this.$store.state.memorize.stack[this.uid].is_active;
    this.stackDescription = this.$store.state.memorize.stack[this.uid].description;
  },
  methods: {
    // Dialog
    show() {
      this.$refs.dialogEditRTRef.show();
    },
    hide() {
      this.$refs.dialogEditRTRef.hide();
    },
    async onDialogHide() {
      await this.saveStack();
      await this.saveCard();
    },
    onOKClick() {
      this.$emit("ok");
      this.hide();
    },
    showMarkdownSyntax() {
      this.$q.dialog({
        component: DHelpMarkdown,
      });
    },
    // Card methods
    updateQ: debounce(function (e) {
      this.cardObverse = e.target.value;
    }, 100),
    updateA: debounce(function (e) {
      this.cardReverse = e.target.value;
    }, 100),
    updateH: debounce(function (e) {
      this.cardHint = e.target.value;
    }, 100),
    async selectCard(uid) {
      // Save current changes, before switch item
      if (this.selected) await this.saveCard();
      else await this.saveStack();

      this.selected = uid;
      if (uid != undefined) {
        this.cardName = this.$store.state.memorize.card[uid].name;
        this.cardObverse = this.$store.state.memorize.card[uid].obverse;
        this.cardReverse = this.$store.state.memorize.card[uid].reverse;
        this.cardCategory = this.$store.state.memorize.card[uid].category;
        this.cardActive = this.$store.state.memorize.card[uid].is_active;
        this.cardHint = this.$store.state.memorize.card[uid].hint;
        if (this.cardHint == null) this.cardHint = "";
      }
    },
    async addCard() {
      const uid = await this.$store.dispatch("aMemorizeCardCreate", { stack: this.uid });
      await this.selectCard(uid);
    },
    async deleteCard() {
      if (this.selected != undefined) {
        this.$q
          .dialog({
            title: "Confirm",
            dark: true,
            message: "Confirm card delete?",
            cancel: true,
            persistent: true,
          })
          .onOk(() => {
            this.$store.dispatch("aMemorizeCardDelete", this.selected);
            this.selected = undefined;
          });
      }
    },
    async saveCard() {
      if (!this.selected) return;
      const old = this.$store.state.memorize.card[this.selected];
      var data = {};
      if (this.cardObverse != old.obverse) data.obverse = this.cardObverse;
      if (this.cardReverse != old.reverse) data.reverse = this.cardReverse;
      if (this.cardName != old.name) data.name = this.cardName;
      if (this.cardCategory != old.category) data.category = this.cardCategory;
      if (this.cardActive != old.is_active) data.is_active = this.cardActive;
      const hint = this.cardHint == "" ? null : this.cardHint;
      if (hint != old.hint) data.hint = hint;

      if (Object.keys(data).length > 0) {
        await this.$store.dispatch("aMemorizeCardUpdate", { uid: this.selected, data });
      }
    },
    // Stack methods
    async saveStack() {
      const old = this.$store.state.memorize.stack[this.uid];
      var data = {};
      if (this.stackName != old.name) data.name = this.stackName;
      if (this.stackSection != old.section) data.section = this.stackSection;
      if (this.stackDescription != old.description) data.description = this.stackDescription;
      if (this.stackActive != old.is_active) data.is_active = this.stackActive;
      if (Object.keys(data).length > 0) {
        this.$store.dispatch("aMemorizeStackUpdate", { uid: this.uid, data });
      }
    },
    setSection(val) {
      this.stackSection = val;
    },
  },
  computed: mapState({
    outputQ() {
      return marked(this.cardObverse);
    },
    outputA() {
      return marked(this.cardReverse);
    },
    outputH() {
      return marked(this.cardHint);
    },
    card: (state) => state.memorize.card,
    stackcard: function (state) {
      var cards = [];
      for (var i in state.memorize.card) {
        if (state.memorize.card[i].stack == this.uid) cards.push(i);
      }
      return cards;
    },
    stackList: function (state) {
      var stack_list = [];
      for (var st in state.memorize.stack) {
        const stack = state.memorize.stack[st];
        if (!stack_list.includes(stack.section)) stack_list.push(stack.section);
      }
      return stack_list;
    },
    categorys: function (state) {
      return state.memorize.category;
    },
    categoryList: function (state) {
      var category = [];
      for (var c in state.memorize.category) {
        const txt = state.memorize.category[c].name
          .replace(/&/g, "&amp;")
          .replace(/>/g, "&gt;")
          .replace(/</g, "&lt;")
          .replace(/"/g, "&quot;");
        category.push({
          label:
            "<span style='width: 40px; display: inline-block; background-color: " +
            state.memorize.category[c].hex +
            "'>&nbsp;</span>&nbsp;" +
            txt,
          value: state.memorize.category[c].uid,
        });
      }
      return category;
    },
  }),
};
</script>

<style scoped>
.output {
  overflow: auto;
  height: 100%;
  padding: 0px 5px;
  width: 50%;
  max-width: 50%;
}

.input {
  resize: none;
  width: 50%;
  height: 100%;
  float: left;
  max-width: 50%;
}

.q-card .side-section {
  border-radius: 0px;
  border-top-right-radius: 0px;
  border-bottom-right-radius: 0px;
  background-color: #172830;
  padding: 10px;
  color: white;
}

.main-section {
  padding: 10px;
  flex-grow: 1;
  flex-shrink: 1;
}

.side-section .q-item {
  padding: auto;
}

.side-section .q-item--active {
  background-color: #2c3e50;
  color: white;
}

.md-edit-section {
  width: 100%;
  max-width: 100%;
  min-height: 225px;
  padding: 0px 6px 6px 6px;
}

.sect_separator {
  margin-top: 6px;
  margin-right: 6px;
  width: 100%;
  border-top-left-radius: 5px;
  border-top-right-radius: 5px;
  padding: 0px 6px;
}

.single-line-select {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
</style>
