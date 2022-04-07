import { api } from "@/api";

export default {
  state: {
    lst: null,
  },
  actions: {
    async aDailytasksLoad({ commit }) {
      try {
        const response = await api.dailytask.get_all();
        if (response.data) {
          commit("dailytaskSet", response.data);
        }
      } catch (error) {
        //await dispatch("aCheckApiError", error);
      }
    },
    async aDailytaskUpdate({ commit, rootState }, { uid, data }) {
      commit("dailytaskUpdate", { uid, data });
      api.dailytask.update(uid, data, { operationdate: rootState.current.date });
      // TODO: Create/remove dailytaskstate
    },
    async aDailytaskCreate({ commit, rootState }, data) {
      const response = await api.dailytask.create(data, { operationdate: rootState.current.date });
      if (response.data) {
        commit("dailytaskAppend", response.data);
      }
      // TODO: Create dailytaskstate
    },
    async aDailytaskDelete({ commit }, { uid }) {
      commit("dailytaskDelete", uid);
      commit("dailytaskstateDeleteByTask", parseInt(uid));
      await api.dailytask.delete(uid);
    },
  },
  mutations: {
    dailytaskSet(state, payload) {
      state.lst = {};
      for (var i in payload) state.lst[payload[i].uid] = payload[i];
    },
    dailytaskAppend(state, payload) {
      state.lst[payload.uid] = payload;
    },
    dailytaskDelete(state, uid) {
      delete state.lst[uid];
    },
    dailytaskUpdate(state, { uid, data }) {
      if (state.lst[uid] == undefined) return;
      for (var i in data) {
        state.lst[uid][i] = data[i];
      }
    },
  },
};
