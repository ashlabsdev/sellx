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

async function selectCategory(
  categoryId: number,
) {
  selectedCategory.value = categoryId

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

    <!-- Hero -->

    <section class="hero">
      <div class="hero-content">
        <p class="eyebrow">
          Welcome to SellX
        </p>

        <h1>
          Find what you need.
          <span>Sell what you don't.</span>
        </h1>

        <p class="hero-description">
          Discover products from your local marketplace
          and find great deals in one place.
        </p>

        <div class="hero-search">
          <input
            v-model="search"
            type="text"
            placeholder="Search for products..."
            @keyup.enter="applyFilters"
          />

          <button
            type="button"
            @click="applyFilters"
          >
            Search
          </button>
        </div>
      </div>
    </section>

    <!-- Categories -->

    <section
      id="categories"
      class="section"
    >
      <div class="section-heading">
        <div>
          <p class="section-label">
            Explore
          </p>

          <h2>
            Browse Categories
          </h2>
        </div>
      </div>

      <div class="category-list">
        <button
          v-for="category in categories"
          :key="category.id"
          type="button"
          class="category-button"
          :class="{
            active:
              selectedCategory === category.id,
          }"
          @click="selectCategory(category.id)"
        >
          {{ category.name }}
        </button>
      </div>
    </section>

    <!-- Products -->

    <section
      id="products"
      class="section"
    >
      <div class="section-heading products-heading">
        <div>
          <p class="section-label">
            Marketplace
          </p>

          <h2>
            Latest Products
          </h2>
        </div>

        <button
          v-if="
            search ||
            selectedCategory ||
            selectedStatus
          "
          type="button"
          class="clear-button"
          @click="clearFilters"
        >
          Clear filters
        </button>
      </div>

      <div class="filters">
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

        <button
          type="button"
          @click="applyFilters"
        >
          Apply
        </button>
      </div>

      <div class="products-section">

        <div
          v-if="isLoading"
          class="state-message"
        >
          <p>Loading products...</p>
        </div>

        <div
          v-else-if="errorMessage"
          class="state-message error"
        >
          <p>{{ errorMessage }}</p>

          <button
            type="button"
            @click="loadProducts"
          >
            Try again
          </button>
        </div>

        <div
          v-else-if="products.length === 0"
          class="state-message"
        >
          <h3>No products found</h3>

          <p>
            Try changing your search or filters.
          </p>
        </div>

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

      </div>
    </section>

  </main>
</template>

<style scoped>
.home-page {
  min-height: 100vh;
  background: #fafafa;
}

.hero {
  padding: 90px 20px 80px;
  background:
    radial-gradient(
      circle at top right,
      #e8e8e8,
      transparent 40%
    ),
    #f4f4f4;
}

.hero-content {
  align-items: center;
  justify-content: center;
  max-width: 900px;
  margin: 0 auto;
  text-align: center;
}

.eyebrow {
  margin: 0 0 16px;
  color: #666;
  font-size: 13px;
  font-weight: 700;
  letter-spacing: 0.12em;
  text-transform: uppercase;
}

.hero h1 {
  max-width: 800px;
  margin: 0 auto;
  font-size: clamp(42px, 7vw, 72px);
  line-height: 1.05;
  letter-spacing: -0.04em;
  color: #000;
}

.hero h1 span {
  display: block;
  color: #0a2eff;
}

.hero-description {
  max-width: 600px;
  margin: 24px auto 32px;
  color: #666;
  font-size: 17px;
  line-height: 1.6;
}

.hero-search {
  display: flex;
  max-width: 650px;
  margin: 0 auto;
  padding: 6px;
  border: 1px solid #ddd;
  border-radius: 14px;
  background: #fff;
  box-shadow:
    0 12px 35px rgba(0, 0, 0, 0.07);
}

.hero-search input {
  flex: 1;
  min-width: 0;
  padding: 15px;
  border: 0;
  outline: 0;
  background: transparent;
  font-size: 15px;
}

.hero-search button,
.filters button {
  padding: 0 22px;
  border: 0;
  border-radius: 9px;
  background: #111;
  color: #fff;
  cursor: pointer;
  font-weight: 600;
}

.section {
  max-width: 1200px;
  margin: 0 auto;
  padding: 60px 20px 0;
}

.section-heading {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 20px;
  margin-bottom: 24px;
  text-align: center;
}

.section-label {
  margin: 0 0 6px;
  color: #000;
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  text-align: center;
}

.section-heading h2 {
  margin: 0;
  font-size: 30px;
  letter-spacing: -0.02em;
  color: #000;
}

.category-list {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 10px;
}

.category-button {
  padding: 12px 18px;
  border: 1px solid #ddd;
  border-radius: 999px;
  background: #fff;
  color: #333;
  cursor: pointer;
  transition:
    background 0.2s ease,
    color 0.2s ease,
    border-color 0.2s ease;
}

.category-button:hover,
.category-button.active {
  border-color: #111;
  background: #111;
  color: #fff;
}

.products-heading {
  justify-content: center;
  margin-bottom: 20px;
  color: #000;
}

.clear-button {
  border: 0;
  background: transparent;
  color: #666;
  cursor: pointer;
  text-decoration: underline;
}

.filters {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 30px;
}

.filters input,
.filters select {
  min-height: 44px;
  padding: 0 13px;
  border: 1px solid #ddd;
  border-radius: 9px;
  background: #fff;
  color: #333;
}

.filters input {
  min-width: 240px;
}

.filters select {
  min-width: 170px;
}

.filters button {
  min-height: 44px;
}

.products-section {
  padding-bottom: 80px;
}

.products-grid {
  display: grid;
  grid-template-columns:
    repeat(
      auto-fit,
      minmax(260px, 280px)
    );
  justify-content: center;
  gap: 20px;
}

.state-message {
  padding: 70px 20px;
  border: 1px dashed #ddd;
  border-radius: 16px;
  background: #fff;
  text-align: center;
}

.state-message h3 {
  margin: 0 0 8px;
  font-size: 20px;
}

.state-message p {
  margin: 0;
  color: #000;
}

.state-message.error {
  border-style: solid;
}

.state-message button {
  margin-top: 18px;
  padding: 10px 18px;
  border: 0;
  border-radius: 8px;
  background: #111;
  color: #fff;
  cursor: pointer;
}

@media (max-width: 640px) {
  .hero {
    padding: 60px 20px;
  }

  .hero-search {
    flex-direction: column;
    padding: 8px;
  }

  .hero-search input {
    padding: 14px;
  }

  .hero-search button {
    min-height: 44px;
  }

  .section {
    padding-top: 45px;
  }

  .section-heading {
  align-items: center;
  flex-direction: column;
  text-align: center;
}

  .filters {
    flex-direction: column;
  }

  .filters input,
  .filters select,
  .filters button {
    width: 100%;
  }
}
</style>