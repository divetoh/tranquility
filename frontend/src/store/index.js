import { createStore } from "vuex";
import auth from "./modules/auth";
import admin from "./modules/admin";
import markdown from "./modules/markdown";
import workspace from "./modules/workspace";
import regulartask from "./modules/regulartask";
import regulartaskstate from "./modules/regulartaskstate";
import dailytaskstate from "./modules/dailytaskstate";
import dailytask from "./modules/dailytask";
import tasklist from "./modules/tasklist";
import current from "./modules/current.js";
import activity from "./modules/activity.js";
import daystate from "./modules/daystate.js";

export default createStore({
  state: {},
  mutations: {},
  actions: {},
  modules: {
    admin,
    auth,
    markdown,
    workspace,
    regulartask,
    dailytask,
    tasklist,
    current,
    activity,
    daystate,
    regulartaskstate,
    dailytaskstate,
  },
});
