import { api } from "@/api";

export default {
  state: {
    lst: null,
  },
  actions: {
    async aDailytasksLoad({ commit }) {
      const response = await api.dailytask.get_all();
      if (response.data) {
        commit("dailytaskSet", response.data);
      }
    },
    async aDailytaskUpdate({ commit, dispatch, rootState }, { uid, data }) {
      const dt = rootState.current.date;
      commit("dailytaskUpdate", { uid, data });
      api.dailytask.update(uid, data, { operationdate: dt });
      if (data.is_active === false) await dispatch("aDailytaskstateRemoveAfterDate", { dailytask: uid, fromdate: dt });
      else if (data.is_active === true)
        await dispatch("aDailytaskstateCreateAfterDate", { dailytask: uid, fromdate: dt, taskstate: 0 });
    },
    async aDailytaskCreate({ commit, dispatch, rootState }, data) {
      const dt = rootState.current.date;
      const response = await api.dailytask.create(data, { operationdate: dt });
      if (response.data) {
        commit("dailytaskAppend", response.data);
      }
      await dispatch("aDailytaskstateCreateAfterDate", { dailytask: response.data.uid, fromdate: dt, taskstate: 0 });
    },
    async aDailytaskDelete({ commit, dispatch, rootState }, { uid }) {
      commit("dailytaskDelete", uid);
      commit("dailytaskstateDeleteByTask", parseInt(uid));
      await api.dailytask.delete(uid);
      await dispatch("aDailytaskstateRemoveAfterDate", { dailytask: uid, fromdate: rootState.current.date });
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
