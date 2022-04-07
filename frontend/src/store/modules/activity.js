import { api } from "@/api";

export default {
  state: {
    lst: {},
  },
  actions: {
    async aActivityLoad({ commit }, uid) {
      const response = await api.jsondoc.get(uid);
      if (response.data) {
        commit("activitySet", response.data);
      }
    },
    async aActivitySave({ state }, uid) {
      await api.jsondoc.update(uid, {
        jsondoc: JSON.stringify({
          name: state.lst[uid].name,
          workspaces: state.lst[uid].workspaces,
        }),
        name: state.lst[uid].name,
      });
    },
    async aActivityRemoveWorkspace({ commit, dispatch }, { activity, workspace }) {
      commit("activityRemoveWorkspace", { activity, workspace });
      await dispatch("aActivitySave", activity);
    },
    async aActivityAppendWorkspace({ commit, dispatch }, { activity, workspace }) {
      commit("activityAppendWorkspace", { activity, workspace });
      await dispatch("aActivitySave", activity);
    },
    async aActivityMoveWorkspaceUp({ commit, dispatch }, { activity, index }) {
      commit("activityMoveWorkspaceUp", { activity, index });
      await dispatch("aActivitySave", activity);
    },
  },
  mutations: {
    activitySet(state, payload) {
      const doc = JSON.parse(payload.jsondoc);
      state.lst[payload.uid] = {
        uid: payload.uid,
        name: payload.uid,
        workspaces: doc.workspaces,
      };
    },
    activityAppendWorkspace(state, { activity, workspace }) {
      state.lst[activity].workspaces.push(workspace);
    },
    activityRemoveWorkspace(state, { activity, workspace }) {
      const index = state.lst[activity].workspaces.indexOf(workspace);
      if (index !== -1) {
        state.lst[activity].workspaces.splice(index, 1);
      }
    },
    activityMoveWorkspaceUp(state, { activity, index }) {
      var ws = state.lst[activity].workspaces;
      [ws[index], ws[index - 1]] = [ws[index - 1], ws[index]];
    },
  },
};
