<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { healthCheck } from '../../services/api';

const apiStatus = ref('Checking API...');

onMounted(async () => {
  try {
    const result = await healthCheck();
    apiStatus.value = result.status;
  } catch {
    apiStatus.value = 'API unavailable';
  }
});
</script>

<template>
  <main>
    <h1>SellX</h1>
    <p>API Status: {{ apiStatus }}</p>
  </main>
</template>