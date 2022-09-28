import { createRouter, createWebHistory } from "vue-router";

const routes = [
  {
    path: "/",
    name: "Start",
    component: () => import("../views/main/Start.vue"),
    children: [
      {
        path: "login",
        name: "login",
        component: () => import("../views/Login.vue"),
      },
      {
        path: "ws",
        component: () => import("../views/Workspace.vue"),
      },
      {
        path: "ws/:ws_uid",
        name: "ws",
        component: () => import("../views/Workspace.vue"),
      },
      {
        path: "ol",
        component: () => import("../views/outliner/Outliner.vue"),
      },
      {
        path: "ol/:fld_uid(\\d+)/:file_uid?",
        name: "ol",
        component: () => import("../views/outliner/Outliner.vue"),
      },
      {
        path: "planing/:p_section",
        name: "planing",
        component: () => import("../views/Planing.vue"),
      },
      {
        path: "settings/:s_section",
        name: "settings",
        component: () => import("../views/Settings.vue"),
      },
      {
        path: "memorize/:s_section",
        name: "memorize",
        component: () => import("../views/memorize/Memorize.vue"),
      },
    ],
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
