import { api } from "@/api";

export default {
  state: {
    lst: {},
  },
  actions: {
    async aDaystateLoad({ commit }, statedate) {
      const response = await api.daystate.get(statedate);
      if (response.data) {
        commit("daystateSet", response.data);
      }
    },
    async aDaystateLoadRng({ commit }, { start, end }) {
      const response = await api.daystate.get_all({ start, end });
      if (response.data) {
        commit("daystateSetMulti", response.data);
      }
    },
    async aDaystateSetRating({ commit }, { statedate, rating }) {
      // TODO: Check and load
      commit("daystateSetRating", { statedate, rating });
      await api.daystate.update(statedate, { rating });
    },
    async aDaystateSetDescription({ commit }, { statedate, description }) {
      // TODO: Check and load
      commit("daystateSetDescription", { statedate, description });
      await api.daystate.update(statedate, { description });
    },
    async aDaystateAddComplited({ commit, state, rootState }, text) {
      const statedate = rootState.current.date;
      commit("daystateAddComplited", { statedate, text });
      await api.daystate.update(statedate, { complited: JSON.stringify(state.lst[statedate].complited) });
    },
  },
  mutations: {
    daystateSet(state, payload) {
      state.lst[payload.statedate] = payload;
      state.lst[payload.statedate].complited = JSON.parse(payload.complited);
    },
    daystateSetMulti(state, payload) {
      for (var s of payload) {
        state.lst[s.statedate] = s;
        state.lst[s.statedate].complited = JSON.parse(s.complited);
      }
    },
    daystateSetRating(state, { statedate, rating }) {
      state.lst[statedate].rating = rating;
    },
    daystateSetDescription(state, { statedate, description }) {
      state.lst[statedate].description = description;
    },
    daystateAddComplited(state, { statedate, text }) {
      state.lst[statedate].complited.push(text);
    },
  },
};
