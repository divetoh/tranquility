import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import { Quasar } from "quasar";
import quasarUserOptions from "./quasar-user-options";
require("@/assets/styles/markdown.css");
require("@/assets/styles/common.css");

const app = createApp(App).use(Quasar, quasarUserOptions).use(store).use(router);
app.config.globalProperties.$dragState = {
  objectType: "",
  object: {},
};
app.config.globalProperties.$monthNames = [
  "January",
  "February",
  "March",
  "April",
  "May",
  "June",
  "July",
  "August",
  "September",
  "October",
  "November",
  "December",
];
app.mount("#app");
