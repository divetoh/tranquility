<template>
  <q-page class="home-page window-height row justify-center items-center">
    <q-card bordered class="w400 mh300">
      <q-tabs v-model="mode" align="justify" class="text-black" indicator-color="primary" dense v-if="demoMode == 1">
        <q-tab name="demomode" label="Demo mode" />
        <q-tab name="signin" label="Sign in" />
      </q-tabs>
      <q-separator />
      <q-tab-panels v-model="mode" animated>
        <q-tab-panel name="signin" class="q-gutter-y-md row justify-center q-pa-md q-px-xl">
          <q-form @submit="submit" class="q-gutter-md full-width">
            <q-input v-model="email" label="e-mail" class="full-width" />
            <q-input type="password" v-model="password" label="Password" class="full-width" />
            <br />
            <div>
              <q-btn label="Submit" type="submit" color="primary" />
            </div>
          </q-form>
        </q-tab-panel>
        <q-tab-panel name="demomode" class="q-gutter-y-md row justify-center q-pa-md">
          <div class="text-left">
            <h2>Wellcome to tranquility</h2>
            <br />
            <p>User account will be automatically deleted after one hour.</p>
            <p>
              Source Code: <a href="https://github.com/divetoh/tranquility">https://github.com/divetoh/tranquility</a>
            </p>
          </div>
          <q-btn color="primary" style="width: 100%" @click="generateAccount" :loading="awaitAccount">
            Create demo account
            <template v-slot:loading>Creating... <q-spinner-rings color="white" size="md" /> </template>
          </q-btn>
          <div class="text-red" v-if="message != ''">
            {{ message }}
          </div>
        </q-tab-panel>
      </q-tab-panels>
    </q-card>
  </q-page>
</template>

<script>
import { mapState } from "vuex";
import { demoMode } from "@/env";
import { api } from "@/api";

export default {
  name: "Login",
  data() {
    return {
      mode: demoMode == 1 ? "demomode" : "signin",
      email: "",
      password: "",
      awaitAccount: false,
      message: "",
    };
  },
  methods: {
    async submit() {
      this.$store.dispatch("aLogIn", {
        username: this.email,
        password: this.password,
      }).auth;
    },
    async generateAccount() {
      this.awaitAccount = true;
      this.message = "";
      try {
        const response = await api.createDemoAccount();
        var token = response.data.access_token;
      } catch (err) {
        if (err.response && err.response.data.detail) this.message = err.response.data.detail;
        else this.message = "Somthing going wrong, try again later.";
        this.awaitAccount = false;
        return;
      }
      if (token) {
        this.$store.dispatch("aLogIn", { token });
      } else {
        this.message = "Somthing going wrong, try again later.";
        this.awaitAccount = false;
      }
    },
  },
  computed: mapState({
    loginError: (state) => state.auth.logInError,
    demoMode: () => {
      return demoMode;
    },
  }),
};
</script>

<style></style>
