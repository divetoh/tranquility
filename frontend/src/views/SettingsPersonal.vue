<template>
  <div class="q-pa-md row items-start q-gutter-md">
    <q-card bordered class="col-3">
      <q-card-section class="bg-primary text-white"> Personal Settings </q-card-section>
      <q-card-section class="q-gutter-y-md">
        <q-input
          outlined
          dense
          v-model="full_name"
          @update:model-value="full_name_changed = true"
          @change="update_full_name()"
          label="Full name"
          stack-label
        >
          <template v-slot:append v-if="full_name_changed">
            <q-btn icon="save" flat dense size="sm" @click="update_full_name" color="orange" />
          </template>
        </q-input>
        <q-btn color="primary" style="width: 100%" @click="set_password"> Set Password </q-btn>
      </q-card-section>
    </q-card>
  </div>
</template>

<script>
import { Dialog } from "quasar";

export default {
  name: "SettingsPersonal",
  data: function () {
    return {
      full_name: "",
      full_name_changed: false,
    };
  },
  components: {},
  created: async function () {
    this.full_name = this.$store.state.auth.userProfile.full_name;
  },
  methods: {
    update_full_name: async function () {
      this.$store.dispatch("aAuthSetFullname", this.full_name);
      this.full_name_changed = false;
    },
    set_password: async function () {
      Dialog.create({
        title: "Set password",
        message: "New password (minimum 6 characters).",
        prompt: {
          model: "",
          isValid: (val) => val.length > 5,
          type: "password",
        },
        cancel: true,
        persistent: true,
      }).onOk((data) => {
        this.$store.dispatch("aAuthSetPassword", data);
      });
    },
  },
};
</script>
