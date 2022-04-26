import { api } from "@/api";

export default {
  state: {
    users: [],
  },
  actions: {
    async aAdminLoadUsers({ commit }) {
      const response = await api.user.get_all();
      if (response.data) {
        commit("adminSetUsers", response.data);
      }
    },
    async aAdminCreateUsers({ commit }, data) {
      const response = await api.user.create(data);
      if (response.data) {
        commit("adminCreateUser", response.data);
      }
    },
    async aAdminDeleteUser({ commit }, { uid }) {
      const response = await api.user.delete(uid);
      if (response.data) {
        commit("adminDeleteUser", { uid });
      }
    },
    async aAdminUpdateUser({ state, commit, dispatch, rootState }, { uid, data }) {
      await api.user.update(uid, data);
      for (var index in state.users)
        if (state.users[index].uid == uid) {
          commit("adminUpdateUser", { index, data });
          break;
        }
      if (rootState.auth.userProfile.uid == uid) dispatch("aGetUserProfile");
    },
  },
  mutations: {
    adminSetUsers(state, payload) {
      state.users = payload;
    },
    adminCreateUser(state, payload) {
      state.users.push(payload);
    },
    adminUpdateUser(state, { index, data }) {
      for (var i in data) {
        if (i == "password") continue;
        state.users[index][i] = data[i];
      }
    },
    adminDeleteUser(state, { uid }) {
      for (var i in state.users) {
        if (state.users[i].uid != uid) continue;
        state.users.splice(i, 1);
        break;
      }
    },
  },
};
