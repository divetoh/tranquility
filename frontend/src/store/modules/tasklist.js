import { api } from "@/api";
import { debounce } from "lodash";

export default {
  state: {
    lst: {},
  },
  actions: {
    async aTasklistLoad({ commit }, uid) {
      try {
        const response = await api.jsondoc.get(uid);
        if (response.data) {
          var payload = response.data;
          payload.saved = true;
          commit("tasklistSet", payload);
        }
      } catch (error) {
        //await dispatch("aCheckApiError", error);
      }
    },
    async aTasklistCreate({ commit }, { name, folder }) {
      const response = await api.jsondoc.create({
        doctype: "tasklist",
        name,
        folder,
        jsondoc: JSON.stringify([]),
      });
      if (response.data) {
        var payload = response.data;
        payload.saved = true;
        commit("tasklistSet", payload);
        return payload.uid;
      }
      return false;
    },
    async aTasklistDelete({ commit }, { uid }) {
      const response = await api.jsondoc.delete(uid);
      if (response.data.state) commit("tasklistDelete", uid);
    },
    aTasklistAddRows({ commit, dispatch }, { uid, count }) {
      commit("tasklistAddRows", { uid, count });
      dispatch("aTasklistSaveDebounce", uid);
    },
    async aTasklistSave({ commit, state }, uid) {
      await api.jsondoc.update(uid, {
        jsondoc: JSON.stringify(state.lst[uid].jsondoc),
        name: state.lst[uid].name,
      });
      commit("tasklistSetSaved", { uid, saved: true });
    },
    async aTasklistSaveDebounce({ dispatch }, uid) {
      dispatch("aTasklistSave", uid);
    },
    aTasklistSaveDebounce_2fix: debounce(({ dispatch }, uid) => {
      // TODO: Don't work for different uid
      dispatch("aTasklistSave", uid);
    }, 2000),
    async aTaskListDelItem({ commit, dispatch }, payload) {
      commit("tasklistDelItem", payload);
      dispatch("aTasklistSaveDebounce", payload.uid);
    },
    async aTaskListAddItem({ commit, dispatch }, payload) {
      commit("tasklistAddItem", payload);
      dispatch("aTasklistSaveDebounce", payload.uid);
    },
    async aTasklistSetText({ commit, dispatch }, payload) {
      commit("tasklistSetItemText", payload);
      dispatch("aTasklistSaveDebounce", payload.uid);
    },
    async aTaskListRemoveDailyTask({ state, dispatch }, { uid, dailytask }) {
      for (var i in state.lst[uid].jsondoc) {
        if (state.lst[uid].jsondoc[i].type == "dailytask" && state.lst[uid].jsondoc[i].dailytask == dailytask) {
          await dispatch("aTaskListDelItem", { uid, index: i });
          break;
        }
      }
    },
    async aTaskListRemoveRegularTask({ state, dispatch }, { uid, regulartask }) {
      for (var i in state.lst[uid].jsondoc) {
        if (state.lst[uid].jsondoc[i].type == "regulartask" && state.lst[uid].jsondoc[i].regulartask == regulartask) {
          await dispatch("aTaskListDelItem", { uid, index: i });
          break;
        }
      }
    },
    async aTasklistItemMove({ state, dispatch, commit }, { from_uid, from_row, to_uid, to_row }) {
      if (state.lst[from_uid] == undefined) await dispatch("aTasklistLoad", from_uid);
      if (state.lst[to_uid] == undefined) await dispatch("aTasklistLoad", to_uid);
      commit("tasklistItemMove", { from_uid, from_row, to_uid, to_row });
      dispatch("aTasklistSaveDebounce", from_uid);
      if (to_uid != from_uid) dispatch("aTasklistSaveDebounce", to_uid);
    },
  },
  mutations: {
    tasklistSet(state, payload) {
      state.lst[payload.uid] = {
        uid: payload.uid,
        name: payload.name,
        folder: payload.folder,
        doctype: payload.doctype,
        saved: payload.saved,
        jsondoc: JSON.parse(payload.jsondoc),
      };
    },
    tasklistDelete(state, { uid }) {
      delete state.lst[uid];
    },
    tasklistSetSaved(state, payload) {
      state.lst[payload.uid].saved = payload.saved;
    },
    tasklistAddRows(state, payload) {
      for (var i = 0; i < payload.count; i++) state.lst[payload.uid].jsondoc.push({ text: "" });
      state.lst[payload.uid].saved = false;
    },
    tasklistDelItem(state, payload) {
      state.lst[payload.uid].jsondoc.splice(payload.index, 1);
      state.lst[payload.uid].saved = false;
    },
    tasklistAddItem(state, payload) {
      state.lst[payload.uid].jsondoc.push(payload.item);
      state.lst[payload.uid].saved = false;
    },
    tasklistSetItemText(state, { uid, index, text }) {
      state.lst[uid].jsondoc[index].text = text;
      state.lst[uid].saved = false;
    },
    tasklistItemMove(state, { from_uid, from_row, to_uid, to_row }) {
      const block = state.lst[from_uid].jsondoc[from_row];
      state.lst[to_uid].jsondoc.splice(to_row, 0, block);
      if (to_uid == from_uid && to_row <= from_row) from_row += 1;
      state.lst[from_uid].jsondoc.splice(from_row, 1);
      state.lst[from_uid].saved = false;
      state.lst[to_uid].saved = false;
    },
  },
};
