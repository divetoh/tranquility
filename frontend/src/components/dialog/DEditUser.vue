<template>
  <q-dialog ref="dialogRef" persistent>
    <q-card class="q-pa-md q-gutter-md">
      <div>
        <q-input outlined dense v-model="full_name" label="Full name" stack-label />
      </div>
      <div>
        <q-input outlined dense v-model="email" label="E-mail" type="email" stack-label />
      </div>
      <div>
        <q-input outlined dense v-model="password" label="Password" type="password" stack-label v-if="create" />
      </div>
      <div>
        <q-checkbox outlined dense v-model="is_active" label="Active" stack-label />
      </div>
      <div>
        <q-checkbox outlined dense v-model="is_superuser" label="Superuser" stack-label />
      </div>
      <q-btn color="primary" label="Cancel" @click="onCancelClick" />
      <q-btn color="primary" label="Save" @click="onOKClick" />
    </q-card>
  </q-dialog>
</template>

<script>
export default {
  name: "DEditUser",
  props: ["index"],
  emits: ["ok", "hide"],
  created: async function () {
    if (this.index == null) return;
    this.create = false;
    this.full_name = this.$store.state.admin.users[this.index].full_name;
    this.is_active = this.$store.state.admin.users[this.index].is_active;
    this.is_superuser = this.$store.state.admin.users[this.index].is_superuser;
    this.email = this.$store.state.admin.users[this.index].email;
    this.uid = this.$store.state.admin.users[this.index].uid;
  },
  data: function () {
    return {
      array_id: undefined,
      create: true,
      full_name: "",
      email: "",
      password: "",
      is_active: true,
      is_superuser: false,
      uid: null,
    };
  },
  methods: {
    show() {
      this.$refs.dialogRef.show();
    },
    hide() {
      this.$refs.dialogRef.hide();
    },
    onOKClick() {
      var data = {};
      if (this.create) {
        data.full_name = this.full_name;
        data.email = this.email;
        data.is_active = this.is_active;
        data.is_superuser = this.is_superuser;
        data.password = this.password;
        this.$store.dispatch("aAdminCreateUsers", data);
        this.$emit("ok");
        this.hide();
      } else {
        if (this.full_name != this.$store.state.admin.users[this.index].full_name) data.full_name = this.full_name;
        if (this.email != this.$store.state.admin.users[this.index].email) data.email = this.email;
        if (this.is_active != this.$store.state.admin.users[this.index].is_active) data.is_active = this.is_active;
        if (this.is_superuser != this.$store.state.admin.users[this.index].is_superuser)
          data.is_superuser = this.is_superuser;
        this.$store.dispatch("aAdminUpdateUser", { uid: this.uid, data });
        this.$emit("ok");
        this.hide();
      }
    },
    onCancelClick() {
      this.hide();
    },
  },
};
</script>
