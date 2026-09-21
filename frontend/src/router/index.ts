import {
  createRouter,
  createWebHistory,
} from 'vue-router'

import HomeView from '../views/public/HomeView.vue'
import ProductDetailsView from '../views/public/ProductDetailsView.vue'

import AdminLayout from '../layouts/AdminLayout.vue'
import AdminLoginView from '../views/admin/AdminLoginView.vue'
import AdminDashboardView from '../views/admin/AdminDashboardView.vue'

import {
  getToken,
} from '../services/auth'


const router = createRouter({
  history: createWebHistory(
    import.meta.env.BASE_URL,
  ),

  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },

    {
      path: '/products/:id',
      name: 'product-details',
      component: ProductDetailsView,
    },

    {
      path: '/admin/login',
      name: 'admin-login',
      component: AdminLoginView,
      meta: {
        guestOnly: true,
      },
    },

    {
      path: '/admin',
      component: AdminLayout,
      meta: {
        requiresAuth: true,
      },

      children: [
        {
          path: '',
          name: 'admin-dashboard',
          component: AdminDashboardView,
        },
      ],
    },
  ],
})


router.beforeEach((to) => {
  const token = getToken()

  if (
    to.meta.requiresAuth &&
    !token
  ) {
    return {
      name: 'admin-login',
    }
  }

  if (
    to.meta.guestOnly &&
    token
  ) {
    return {
      name: 'admin-dashboard',
    }
  }
})


export default router