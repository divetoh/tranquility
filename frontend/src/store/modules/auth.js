import { api } from "@/api";
import { getLocalToken, removeLocalToken, saveLocalToken } from "@/utils";
import router from "@/router";

export default {
  state: {
    token: null,
    isLoggedIn: null,
    logInError: null,
    userProfile: null,
    notifications: [],
  },
  actions: {
    async aCheckAPIError({ dispatch }, payload) {
      if (payload.response.status === 401) {
        await dispatch("aLogOut");
      }
    },
    async aCheckLoggedIn({ commit, state, dispatch }) {
      if (!state.isLoggedIn) {
        let token = state.token;
        if (!token) {
          const localToken = getLocalToken();
          if (localToken) {
            commit("setToken", localToken);
            token = localToken;
          }
        }
        if (token) {
          try {
            const response = await api.user.get("me");
            commit("setLoggedIn", true);
            commit("setUserProfile", response.data);
            await dispatch("aCurrentSetActivity", response.data.coreactivity);
            await dispatch("aFolderLoadAll");
          } catch (error) {
            await dispatch("aRemoveLogIn");
          }
        } else {
          await dispatch("aRemoveLogIn");
        }
      }
    },
    async aGetUserProfile({ commit, dispatch }) {
      try {
        const response = await api.user.get("me");
        if (response.data) {
          commit("setUserProfile", response.data);
        }
      } catch (error) {
        await dispatch("aCheckApiError", error);
      }
    },
    async aLogIn({ commit, dispatch, state }, payload) {
      //try {
      var token = payload.token;
      if (token == undefined) {
        const response = await api.logInGetToken(payload.username, payload.password);
        token = response.data.access_token;
      }
      if (token) {
        saveLocalToken(token);
        commit("setToken", token);
        await dispatch("aGetUserProfile");
        await dispatch("aCurrentSetActivity", state.userProfile.coreactivity);
        commit("setLoggedIn", true);
        commit("setLogInError", false);
        await dispatch("aCurrentSetDate");
        await dispatch("aRouteLoggedIn");
        commit("addNotification", { content: "Logged in", color: "success" });
      } else {
        await dispatch("aLogOut");
      }
      /*
      } catch (err) {
        console.log(err);
        commit("setLogInError", true);
        await dispatch("aLogOut");
      }*/
    },
    async aRemoveLogIn({ commit }) {
      removeLocalToken();
      commit("setToken", "");
      commit("setLoggedIn", false);
    },
    async aLogOut({ dispatch }) {
      await dispatch("aRemoveLogIn");
      await dispatch("aRouteLogOut");
    },
    async aRouteLoggedIn() {
      router.push("/");
    },
    async aRouteLogOut() {
      if (router.currentRoute.path !== "/login") {
        router.push("/login");
      }
    },
    async aAuthSetFullname({ commit }, name) {
      commit("setFullname", name);
      api.user.update("me", { full_name: name });
    },
    async aAuthSetPassword(_, password) {
      api.user.update("me", { password });
    },
  },
  mutations: {
    setToken(state, payload) {
      state.token = payload;
    },
    setLoggedIn(state, payload) {
      state.isLoggedIn = payload;
    },
    setLogInError(state, payload) {
      state.logInError = payload;
    },
    setUserProfile(state, payload) {
      state.userProfile = payload;
    },
    addNotification(state, payload) {
      state.notifications.push(payload);
    },
    removeNotification(state, payload) {
      state.notifications = state.notifications.filter((notification) => notification !== payload);
    },
    setFullname(state, payload) {
      state.userProfile.full_name = payload;
    },
  },
};
