import { api } from "@/api";

export default {
  state: {
    category: {},
    stack: {},
    card: {},
  },
  actions: {
    // --- Stack ----------------------------------------------------------
    async aMemorizeStackLoad({ commit }) {
      const response = await api.memorize_stack.get_all();
      if (response.data) commit("memorizeStackSet", response.data);
    },
    async aMemorizeStackCreate({ commit }) {
      const response = await api.memorize_stack.create({
        section: "New section",
        name: "New stack",
        description: "Description",
      });
      if (response.data) {
        commit("memorizeStackUpdate", response.data);
        return response.data.uid;
      }
    },
    async aMemorizeStackDelete({ commit }, uid) {
      const response = await api.memorize_stack.delete(uid);
      if (response.data) commit("memorizeStackDelete", uid);
    },
    async aMemorizeStackUpdate({ commit }, { uid, data }) {
      const response = await api.memorize_stack.update(uid, data);
      if (response.data) commit("memorizeStackUpdateData", { uid, data });
    },

    // --- Category -------------------------------------------------------
    async aMemorizeCategoryLoad({ commit }) {
      const response = await api.memorize_category.get_all();
      if (response.data) commit("memorizeCategorySet", response.data);
    },
    async aMemorizeCategoryCreate({ commit }) {
      const response = await api.memorize_category.create({
        name: "New category",
        description: "Description",
        color: 0,
      });
      if (response.data) {
        commit("memorizeCategoryUpdate", response.data);
        return response.data.uid;
      }
    },
    async aMemorizeCategoryDelete({ commit }, uid) {
      const response = await api.memorize_category.delete(uid);
      if (response.data) commit("memorizeCategoryDelete", uid);
    },
    async aMemorizeCategoryUpdate({ commit }, { uid, data }) {
      const response = await api.memorize_category.update(uid, data);
      if (response.data) commit("memorizeCategoryUpdateData", { uid, data });
    },

    // --- Card -----------------------------------------------------------
    async aMemorizeCardLoadByStack({ commit }, { stack }) {
      const response = await api.memorize_card.get_all({ stack });
      if (response.data) commit("memorizeCardUpdate", response.data);
      var cards = [];
      for (var x of response.data) cards.push(x.uid);
      return cards;
    },
    async aMemorizeCardLoadByCategory({ commit }, { category }) {
      const response = await api.memorize_category.get_cards(category);
      if (response.data) commit("memorizeCardUpdate", response.data);
      var cards = [];
      for (var x of response.data) cards.push(x.uid);
      return cards;
    },
    async aMemorizeCardUpdate({ commit }, { uid, data }) {
      const response = await api.memorize_card.update(uid, data);
      if (response.data) commit("memorizeCardUpdateData", { uid, data });
    },
    async aMemorizeCardDelete({ commit }, uid) {
      const response = await api.memorize_card.delete(uid);
      if (response.data) commit("memorizeCardDelete", uid);
    },
    async aMemorizeCardCreate({ commit }, { stack }) {
      const response = await api.memorize_card.create({
        stack: stack,
        name: "New card",
        obverse: "Question",
        reverse: "Answer",
      });
      if (response.data) {
        commit("memorizeCardUpdate", [response.data]);
        return response.data.uid;
      }
    },
    async aMemorizeCardAnswer({ commit, rootState }, { uid, state }) {
      const response = await api.memorize_card.answer(uid, { state, answerdate: rootState.current.date });
      commit("memorizeCardSetStatus", { uid, cardstate: response.data.state });
    },
  },
  mutations: {
    // --- Stack ----------------------------------------------------------
    memorizeStackSet(state, payload) {
      for (var i of payload) {
        state.stack[i.uid] = i;
      }
    },
    memorizeStackUpdate(state, payload) {
      state.stack[payload.uid] = payload;
    },
    memorizeStackUpdateData(state, { uid, data }) {
      for (var i of Object.keys(data)) {
        state.stack[uid][i] = data[i];
      }
    },
    memorizeStackDelete(state, uid) {
      delete state.stack[uid];
    },

    // --- Category -------------------------------------------------------
    memorizeCategorySet(state, category) {
      for (var i of category) {
        state.category[i.uid] = i;
        state.category[i.uid].hex = "#" + i.color.toString(16).padStart(6, "0");
      }
    },
    memorizeCategoryUpdate(state, payload) {
      state.category[payload.uid] = payload;
      state.category[payload.uid].hex = "#" + payload.color.toString(16).padStart(6, "0");
    },
    memorizeCategoryUpdateData(state, { uid, data }) {
      for (var i of Object.keys(data)) {
        state.category[uid][i] = data[i];
        if (i == "color") state.category[uid].hex = "#" + data[i].toString(16).padStart(6, "0");
      }
    },
    memorizeCategoryDelete(state, uid) {
      delete state.category[uid];
    },

    // --- Card -----------------------------------------------------------
    memorizeCardUpdate(state, cards) {
      for (var i of cards) state.card[i.uid] = i;
    },
    memorizeCardUpdateData(state, { uid, data }) {
      for (var i of Object.keys(data)) {
        state.card[uid][i] = data[i];
      }
    },
    memorizeCardDelete(state, uid) {
      delete state.card[uid];
    },
    memorizeCardSetStatus(state, { uid, cardstate }) {
      state.card[uid].state_r = [cardstate];
    },
  },
};
