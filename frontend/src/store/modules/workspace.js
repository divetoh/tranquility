import { api } from "@/api";

export default {
  state: {
    workspace_lst: {},
  },
  actions: {
    async aWorkspaceLoad({ commit }, uid) {
      try {
        const response = await api.jsondoc.get(uid);
        if (response.data) {
          var payload = response.data;
          payload.saved = true;
          commit("workspaceSet", payload);
        }
      } catch (error) {
        //await dispatch("aCheckApiError", error);
      }
    },
    async aWorkspacesLoad({ commit }) {
      try {
        const response = await api.jsondoc.get_all({ doctype: "workspace" });
        if (response.data) {
          for (var payload of response.data) {
            payload.saved = true;
            commit("workspaceSet", payload);
          }
        }
      } catch (error) {
        //await dispatch("aCheckApiError", error);
      }
    },
    async aWorkspaceSave({ state }, uid) {
      try {
        await api.jsondoc.update(uid, {
          jsondoc: JSON.stringify(state.workspace_lst[uid].workspace),
          name: state.workspace_lst[uid].name,
        });
      } catch (error) {
        //await dispatch("aCheckApiError", error);
      }
    },
    async aWorkspaceCreate({ commit }, payload) {
      const response = await api.jsondoc.create({
        doctype: "workspace",
        name: payload.name,
        jsondoc: JSON.stringify({
          name: payload.name,
          type: payload.type,
          content: [],
        }),
      });
      if (response.data) {
        var data = response.data;
        commit("workspaceSet", data);
        return data.uid;
      }
    },
    async aWorkspaceColumnAppendTasklist({ commit, dispatch }, payload) {
      commit("workspaceColumnAppendTasklist", payload);
      await dispatch("aWorkspaceSave", payload.workspace);
    },
    async aWorkspaceColumnAppendMarkdown({ commit, dispatch }, payload) {
      commit("workspaceColumnAppendMarkdown", payload);
      await dispatch("aWorkspaceSave", payload.workspace);
    },
    async aWorkspaceColumnAppendBlock({ commit, dispatch }, payload) {
      commit("workspaceColumnAppendBlock", payload);
      await dispatch("aWorkspaceSave", payload.workspace);
    },
    async aWorkspaceColumnAdd({ commit, dispatch }, { workspace }) {
      commit("workspaceColumnAdd", { workspace });
      await dispatch("aWorkspaceSave", workspace);
    },
    async aWorkspaceColumnMove({ commit, dispatch }, payload) {
      commit("workspaceColumnMove", payload);
      await dispatch("aWorkspaceSave", payload.workspace);
    },
    async aWorkspaceColumnDelete({ commit, dispatch }, payload) {
      commit("workspaceColumnDelete", payload);
      await dispatch("aWorkspaceSave", payload.workspace);
    },
    async aWorkspaceBlockDelete({ commit, dispatch }, payload) {
      commit("workspaceBlockDelete", payload);
      await dispatch("aWorkspaceSave", payload.workspace);
    },
    async aWorkspaceBlockMove({ commit, dispatch }, payload) {
      commit("workspaceBlockMove", payload);
      await dispatch("aWorkspaceSave", payload.workspace);
    },
    async aWorkspaceSetColumnName({ commit, dispatch }, payload) {
      commit("workspaceSetColumnName", payload);
      await dispatch("aWorkspaceSave", payload.workspace);
    },
    async aWorkspaceSetName({ commit, dispatch }, { workspace, name }) {
      commit("workspaceSetName", { workspace, name });
      await dispatch("aWorkspaceSave", workspace);
    },
    async aWorkspaceDelete({ commit }, { workspace }) {
      const response = await api.jsondoc.delete(workspace);
      if (response.data.state) commit("workspaceDelete", workspace);
    },
  },
  mutations: {
    workspaceSet(state, payload) {
      state.workspace_lst[payload.uid] = {
        name: payload.name,
        workspace: JSON.parse(payload.jsondoc),
        saved: payload.saved,
      };
    },
    workspaceSetSaved(state, payload) {
      state.workspace_lst[payload.uid].saved = payload.saved;
    },
    workspaceColumnAppendMarkdown(state, payload) {
      state.workspace_lst[payload.workspace].workspace.content[payload.column].content.push({
        type: "markdown",
        uid: payload.markdown,
      });
    },
    workspaceColumnAppendTasklist(state, payload) {
      state.workspace_lst[payload.workspace].workspace.content[payload.column].content.push({
        type: "tasklist",
        uid: payload.tasklist,
      });
    },
    workspaceColumnAppendBlock(state, payload) {
      state.workspace_lst[payload.workspace].workspace.content[payload.column].content.push(payload.param);
    },
    workspaceColumnAdd(state, payload) {
      state.workspace_lst[payload.workspace].workspace.content.push({
        name: "New column",
        content: [],
      });
    },
    workspaceColumnMove(state, { workspace, from_col, to_col }) {
      var cnt = state.workspace_lst[workspace].workspace.content;
      if (cnt.lenght < to_col || cnt[from_col] == undefined) return;
      const col = cnt[from_col];
      cnt.splice(to_col, 0, col);
      if (to_col <= from_col) from_col += 1;
      cnt.splice(from_col, 1);
    },
    workspaceColumnDelete(state, { workspace, index }) {
      state.workspace_lst[workspace].workspace.content.splice(index, 1);
    },
    workspaceBlockDelete(state, { workspace, row, col }) {
      var cnt = state.workspace_lst[workspace].workspace.content;
      if (cnt[col] != undefined && cnt[col].content[row] != undefined) cnt[col].content.splice(row, 1);
    },
    workspaceBlockMove(state, { workspace, from_row, from_col, to_row, to_col }) {
      var cnt = state.workspace_lst[workspace].workspace.content;
      if (cnt[from_col] == undefined || cnt[from_col].content[from_row] == undefined) return;
      if (cnt[to_col] == undefined || cnt[to_col].content.lenght < to_row) return;
      const block = cnt[from_col].content[from_row];
      cnt[to_col].content.splice(to_row, 0, block);
      if (to_col == from_col && to_row <= from_row) from_row += 1;
      cnt[from_col].content.splice(from_row, 1);
    },
    workspaceSetColumnName(state, { workspace, name, index }) {
      state.workspace_lst[workspace].workspace.content[index].name = name;
    },
    workspaceSetName(state, { workspace, name }) {
      state.workspace_lst[workspace].name = name;
    },
    workspaceDelete(state, workspace) {
      delete state.workspace_lst[workspace];
    },
  },
};
