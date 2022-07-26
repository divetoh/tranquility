<template>
  <div clickable dense class="memorize_card row" @click="showCard = true">
    <div class="card_content_wrapper" :class="state">
      <div>
        <template v-if="cardState">
          <q-badge class="q-px-xs q-ma-xs" @click.stop="showHistory">
            {{ cardState.state }}
            <q-tooltip :offset="[10, 10]" class="text-body2">
              Right answers count: {{ cardState.state }} <br />
              Last answer date: {{ cardState.lastdate }} <br />
              Next recomended date: {{ cardState.nextdate }} <br /><br />
              Click to show history...
            </q-tooltip>
          </q-badge>
          <q-badge
            class="q-px-xs q-ma-xs"
            v-if="cardState.nextdate > currentDate && state == 'unanswered'"
            color="green"
          >
            It's not time yet
          </q-badge>
        </template>
        <q-badge v-else class="q-px-xs q-ma-xs" color="grey">
          &dash;
          <q-tooltip :offset="[10, 10]" class="text-body2"> Not yet answered. </q-tooltip>
        </q-badge>
      </div>
      <div class="triangle" :style="'border-top-color: ' + cardHex" v-if="cardHex">
        <q-tooltip :offset="[10, 10]" class="text-body2">
          {{ cardCategory }}
        </q-tooltip>
      </div>
      <div class="card_content_preview_wrapper scroll6" v-if="preview || state != 'unanswered'">
        <div class="card_content no-wrap" v-html="cardObverse" />
      </div>
    </div>
  </div>

  <!-- Large Card -->
  <q-dialog v-model="showCard" class="q-my-xl">
    <q-card class="column card_large" v-if="!reverse">
      <q-card-section class="column card_content_large scroll6">
        <div class="output" v-html="cardObverse" />
      </q-card-section>
      <q-card-actions width="100%" class="text-primary column">
        <q-btn-group flat spread width="100%" class="full-width">
          <q-btn flat icon="view_module" v-close-popup />
          <q-btn flat icon="360" @click="reverse = true" />
          <q-btn flat icon="help_outline" :disabled="!cardHint" @click="showHint = true" />
        </q-btn-group>
      </q-card-actions>
    </q-card>

    <q-card class="column card_large_reverse" v-else>
      <q-card-section class="column card_content_large_reverse no-wrap scroll6">
        <div class="output no-wrap" v-html="cardReverse" />
      </q-card-section>
      <q-card-actions align="right" class="text-primary column">
        <q-btn-group flat spread width="100%" class="full-width">
          <q-btn flat icon="thumb_down_off_alt" @click="badAnswer" :disabled="state != 'unanswered'" />
          <q-btn flat icon="360" @click="reverse = false" />
          <q-btn flat icon="thumb_up_off_alt" @click="goodAnswer" :disabled="state != 'unanswered'" />
        </q-btn-group>
      </q-card-actions>
    </q-card>
  </q-dialog>

  <!-- Hint text -->
  <q-dialog v-model="showHint" class="q-my-xl">
    <q-card class="column hintbox">
      <div v-html="cardHint" />
    </q-card>
  </q-dialog>
</template>

<script>
import { mapState } from "vuex";
import { Dialog } from "quasar";
import DMemorizeCardHistory from "@/components/dialog/DMemorizeCardHistory";
import marked from "marked";

export default {
  name: "MemorizeLearn",
  expose: ["show", "uid"],
  data: function () {
    return {
      showCard: false,
      section: undefined,
      reverse: false,
      showHint: false,
    };
  },
  emits: ["correct", "incorrect", "skip"],
  props: ["state", "preview", "uid"],
  components: {},
  created: async function () {},
  methods: {
    async goodAnswer() {
      this.showCard = false;
      this.$store.dispatch("aMemorizeCardAnswer", { uid: this.uid, state: 1 });
      this.$emit("correct");
    },
    async badAnswer() {
      this.showCard = false;
      this.$store.dispatch("aMemorizeCardAnswer", { uid: this.uid, state: 0 });
      this.$emit("incorrect");
    },
    async setSection(section) {
      this.section = section;
    },
    async showHistory() {
      Dialog.create({
        component: DMemorizeCardHistory,
        componentProps: {
          uid: this.uid,
        },
      });
    },
    show() {
      this.showCard = true;
    },
  },
  computed: mapState({
    cardObverse: function (state) {
      return marked(state.memorize.card[this.uid].obverse);
    },
    cardReverse: function (state) {
      return marked(state.memorize.card[this.uid].reverse);
    },
    cardHex: function (state) {
      if (!state.memorize.card[this.uid].category) return undefined;
      return state.memorize.category[state.memorize.card[this.uid].category].hex;
    },
    cardHint: function (state) {
      if (state.memorize.card[this.uid].hint == null) return undefined;
      return marked(state.memorize.card[this.uid].hint);
    },
    cardCategory: function (state) {
      return state.memorize.category[state.memorize.card[this.uid].category].name;
    },
    cardState: function (state) {
      return state.memorize.card[this.uid].state_r[0];
    },
    currentDate: function (state) {
      return state.current.date;
    },
  }),
};
</script>

<style scoped>
.memorize_card {
  width: 200px;
  height: 300px;
  display: inline-block;
  margin: 5px;
  border-radius: 8px;
  cursor: pointer;
  overflow: hidden;
  background: url("../../assets/card_side1.png");
  border: solid 1px #b7c3cd;
  box-shadow: 1px 1px 4px #b7c3cd;
}

.correct:after {
  content: " ";
  z-index: 10;
  display: block;
  position: absolute;
  height: 100%;
  top: 0;
  left: 0;
  right: 0;
  background: rgba(0, 100, 0, 0.2);
  pointer-events: none;
}

.incorrect:after {
  content: " ";
  z-index: 10;
  display: block;
  position: absolute;
  height: 100%;
  top: 0;
  left: 0;
  right: 0;
  background: rgba(100, 0, 0, 0.2);
  pointer-events: none;
}

.card_large {
  padding: 15px 15px;
  background: url("../../assets/card_side1.png");
  height: 85vh;
  width: calc(85vh * 2 / 3);
  overflow: auto;
}

.hintbox {
  padding: 15px 15px;
  height: 75vh;
  width: 75vh;
  max-width: 90vw;
  overflow: auto;
}

.card_large_reverse {
  padding: 15px 15px;
  background: url("../../assets/card_side2.png");
  color: #eee;
  height: 85vh;
  width: calc(85vh * 2 / 3);
  overflow: auto;
}

.card_content_large {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-grow: 1;
  overflow: auto;
  padding: 5px 5px;
  background-color: #ffffff60;
  max-width: 100%;
}

.card_content_large_reverse {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-grow: 1;
  overflow: auto;
  padding: 5px 5px;
  background-color: #00000060;
  max-width: 100%;
}

.triangle {
  width: 0;
  height: 0;
  position: absolute;
  right: 0;
  top: 0;
  border-top-style: solid;
  border-top-width: 20px;
  border-left: 20px solid transparent;
}

.card_content_wrapper {
  position: relative;
  padding: 5px;
  height: 100%;
  width: 100%;
}

.card_content_preview_wrapper {
  overflow: auto;
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  max-width: 100%;
  flex-grow: 1;
  background-color: #ffffff60;
}

.card_content {
  padding: 5px 5px;
  font-size: 90%;
  max-width: 100%;
  max-height: 100%;
}

.output {
  max-width: 100%;
  max-height: 100%;
}
</style>
