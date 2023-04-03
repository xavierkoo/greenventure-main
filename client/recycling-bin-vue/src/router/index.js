import { createRouter, createWebHistory } from "vue-router";
import PlasticBin from "../views/PlasticBin.vue";
import PaperBin from "../views/PaperBin.vue";

const routes = [
  {
    path: "/",
    name: "plastic",
    component: PlasticBin,
  },

  {
    path: "/paper_bin",
    name: "paperbin",
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.

    // component: () =>
    //   import(/* webpackChunkName: "about" */ "../views/AboutView.vue"),
    component: PaperBin,
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
