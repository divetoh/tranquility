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
    async aFolderCreate({ commit }, payload) {
      const response = await api.folder.create(payload);
      if (response.data) {
        commit("folderSet", response.data);
        return response.data.uid;
      }
      return false;
    },
    async aFolderRemove({ commit }, { uid }) {
      const restponse_files = await api.folder.get_content(uid);
      if (!restponse_files.data) {
        return false;
      }
      const files = restponse_files.data;
      const response = await api.folder.delete(uid);
      if (response.data) {
        commit("folderRemove", { uid, files });
        return true;
      }
      return false;
    },
    async aFolderRemoveFile({ commit }, { uid, source }) {
      var response;
      if (source == "markdown") response = await api.markdown.delete(uid);
      else if (source == "jsondoc") response = await api.jsondoc.delete(uid);
      else return false;
      if (response.data) {
        commit("folderRemoveFile", response.data);
        return response.data.uid;
      }
      return false;
    },
    async aFolderSetName({ commit }, { uid, name }) {
      const response = await api.folder.update(uid, { name });
      if (response.data) {
        commit("folderSetName", { uid, name });
        return true;
      }
      return false;
    },
    async aFolderSetFileName({ commit }, { uid, source, name }) {
      var response;
      if (source == "markdown") response = await api.markdown.update(uid, { name });
      else if (source == "jsondoc") response = await api.jsondoc.update(uid, { name });
      else return false;
      if (response.data) {
        commit("folderSetFileName", { uid, source, name });
        return true;
      }
      return false;
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
    folderSet(state, payload) {
      // Update/add data for one folder
      if (!payload.parent && !state.root.includes(payload.uid)) state.root.push(payload.uid);
      if (payload.parent && state.root.includes(payload.uid)) state.root.splice(state.root.indexOf(payload.uid), 1);
      state.lst[payload.uid] = payload;
    },
    folderSetName(state, { uid, name }) {
      state.lst[uid].name = name;
    },
    folderSetFileName(state, { uid, source, name }) {
      if (source == "markdown" && this.state.markdown.markdown_data[uid] != undefined)
        this.state.markdown.markdown_data[uid].name = name;
    },
    folderRemove(state, { uid, files }) {
      delete state.lst[uid];
      const index = state.root.indexOf(uid);
      if (index != -1) state.root.splice(index, 1);
      for (const f in files) {
        this.commit("folderRemoveFile", f);
      }
    },
    folderRemoveFile(state, { uid, source }) {
      if (source == "markdown" && this.state.markdown.markdown_data[uid] != undefined)
        delete this.state.markdown.markdown_data[uid];
    },
  },
};
