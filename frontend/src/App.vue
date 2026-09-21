<script setup lang="ts">
import {
  computed,
} from 'vue'

import {
  RouterView,
  useRoute,
} from 'vue-router'

import AppHeader from './components/AppHeader.vue'


const route = useRoute()

const isAdminRoute = computed(
  () => route.path.startsWith('/admin'),
)
</script>


<template>
  <AppHeader v-if="!isAdminRoute" />

  <RouterView />
</template>