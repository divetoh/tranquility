<template>
  <router-view></router-view>
</template>

<script>
import store from "../../store";

const startRouteGuard = async (to, from, next) => {
  await store.dispatch("aCheckLoggedIn");
  if (store.state.auth.isLoggedIn) {
    if (to.path === "/login" || to.path === "/") {
      next("/ws");
    } else {
      next();
    }
  } else if (store.state.auth.isLoggedIn === false) {
    if (to.path === "/" || to.path.startsWith("/ws")) {
      next("/login");
    } else {
      next();
    }
  }
};

export default {
  beforeRouteEnter(to, from, next) {
    startRouteGuard(to, from, next);
  },
  beforeRouteUpdate(to, from, next) {
    startRouteGuard(to, from, next);
  },
  created: function () {
    if (this.$store.state.current.date == undefined) this.$store.dispatch("aCurrentSetDate");
  },
};
</script>
