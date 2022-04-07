import { api } from "@/api";

export default {
  state: {
    lst: {},
  },
  actions: {
    async aRegulartaskstateLoad({ commit }, statedate) {
      const response = await api.regulartaskstate.get(statedate);
      if (response.data) {
        commit("regulartaskstateSetMulti", response.data);
      }
    },
    async aRegulartaskstateLoadRng({ commit }, { start, end }) {
      const response = await api.regulartaskstate.get_all({ start, end });
      if (response.data) {
        commit("regulartaskstateSetMulti", response.data);
      }
    },
    async aRegulartaskstateAdd({ commit, state, dispatch }, { statedate, taskstate, regulartask }) {
      if (state.lst[statedate] == undefined) await dispatch("aRegulartaskstateLoad", statedate);
      const response = await api.regulartaskstate.create({ statedate, state: taskstate, regulartask });
      if (response.data) {
        commit("regulartaskstateAdd", response.data);
      }
    },
  },
  mutations: {
    regulartaskstateSetMulti(state, payload) {
      for (var s of payload) {
        if (state.lst[s.statedate] == undefined) state.lst[s.statedate] = {};
        state.lst[s.statedate][s.regulartask] = s.state;
      }
    },
    regulartaskstateAdd(state, payload) {
      if (state.lst[payload.statedate] == undefined) state.lst[payload.statedate] = {};
      state.lst[payload.statedate][payload.regulartask] = payload.state;
    },
    regulartaskstateDeleteByTask(state, payload) {
      for (var i in state.lst) for (var j in state.lst[i]) if (j == payload) delete state.lst[i][j];
    },
  },
};
