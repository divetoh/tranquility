<template>
  <div class="q-pa-md row items-start q-gutter-md">
    <q-card bordered class="w400">
      <q-card-section class="bg-primary text-white"> Personal Settings </q-card-section>
      <q-card-section class="q-gutter-y-md">
        <q-input
          outlined
          dense
          v-model="full_name"
          @update:model-value="full_name_changed = true"
          @change="updateFullName()"
          label="Full name"
          stack-label
        >
          <template v-slot:append v-if="full_name_changed">
            <q-btn icon="save" flat dense size="sm" @click="updateFullName" color="orange" />
          </template>
        </q-input>
        <q-btn color="primary" style="width: 100%" @click="setPassword"> Set Password </q-btn>
      </q-card-section>
    </q-card>
    <q-card bordered class="w400">
      <q-card-section class="bg-primary text-white"> Download Archive </q-card-section>
      <q-card-section class="q-gutter-y-md">
        <q-btn color="primary" style="width: 100%" @click="downloadJSON" :loading="json_loading">
          JSON
          <template v-slot:loading> Loading... <q-spinner-rings color="grey" size="md" /> </template>
        </q-btn>
      </q-card-section>
    </q-card>
  </div>
</template>

<script>
import { Dialog } from "quasar";
import { api } from "@/api";
export default {
  name: "SettingsPersonal",
  data: function () {
    return {
      full_name: "",
      full_name_changed: false,
      json_loading: false,
    };
  },
  components: {},
  created: async function () {
    this.full_name = this.$store.state.auth.userProfile.full_name;
  },
  methods: {
    downloadJSON: async function () {
      this.json_loading = true;
      var response = await api.getArchiveJSON();
      var fileLink = document.createElement("a");
      fileLink.href = window.URL.createObjectURL(new Blob([response.data]));
      fileLink.setAttribute("download", "archive.json");
      document.body.appendChild(fileLink);
      fileLink.click();
      document.body.removeChild(fileLink);
      this.json_loading = false;
    },
    updateFullName: async function () {
      this.$store.dispatch("aAuthSetFullname", this.full_name);
      this.full_name_changed = false;
    },
    setPassword: async function () {
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
