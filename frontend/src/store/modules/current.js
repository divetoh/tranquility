export default {
  state: {
    activity: undefined,
    workspace: undefined,
    date: undefined,
    folderFilter: 1,
    outlinerViewMode: "view",
    folderUid: 0,
    fileSource: undefined,
    fileUid: undefined,
  },
  actions: {
    async aCurrentSetActivity({ commit, dispatch, rootState }, uid) {
      if (rootState.activity.lst[uid] == undefined) await dispatch("aActivityLoad", uid);
      commit("currentSetActivity", uid);
      dispatch("aWorkspacesLoad");
      dispatch("aCurrentSetWorkspace", rootState.activity.lst[uid].workspaces[0]);
    },
    async aCurrentSetWorkspace({ commit, dispatch, rootState }, uid) {
      if (uid != undefined && rootState.workspace.workspace_lst[uid] == undefined) dispatch("aWorkspaceLoad", uid);
      commit("currentSetWorkspace", uid);
    },
    async aCurrentSetFolder({ commit }, uid) {
      commit("currentSetFolder", uid);
    },
    async aCurrentSetFile({ commit }, { source, uid }) {
      commit("currentSetFile", { source, uid });
    },
    async aCurrentSetDate({ commit, dispatch, rootState }) {
      if (!rootState.auth.isLoggedIn) return;
      var d = new Date();
      d.setHours(d.getHours() - 2);
      var tzoffset = new Date().getTimezoneOffset() * 60000;
      d = new Date(d - tzoffset).toISOString().substring(0, 10);

      commit("currentSetDate", d);
      dispatch("aDailytaskstateLoad", d);
      dispatch("aRegulartaskstateLoad", d);
      dispatch("aDaystateLoad", d);
    },
  },
  mutations: {
    currentSetActivity(state, payload) {
      state.activity = payload;
    },
    currentSetDate(state, payload) {
      state.date = payload;
    },
    currentSetWorkspace(state, payload) {
      state.workspace = payload;
    },
    currentSetFolder(state, uid) {
      state.folderUid = uid;
    },
    currentSetFile(state, { source, uid }) {
      state.fileSource = source;
      state.fileUid = uid;
    },
  },
};
