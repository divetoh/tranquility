<template>
  <div class="row">
    <q-tree
      ref="folderTreeRef"
      class="file_tree q-pa-sm full-width"
      text-color="white"
      selected-color="white"
      :nodes="folderTree"
      node-key="uid"
      dense
      v-model:selected="selected"
      default-expand-all
      @update:selected="select"
    />
  </div>
</template>

<script>
import { mapState } from "vuex";

export default {
  name: "FolderTree",
  created: async function () {},
  components: {},
  emits: ["select"],
  data() {
    return {
      selected: null,
    };
  },
  computed: mapState({
    folderTree: function (state) {
      const tree = [];
      const backref = {};
      const filter = state.current.folderFilter;
      for (const i in state.folder.lst) {
        const b = state.folder.lst[i];
        if (filter && b.foldertype > 63) continue;
        if (!b.parent) continue;
        if (!backref[b.parent]) backref[b.parent] = [i];
        else backref[b.parent].push(i);
      }
      function make_branch(uid) {
        const branch = {
          uid: parseInt(uid),
          label: state.folder.lst[uid].name,
          icon: "folder",
          children: [],
        };
        if (backref[uid]) {
          backref[uid].sort((a, b) => {
            if (state.folder.lst[a].name > state.folder.lst[b].name) return 1;
            if (state.folder.lst[a].name < state.folder.lst[b].name) return -1;
            return 0;
          });
          for (const i of backref[uid]) branch.children.push(make_branch(i));
        }
        return branch;
      }

      const root = [...state.folder.root].sort((a, b) => {
        if (state.folder.lst[a].name > state.folder.lst[b].name) return 1;
        if (state.folder.lst[a].name < state.folder.lst[b].name) return -1;
        return 0;
      });
      for (const i of root) {
        if (filter && state.folder.lst[i].foldertype > 63) continue;
        tree.push(make_branch(i));
      }

      return tree;
    },
  }),
  methods: {
    async select(uid) {
      this.$emit("select", uid);
    },
    async setFolder(uid) {
      this.selected = parseInt(uid);
    },
  },
};
</script>
