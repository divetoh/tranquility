import { api } from "@/api";

export default {
  state: {
    lst: null,
  },
  actions: {
    async aRegulartasksLoad({ commit }) {
      try {
        const response = await api.regulartask.get_all();
        if (response.data) {
          commit("regulartaskSet", response.data);
        }
      } catch (error) {
        //await dispatch("aCheckApiError", error);
      }
    },
    async aRegulartaskDone({ state, commit, rootState, dispatch }, uid) {
      if (state.lst == null) await dispatch("aRegulartasksLoad");
      if (rootState.current.date == undefined) return;
      await dispatch("aRegulartaskstateAdd", { statedate: rootState.current.date, taskstate: 1, regulartask: uid });
      var nextdate = new Date();
      nextdate.setDate(nextdate.getDate() + state.lst[uid].period);
      nextdate = nextdate.toISOString().substring(0, 10);
      commit("regulartaskSetNextdate", { uid, nextdate });
      await api.regulartask.update(uid, {
        nextdate: state.lst[uid].nextdate,
      });
    },
    async aRegulartaskUpdate({ commit }, { uid, data }) {
      commit("regulartasksUpdate", { uid, data });
      api.regulartask.update(uid, data);
    },
    async aRegulartaskCreate({ commit }, data) {
      const response = await api.regulartask.create(data);
      if (response.data) {
        commit("regulartaskAppend", response.data);
      }
    },
    async aRegulartaskDelete({ commit }, { uid }) {
      commit("regulartasksDelete", uid);
      commit("regulartaskstateDeleteByTask", parseInt(uid));
      await api.regulartask.delete(uid);
    },
  },
  mutations: {
    regulartaskSet(state, payload) {
      state.lst = {};
      for (var i in payload) state.lst[payload[i].uid] = payload[i];
    },
    regulartaskAppend(state, payload) {
      state.lst[payload.uid] = payload;
    },
    regulartasksDelete(state, uid) {
      delete state.lst[uid];
    },
    regulartasksUpdate(state, { uid, data }) {
      if (state.lst[uid] == undefined) return;
      for (var i in data) {
        state.lst[uid][i] = data[i];
      }
    },
    regulartaskSetNextdate(state, { uid, nextdate }) {
      state.lst[uid].nextdate = nextdate;
    },
  },
};
