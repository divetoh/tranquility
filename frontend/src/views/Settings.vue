<template>
  <q-page>
    <div class="">
      <q-tabs v-model="tab" no-caps dense align="left" narrow-indicator class="bg-topbar text-white">
        <q-route-tab name="personal" label="Settings" to="/settings/personal" />
        <q-route-tab name="users" label="Users" to="/settings/users" v-if="isSuperUser" />
      </q-tabs>
    </div>
    <div v-if="tab == 'personal'">
      <SettingsPersonal />
    </div>
    <div v-if="tab == 'users'">
      <SettingsUsers />
    </div>
  </q-page>
</template>

<script>
import { mapState } from "vuex";
import { ref } from "vue";
import SettingsPersonal from "@/views/SettingsPersonal";
import SettingsUsers from "@/views/SettingsUsers";

export default {
  name: "Planing",

  components: {
    SettingsUsers,
    SettingsPersonal,
  },
  created: async function () {},
  methods: {},
  computed: mapState({
    isSuperUser: (state) => state.auth.userProfile.is_superuser,
  }),

  setup() {
    return {
      tab: ref("personal"),
    };
  },
};
</script>
