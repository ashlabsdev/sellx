<script setup lang="ts">
import {
  onMounted,
  ref,
} from 'vue'

import {
  RouterLink,
  RouterView,
  useRouter,
} from 'vue-router'

import {
  getCurrentAdmin,
} from '../services/api'

import {
  removeToken,
} from '../services/auth'

import type {
  Admin,
} from '../types/admin'


const router = useRouter()

const admin = ref<Admin | null>(null)
const isLoading = ref(true)


async function loadAdmin() {
  try {
    admin.value =
      await getCurrentAdmin()
  } catch (error) {
    console.error(error)

    removeToken()

    await router.replace({
      name: 'admin-login',
    })
  } finally {
    isLoading.value = false
  }
}


async function logout() {
  removeToken()

  await router.replace({
    name: 'admin-login',
  })
}


onMounted(loadAdmin)
</script>


<template>
  <div
    v-if="isLoading"
    class="admin-loading"
  >
    Checking admin session...
  </div>

  <div
    v-else-if="admin"
    class="admin-layout"
  >
    <aside class="admin-sidebar">
      <div>
        <RouterLink
          to="/admin"
          class="admin-brand"
        >
          SellX
          <span>Admin</span>
        </RouterLink>

        <nav class="admin-nav">
          <RouterLink
            to="/admin"
            class="admin-nav-link"
          >
            Dashboard
          </RouterLink>

          <span
            class="admin-nav-link
                   admin-nav-disabled"
          >
            Products
            <small>Day 14</small>
          </span>
        </nav>
      </div>

      <RouterLink
        to="/"
        class="marketplace-link"
      >
        ← View marketplace
      </RouterLink>
    </aside>

    <div class="admin-main">
      <header class="admin-topbar">
        <div>
          <p class="admin-topbar-label">
            Signed in as
          </p>

          <strong>
            {{ admin.email }}
          </strong>
        </div>

        <button
          type="button"
          class="logout-button"
          @click="logout"
        >
          Log out
        </button>
      </header>

      <main class="admin-content">
        <RouterView />
      </main>
    </div>
  </div>
</template>


<style scoped>
.admin-loading {
  display: grid;
  min-height: 100vh;
  place-items: center;
  color: #666;
}

.admin-layout {
  display: grid;
  grid-template-columns: 250px 1fr;
  min-height: 100vh;
  background: #f7f7f8;
}

.admin-sidebar {
  display: flex;
  position: sticky;
  top: 0;
  flex-direction: column;
  justify-content: space-between;
  height: 100vh;
  padding: 28px 20px;
  border-right: 1px solid #e5e5e5;
  background: #fff;
}

.admin-brand {
  display: inline-flex;
  align-items: baseline;
  gap: 7px;
  margin-bottom: 34px;
  color: #111;
  font-size: 24px;
  font-weight: 800;
  text-decoration: none;
}

.admin-brand span {
  color: #777;
  font-size: 13px;
  font-weight: 700;
}

.admin-nav {
  display: grid;
  gap: 6px;
}

.admin-nav-link {
  display: flex;
  align-items: center;
  justify-content: space-between;
  min-height: 44px;
  padding: 0 14px;
  border-radius: 9px;
  color: #555;
  font-size: 14px;
  font-weight: 600;
  text-decoration: none;
}

.admin-nav-link:hover {
  background: #f4f4f4;
  color: #111;
}

.admin-nav-link.router-link-exact-active {
  background: #111;
  color: #fff;
}

.admin-nav-disabled {
  cursor: default;
  opacity: 0.45;
}

.admin-nav-disabled:hover {
  background: transparent;
  color: #555;
}

.admin-nav-disabled small {
  font-size: 10px;
}

.marketplace-link {
  color: #666;
  font-size: 14px;
  text-decoration: none;
}

.marketplace-link:hover {
  color: #111;
}

.admin-main {
  min-width: 0;
}

.admin-topbar {
  display: flex;
  position: sticky;
  z-index: 10;
  top: 0;
  align-items: center;
  justify-content: space-between;
  min-height: 76px;
  padding: 12px 32px;
  border-bottom: 1px solid #e5e5e5;
  background: rgba(255, 255, 255, 0.96);
}

.admin-topbar-label {
  margin: 0 0 3px;
  color: #777;
  font-size: 11px;
  text-transform: uppercase;
}

.admin-topbar strong {
  font-size: 14px;
}

.logout-button {
  padding: 9px 15px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background: #fff;
  cursor: pointer;
  font-weight: 600;
}

.logout-button:hover {
  background: #f5f5f5;
}

.admin-content {
  padding: 36px;
}

@media (max-width: 760px) {
  .admin-layout {
    grid-template-columns: 1fr;
  }

  .admin-sidebar {
    position: static;
    height: auto;
    padding: 18px 20px;
    border-right: 0;
    border-bottom: 1px solid #e5e5e5;
  }

  .admin-brand {
    margin-bottom: 16px;
  }

  .admin-nav {
    grid-template-columns: 1fr 1fr;
  }

  .marketplace-link {
    margin-top: 16px;
  }

  .admin-topbar {
    position: static;
    padding: 12px 20px;
  }

  .admin-content {
    padding: 24px 20px;
  }
}
</style>