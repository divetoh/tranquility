<template>
  <q-dialog ref="dialogEditRTRef" @hide="onDialogHide" full-height>
    <q-card class="column" style="width: 1600px; max-width: 80vw">
      <q-card-section>
        <div class="text-bold">Memorize test</div>
      </q-card-section>
      <q-separator />
      <q-card-section class="col row">
        <q-scroll-area class="col scroll">
          <MemorizeCard
            v-for="card in cards"
            :key="card"
            :uid="card"
            ref="card"
            state="unanswered"
            :preview="preview"
            @correct="goodAnswer(card)"
            @incorrect="badAnswer(card)"
          />
          <template v-if="!hideUntimely">
            <MemorizeCard
              v-for="card in untimely"
              :key="card"
              :uid="card"
              state="unanswered"
              :preview="preview"
              @correct="goodAnswer(card)"
              @incorrect="badAnswer(card)"
            />
          </template>
          <MemorizeCard
            v-for="card in correct"
            :key="card"
            :uid="card"
            state="correct"
            :preview="preview"
            @correct="goodAnswer(card)"
            @incorrect="badAnswer(card)"
          />
          <MemorizeCard
            v-for="card in incorrect"
            :key="card"
            :uid="card"
            state="incorrect"
            :preview="preview"
            @correct="goodAnswer(card)"
            @incorrect="badAnswer(card)"
          />
        </q-scroll-area>
      </q-card-section>
      <q-separator />
      <q-card-actions align="right" class="bg-white text-primary row">
        <!--   Button area   -->
        <q-toggle v-model="preview" label="Question preview" />
        <q-toggle v-model="hideUntimely" label="Нide untimely" />
        <q-space />
        <q-btn color="primary" no-caps label="Close" @click="onOKClick" />
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<script>
import MemorizeCard from "@/components/items/MemorizeCard";

export default {
  name: "DMemorizeTest",
  props: ["test"],
  emits: ["ok", "hide"],
  data: function () {
    return {
      cards: [],
      correct: [],
      incorrect: [],
      untimely: [],
      preview: false,
      hideUntimely: true,
    };
  },
  components: {
    MemorizeCard,
  },
  created: async function () {
    const cur_date = this.$store.state.current.date;
    var all_cards = [];
    if (this.test.mode == "fullstack") {
      all_cards = await this.$store.dispatch("aMemorizeCardLoadByStack", { stack: this.test.stack });
    }
    if (this.test.mode == "fullcategory") {
      all_cards = await this.$store.dispatch("aMemorizeCardLoadByCategory", { category: this.test.category });
    }
    for (var i of all_cards) {
      const card = this.$store.state.memorize.card[i];
      if (card.is_active) {
        if (card.state_r[0] && card.state_r[0].nextdate > cur_date) this.untimely.push(i);
        else this.cards.push(i);
      }
    }
    // Simple shuffle
    this.cards.sort(() => Math.random() - 0.5);
    this.untimely.sort(() => Math.random() - 0.5);
  },
  methods: {
    // Dialog
    show() {
      this.$refs.dialogEditRTRef.show();
    },
    hide() {
      this.$refs.dialogEditRTRef.hide();
    },
    onDialogHide() {
      this.$emit("ok");
    },
    onOKClick() {
      this.$emit("ok");
      this.hide();
    },
    goodAnswer(uid) {
      const index = this.cards.indexOf(uid);
      if (index !== -1) this.cards.splice(index, 1);
      const index2 = this.untimely.indexOf(uid);
      if (index2 !== -1) this.untimely.splice(index2, 1);
      this.correct.push(uid);
      this.showNext(index);
    },
    badAnswer(uid) {
      const index = this.cards.indexOf(uid);
      if (index !== -1) this.cards.splice(index, 1);
      const index2 = this.untimely.indexOf(uid);
      if (index2 !== -1) this.untimely.splice(index2, 1);
      this.incorrect.push(uid);
      this.showNext(index);
    },
    showNext(index = 0) {
      if (this.cards.length == 0) return;
      if (index > this.cards.length - 1) index = this.cards.length - 1;
      const uid = this.cards[index];
      for (const c in this.$refs.card) {
        if (this.$refs.card[c].$props.uid == uid) this.$refs.card[c].show();
      }
    },
  },
};
</script>
