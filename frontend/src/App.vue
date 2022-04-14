<template>
  <q-layout view="lHh LpR fFf">
    <q-drawer
      show-if-above
      side="left"
      behavior="default"
      elevated
      :width="200"
      :breakpoint="500"
      class="column justify-between no-wrap bg-drawer text-black"
    >
      <q-toolbar class="bg-sidemenu-dark text-grey-1">
        <q-toolbar-title>
          <img src="./assets/tranquility.png" class="q-pt-md q-my-lg" />
        </q-toolbar-title>
      </q-toolbar>
      <q-separator />
      <LeftBar v-if="loggedIn === true" />
      <q-item class="col-grow"></q-item>
      <LeftBarFooter v-if="loggedIn === true" />
    </q-drawer>
    <q-page-container class="fit scroll fixed">
      <router-view v-if="loggedIn !== null" />
    </q-page-container>
  </q-layout>
</template>

<script>
import LeftBar from "@/components/LeftBar.vue";
import LeftBarFooter from "@/components/LeftBarFooter.vue";
import { mapState } from "vuex";
export default {
  name: "App",
  created: async function () {
    await this.$store.dispatch("aCheckLoggedIn");
  },
  computed: mapState({
    loggedIn: (state) => state.auth.isLoggedIn,
  }),
  components: {
    LeftBar,
    LeftBarFooter,
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

html {
  background-image: url(./assets/bg.jpg);
  background-size: cover;
  background-position-y: center;
  background-attachment: fixed;
  /* background-image: url(./assets/bg_tile2.png);
  background-repeat: repeat; */
}
.hover_ctrl .hover_block {
  visibility: hidden;
  opacity: 0;
  transition: 0.4s;
}

.hover_ctrl:hover .hover_block {
  visibility: visible;
  opacity: 1;
  transition: 0.2s;
}
h1,
h2,
h3,
h4,
h5,
h6 {
  margin-top: 0.15em;
  margin-bottom: 0.05em;
}

.pointer_cursor {
  cursor: pointer;
}

tbody .qtable_inactive_row td {
  background-color: lightgray;
}

.bg-sidemenu-dark {
  background-color: #172830;
}

.q-drawer {
  background-color: #394454ce !important;
  color: white;
}

.bg-topbar {
  background-color: #394454ce !important;
  color: white;
}

.bg-card-head {
  background-color: rgb(245, 245, 245) !important;
}

.scroll6::-webkit-scrollbar {
  display: block;
  height: 6px;
  width: 6px;
}

.scroll6::-webkit-scrollbar-track {
  background-color: #394454ce;
  border-radius: 10px;
  margin: 6px;
}

.scroll6::-webkit-scrollbar-thumb {
  background-color: #c1c1c1;
  border-radius: 10px;
}
</style>
