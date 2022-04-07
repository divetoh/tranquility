<template>
  <q-list padding class="side-menu-list">
    <q-item
      clickable
      :active="this.$route.name == 'ws'"
      @click="this.$router.push('/ws/')"
      active-class="act-menu-link"
    >
      <q-item-section avatar>
        <q-icon name="developer_board"></q-icon>
      </q-item-section>
      <q-item-section class="text-left">Workspace</q-item-section>
    </q-item>

    <q-item
      clickable
      :active="this.$route.name == 'planing'"
      @click="this.$router.push('/planing/tasks')"
      active-class="act-menu-link"
    >
      <q-item-section avatar>
        <q-icon name="assignment"></q-icon>
      </q-item-section>
      <q-item-section color="white" class="text-left">Planing</q-item-section>
    </q-item>
  </q-list>
</template>

<script>
export default {
  name: "LeftBar",
  components: {},
};
</script>

<style scoped>
.act-menu-link {
  background-color: #172830;
  color: white;
}
.side-menu-list {
  color: white;
}
</style>
