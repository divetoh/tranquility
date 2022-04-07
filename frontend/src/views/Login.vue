<template>
  <q-page class="home-page window-height row justify-center items-center">
    <q-card class="row justify-center q-pa-md q-px-xl">
      <q-form @submit="submit" class="q-gutter-md">
        <q-input v-model="email" label="e-mail" />

        <q-input type="password" v-model="password" label="Password" />

        <div>
          <q-btn label="Submit" type="submit" color="primary" />
        </div>
      </q-form>
    </q-card>
  </q-page>
</template>

<script>
import { mapState } from "vuex";

export default {
  name: "Login",
  data() {
    return {
      email: "",
      password: "",
    };
  },
  methods: {
    async submit() {
      this.$store.dispatch("aLogIn", {
        username: this.email,
        password: this.password,
      }).auth;
    },
  },
  computed: mapState({
    loginError: (state) => state.auth.logInError,
  }),
};
</script>

<style></style>
