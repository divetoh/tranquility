import { api } from "@/api";

export default {
  state: {
    lst: {},
    root: [],
  },
  actions: {
    async aFolderLoadAll({ commit }) {
      const response = await api.folder.get_all();
      if (response.data) {
        commit("folderSetAll", response.data);
      }
    },
  },
  mutations: {
    folderSetAll(state, payload) {
      state.lst = {};
      state.root = [];
      for (var f of payload) {
        state.lst[f.uid] = f;
        if (!f.parent) state.root.push(f.uid);
      }
    },
  },
};
