import { createRouter, createWebHistory } from "vue-router";

const routes = [
  {
    path: "/",
    name: "Start",
    component: () => import("../views/main/Start.vue"),
    children: [
      {
        path: "login",
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
