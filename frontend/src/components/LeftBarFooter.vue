<template>
  <div class="q-pb-md bg-sidemenu-dark text-grey-1">
    <q-separator />
    <div class="text-center q-pt-md">{{ userProfile.full_name }}</div>
    <div class="text-center q-pb-md">{{ current_date }}</div>
    <div class="q-gutter-sm">
      <q-btn color="primary" no-caps to="/settings/personal" icon="settings" />
      <q-btn color="primary" no-caps @click="LogOut" icon="logout" />
    </div>
  </div>
</template>

<style></style>

<script>
import { mapState } from "vuex";
export default {
  name: "LeftBarFooter",
  computed: mapState({
    userProfile: (state) => state.auth.userProfile,
    current_date: (state) => state.current.date,
  }),
  methods: {
    async LogOut() {
      await this.$store.dispatch("aLogOut");
    },
  },
};
</script>

<style scoped>
.user_footer {
  background-color: gainsboro;
}
</style>
