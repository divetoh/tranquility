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
    aTasklistSaveDebounce: debounce(({ dispatch }, uid) => {
      // TODO: Check that save executes fo all uid argument
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
  },
  mutations: {
    tasklistSet(state, payload) {
      state.lst[payload.uid] = {
        uid: payload.uid,
        name: payload.name,
        doctype: payload.doctype,
        saved: payload.saved,
        jsondoc: JSON.parse(payload.jsondoc),
      };
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
  },
};
