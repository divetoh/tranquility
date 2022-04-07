<template>
  <q-dialog ref="dialogRef" persistent>
    <q-card class="q-pa-md q-gutter-md" style="width: 500px; max-width: 80vw">
      <div>
        <q-input outlined dense v-model="name" label="Task" stack-label />
      </div>
      <div>
        <q-input outlined dense v-model="period" label="Period" type="int" stack-label />
      </div>
      <div>
        <q-input outlined dense v-model="nextdate" label="Next date" type="date" stack-label />
      </div>
      <div>
        <q-checkbox outlined dense v-model="is_active" label="Active" stack-label />
      </div>
      <q-btn color="primary" label="Cancel" @click="onCancelClick" />
      <q-btn color="primary" label="Save" @click="onOKClick" />
    </q-card>
  </q-dialog>
</template>

<script>
export default {
  name: "DEditRegularTaskItem",
  props: ["uid"],
  emits: ["ok", "hide"],
  created: async function () {
    if (this.uid == null) {
      this.nextdate = this.$store.state.current.date;
      return;
    }
    this.create = false;
    this.name = this.$store.state.regulartask.lst[this.uid].name;
    this.is_active = this.$store.state.regulartask.lst[this.uid].is_active;
    this.period = this.$store.state.regulartask.lst[this.uid].period;
    this.nextdate = this.$store.state.regulartask.lst[this.uid].nextdate;
  },
  data: function () {
    return {
      array_id: undefined,
      create: true,
      name: "New task",
      period: 1,
      nextdate: "2022-01-01",
      is_active: true,
    };
  },
  methods: {
    show() {
      this.$refs.dialogRef.show();
    },
    hide() {
      this.$refs.dialogRef.hide();
    },
    onOKClick() {
      var data = {};
      if (this.create) {
        data.name = this.name;
        data.period = this.period;
        data.is_active = this.is_active;
        data.nextdate = this.nextdate;
        this.$store.dispatch("aRegulartaskCreate", data);
        this.$emit("ok");
        this.hide();
      } else {
        if (this.name != this.$store.state.regulartask.lst[this.uid].name) data.name = this.name;
        if (this.period != this.$store.state.regulartask.lst[this.uid].period) data.period = this.period;
        if (this.is_active != this.$store.state.regulartask.lst[this.uid].is_active) data.is_active = this.is_active;
        if (this.nextdate != this.$store.state.regulartask.lst[this.uid].nextdate) data.nextdate = this.nextdate;
        this.$store.dispatch("aRegulartaskUpdate", { uid: this.uid, data });
        this.$emit("ok");
        this.hide();
      }
    },
    onCancelClick() {
      this.hide();
    },
  },
};
</script>
