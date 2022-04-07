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
    async aWorkspaceColumnAppendMarkdown({ commit, dispatch }, payload) {
      // TODO: Check if workspace loaded
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
    async aWorkspaceColumnMoveLeft({ commit, dispatch }, payload) {
      commit("workspaceColumnMoveLeft", payload);
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
    workspaceColumnAppendBlock(state, payload) {
      state.workspace_lst[payload.workspace].workspace.content[payload.column].content.push(payload.param);
    },
    workspaceColumnAdd(state, payload) {
      state.workspace_lst[payload.workspace].workspace.content.push({
        name: "New column",
        content: [],
      });
    },
    workspaceColumnMoveLeft(state, { workspace, index }) {
      var cnt = state.workspace_lst[workspace].workspace.content;
      if (index > 0 && cnt[index] != undefined) [cnt[index - 1], cnt[index]] = [cnt[index], cnt[index - 1]];
    },
    workspaceColumnDelete(state, { workspace, index }) {
      state.workspace_lst[workspace].workspace.content.splice(index, 1);
    },
    workspaceBlockDelete(state, { workspace, row, col }) {
      var cnt = state.workspace_lst[workspace].workspace.content;
      if (cnt[col] != undefined && cnt[col].content[row] != undefined) cnt[col].content.splice(row, 1);
    },
    workspaceBlockMove(state, { workspace, row, col, direction }) {
      var cnt = state.workspace_lst[workspace].workspace.content;
      if (cnt[col] == undefined || cnt[col].content[row] == undefined) return;
      switch (direction) {
        case "left":
          if (col > 0) {
            cnt[col - 1].content.push(cnt[col].content[row]);
            cnt[col].content.splice(row, 1);
          }
          break;
        case "right":
          if (cnt[col + 1] != undefined) {
            cnt[col + 1].content.push(cnt[col].content[row]);
            cnt[col].content.splice(row, 1);
          }
          break;
        case "up":
          if (row > 0)
            [cnt[col].content[row], cnt[col].content[row - 1]] = [cnt[col].content[row - 1], cnt[col].content[row]];
          break;
        case "down":
          if (cnt[col].content[row + 1] != undefined)
            [cnt[col].content[row], cnt[col].content[row + 1]] = [cnt[col].content[row + 1], cnt[col].content[row]];
          break;
      }
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
