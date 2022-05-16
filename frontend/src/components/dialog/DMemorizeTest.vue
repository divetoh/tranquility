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
            state="unanswered"
            :preview="preview"
            @correct="goodAnswer(card)"
            @incorrect="badAnswer(card)"
          />
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
      preview: false,
    };
  },
  components: {
    MemorizeCard,
  },
  created: async function () {
    if (this.test.mode == "fullstack") {
      const all_cards = await this.$store.dispatch("aMemorizeCardLoadByStack", { stack: this.test.stack });
      for (var i of all_cards) {
        if (this.$store.state.memorize.card[i].is_active) this.cards.push(i);
      }
      this.cards.sort(() => Math.random() - 0.5); // Simple shuffle
    }
  },
  methods: {
    // Dialog
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
    goodAnswer(uid) {
      const index = this.cards.indexOf(uid);
      if (index !== -1) {
        this.cards.splice(index, 1);
        this.correct.push(uid);
      }
    },
    badAnswer(uid) {
      const index = this.cards.indexOf(uid);
      if (index !== -1) {
        this.cards.splice(index, 1);
        this.incorrect.push(uid);
      }
    },
  },
};
</script>
