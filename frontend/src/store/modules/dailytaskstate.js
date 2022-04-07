import { api } from "@/api";

export default {
  state: {
    lst: {},
  },
  actions: {
    async aDailytaskstateLoad({ commit }, statedate) {
      const response = await api.dailytaskstate.get(statedate);
      if (response.data) {
        commit("dailytaskstateSet", { statedate, data: response.data });
      }
    },
    async aDailytaskstateLoadRng({ commit }, { start, end }) {
      const response = await api.dailytaskstate.get_all({ start, end });
      if (response.data) {
        commit("dailytaskstateSetMulti", response.data);
      }
    },
    async aDailytaskstateSet({ commit, state, dispatch }, { statedate, taskstate, dailytask }) {
      if (state.lst[statedate] == undefined) await dispatch("aDailytaskstateLoad", statedate);
      if (state.lst[statedate][dailytask] == undefined) return false;
      // TODO: Create daily task if it's not exist
      const response = await api.dailytaskstate.update(statedate, { state: taskstate }, { dailytask });
      if (response.data) {
        commit("dailytaskstateUpdate", { statedate, taskstate, dailytask });
      }
    },
  },
  mutations: {
    dailytaskstateSet(state, payload) {
      state.lst[payload.statedate] = {};
      for (var i of payload.data) state.lst[payload.statedate][i.dailytask] = i.state;
    },
    dailytaskstateSetMulti(state, payload) {
      for (var s of payload) {
        if (state.lst[s.statedate] == undefined) state.lst[s.statedate] = {};
        state.lst[s.statedate][s.dailytask] = s.state;
      }
    },
    dailytaskstateUpdate(state, { statedate, taskstate, dailytask }) {
      state.lst[statedate][dailytask] = taskstate;
    },
    dailytaskstateDeleteByTask(state, payload) {
      for (var i in state.lst) for (var j in state.lst[i]) if (j == payload) delete state.lst[i][j];
    },
  },
};
