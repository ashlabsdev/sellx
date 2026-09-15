import {
  createRouter,
  createWebHistory,
} from 'vue-router'

import HomeView from '../views/public/HomeView.vue'
import ProductDetailsView from '../views/public/ProductDetailsView.vue'

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
  ],
})

export default router