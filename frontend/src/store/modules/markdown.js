import { api } from "@/api";

export default {
  state: {
    markdown_data: {},
  },
  actions: {
    async aMarkdownLoad({ commit }, uid) {
      try {
        const response = await api.markdown.get(uid);
        if (response.data) {
          var payload = response.data;
          payload.saved = true;
          commit("markdownSet", payload);
        }
      } catch (error) {
        //await dispatch("aCheckApiError", error);
      }
    },
    async aMarkdownUpdate({ commit }, { uid, data }) {
      try {
        commit("markdownUpdate", { uid, data });
        const response = await api.markdown.update(uid, data);
        if (response.data) {
          commit("markdownSetSaved", { uid, saved: true });
        }
      } catch (error) {
        //await dispatch("aCheckApiError", error);
      }
    },
    async aMarkdownCreate({ commit }, { name, md, folder }) {
      try {
        const response = await api.markdown.create({ name, md, folder });
        if (response.data) {
          var payload = response.data;
          payload.saved = true;
          commit("markdownSet", payload);
          return payload.uid;
        }
      } catch (error) {
        //await dispatch("aCheckApiError", error);
      }
      return false;
    },
    async aMarkdownDelete({ commit }, payload) {
      await api.markdown.delete(payload.uid);
      commit("markdownDelete", payload);
    },
  },
  mutations: {
    markdownSet(state, payload) {
      state.markdown_data[payload.uid] = {
        name: payload.name,
        md: payload.md,
        saved: payload.saved,
        folder: payload.folder,
      };
    },
    markdownUpdate(state, { uid, data }) {
      const md = state.markdown_data[uid];
      for (const i in data) md[i] = data[i];
      if (!data.saved) md.saved = false;
    },
    markdownSetSaved(state, payload) {
      state.markdown_data[payload.uid].saved = payload.saved;
    },
    markdownDelete(state, { uid }) {
      if (state.markdown_data[uid] != undefined) delete state.markdown_data[uid];
    },
  },
};
