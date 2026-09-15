<script setup lang="ts">
import { RouterLink } from 'vue-router'

import logo from '../assets/sellX4-logo.jpeg'
</script>

<template>
  <header class="app-header">
    <div class="header-container">
      <RouterLink
        to="/"
        class="logo-link"
      >
        <img
          :src="logo"
          alt="SellX"
          class="logo"
        />
      </RouterLink>

      <nav class="navigation">
        <RouterLink to="/">
          Home
        </RouterLink>

        <a href="#categories">
          Categories
        </a>

        <a href="#products">
          Products
        </a>
      </nav>
    </div>
  </header>
</template>

<style scoped>
.app-header {
  position: sticky;
  top: 0;
  z-index: 100;
  border-bottom: 1px solid #e5e5e5;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
}

.header-container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  max-width: 1200px;
  min-height: 72px;
  margin: 0 auto;
  padding: 0 20px;
}

.logo-link {
  display: flex;
  align-items: center;
}

.logo {
  width: 150px;
  height: auto;
}

.navigation {
  display: flex;
  align-items: center;
  gap: 28px;
}

.navigation a {
  color: #333;
  font-size: 15px;
  font-weight: 500;
  text-decoration: none;
}

.navigation a:hover {
  color: #000;
}

@media (max-width: 640px) {
  .header-container {
    min-height: 64px;
  }

  .logo {
    width: 125px;
  }

  .navigation {
    gap: 14px;
  }

  .navigation a {
    font-size: 13px;
  }
}
</style>