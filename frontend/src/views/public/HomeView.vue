<script setup lang="ts">
import { onMounted, ref } from 'vue'

import ProductCard from '../../components/ProductCard.vue'
import {
  getCategories,
  getProducts,
} from '../../services/api'

import type { Product } from '../../types/product'
import type { Category } from '../../types/category'

const products = ref<Product[]>([])
const categories = ref<Category[]>([])

const search = ref('')
const selectedCategory = ref<number | undefined>()
const selectedStatus = ref('')

const isLoading = ref(false)
const errorMessage = ref('')

async function loadProducts() {
  isLoading.value = true
  errorMessage.value = ''

  try {
    products.value = await getProducts({
      search: search.value.trim() || undefined,
      category_id: selectedCategory.value,
      status: selectedStatus.value || undefined,
    })
  } catch {
    errorMessage.value = 'Unable to load products.'
  } finally {
    isLoading.value = false
  }
}

async function loadCategories() {
  try {
    categories.value = await getCategories()
  } catch {
    errorMessage.value = 'Unable to load categories.'
  }
}

async function applyFilters() {
  await loadProducts()
}

async function clearFilters() {
  search.value = ''
  selectedCategory.value = undefined
  selectedStatus.value = ''

  await loadProducts()
}

onMounted(async () => {
  await Promise.all([
    loadProducts(),
    loadCategories(),
  ])
})
</script>

<template>
  <main class="home-page">
    <section class="hero">
      <h1>SellX</h1>

      <p>
        Find products you are looking for.
      </p>
    </section>

    <section class="filters">
      <input
        v-model="search"
        type="text"
        placeholder="Search products..."
        @keyup.enter="applyFilters"
      />

      <select v-model="selectedCategory">
        <option :value="undefined">
          All Categories
        </option>

        <option
          v-for="category in categories"
          :key="category.id"
          :value="category.id"
        >
          {{ category.name }}
        </option>
      </select>

      <select v-model="selectedStatus">
        <option value="">
          All Statuses
        </option>

        <option value="active">
          Active
        </option>

        <option value="draft">
          Draft
        </option>
      </select>

      <button type="button" @click="applyFilters">
        Search
      </button>

      <button
        type="button"
        @click="clearFilters"
      >
        Clear
      </button>
    </section>

    <section class="products-section">
      <p v-if="isLoading">
        Loading products...
      </p>

      <p
        v-else-if="errorMessage"
        class="error-message"
      >
        {{ errorMessage }}
      </p>

      <p
        v-else-if="products.length === 0"
      >
        No products found.
      </p>

      <div
        v-else
        class="products-grid"
      >
        <ProductCard
          v-for="product in products"
          :key="product.id"
          :product="product"
        />
      </div>
    </section>
  </main>
</template>

<style scoped>
.home-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 20px;
}

.hero {
  margin-bottom: 32px;
}

.hero h1 {
  margin: 0 0 8px;
  font-size: 42px;
  color: #c3ff00;
}

.hero p {
  margin: 0;
  color: #fff;
}

.filters {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-bottom: 32px;
}

.filters input,
.filters select,
.filters button {
  min-height: 42px;
  padding: 0 12px;
  border: 1px solid #ccc;
  border-radius: 8px;
  background: #fff;
}

.filters input {
  min-width: 240px;
}

.filters button {
  cursor: pointer;
}

.products-grid {
  display: grid;
  grid-template-columns: repeat(
    auto-fill,
    minmax(260px, 1fr)
  );
  color: #333;
  gap: 20px;
}

.error-message {
  color: #c00;
}
</style>