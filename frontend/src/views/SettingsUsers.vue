<template>
  <div class="q-pa-md q-pr-lg row items-start q-gutter-md">
    <q-card bordered class="col-6 q-pa-md">
      <q-btn class="q-mb-sm" no-caps size="sm" @click="create_user" color="primary" icon="person_add">
        &nbsp;Create user
      </q-btn>
      <div>
        <q-markup-table dense bordered class="text-left">
          <thead class="bg-indigo-3">
            <tr>
              <th>&nbsp;</th>
              <th>ID</th>
              <th>Full Name</th>
              <th>Email</th>
              <th>Active?</th>
              <th>Administrator?</th>
            </tr>
          </thead>
          <tbody>
            <template v-for="(u, index) in users" :key="u.uid">
              <tr>
                <td>
                  <q-btn flat dense size="sm" @click="edit_user(index)" icon="edit" />
                  <q-btn flat dense size="sm" @click="set_password(index)" icon="password" />
                </td>
                <td>{{ u.uid }}</td>
                <td>{{ u.full_name }}</td>
                <td>{{ u.email }}</td>
                <td>{{ u.is_active }}</td>
                <td>{{ u.is_superuser }}</td>
              </tr>
            </template>
          </tbody>
        </q-markup-table>
      </div>
    </q-card>
  </div>
</template>

<script>
import { mapState } from "vuex";
import { Dialog } from "quasar";
import DEditUser from "@/components/dialog/DEditUser";

export default {
  name: "SettingsUsers",
  data: function () {
    return {};
  },
  components: {},
  created: async function () {
    await this.$store.dispatch("aAdminLoadUsers");
  },
  methods: {
    create_user: function () {
      Dialog.create({
        component: DEditUser,
      });
    },
    edit_user: function (index) {
      Dialog.create({
        component: DEditUser,
        componentProps: {
          index,
        },
      });
    },
    set_password: async function (index) {
      const name = this.$store.state.admin.users[index].full_name;
      const uid = this.$store.state.admin.users[index].uid;
      Dialog.create({
        title: "Set password",
        message: "New password for user " + name + " (minimum 6 characters).",
        prompt: {
          model: "",
          isValid: (val) => val.length > 5,
          type: "password",
        },
        cancel: true,
        persistent: true,
      }).onOk((password) => {
        this.$store.dispatch("aAdminUpdateUser", { uid, data: { password } });
      });
    },
  },
  computed: mapState({
    users: (state) => state.admin.users,
  }),
};
</script>
