<script setup lang="ts">
import { RouterLink } from 'vue-router'

import type { Product } from '../types/product'

defineProps<{
  product: Product
}>()
</script>

<template>
  <RouterLink
    :to="`/products/${product.id}`"
    class="product-card"
  >
    <div class="product-image">
      <span>No Image</span>
    </div>

    <div class="product-content">
      <div class="product-heading">
        <h2>{{ product.name }}</h2>

        <span class="condition">
          {{ product.condition }}
        </span>
      </div>

      <p class="product-price">
        ₹{{ product.price.toLocaleString('en-IN') }}
      </p>

      <p
        v-if="product.description"
        class="product-description"
      >
        {{ product.description }}
      </p>

      <div
        v-if="product.location"
        class="product-location"
      >
        {{ product.location }}
      </div>
    </div>
  </RouterLink>
</template>

<style scoped>
.product-card {
  display: block;
  overflow: hidden;
  border: 1px solid #e5e5e5;
  border-radius: 16px;
  background: #fff;
  color: inherit;
  text-decoration: none;
  transition:
    transform 0.2s ease,
    box-shadow 0.2s ease,
    border-color 0.2s ease;
}

.product-card:hover {
  transform: translateY(-4px);
  border-color: #ccc;
  box-shadow: 0 12px 30px rgba(0, 0, 0, 0.08);
}

.product-image {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 230px;
  background: #f5f5f5;
  color: #999;
}

.product-content {
  padding: 18px;
}

.product-heading {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 12px;
  color: #000;
}

.product-heading h2 {
  margin: 0;
  font-size: 18px;
  line-height: 1.3;
}

.condition {
  flex-shrink: 0;
  padding: 4px 8px;
  border-radius: 999px;
  background: #ffff00;
  color: #0400ff;
  font-size: 11px;
  font-weight: 700;
  text-transform: capitalize;
}

.product-price {
  margin: 12px 0;
  font-size: 21px;
  font-weight: 700;
  color: #0400ff;
}

.product-description {
  display: -webkit-box;
  overflow: hidden;
  margin: 0 0 12px;
  color: #666;
  line-height: 1.5;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 2;
}

.product-location {
  color: #777;
  font-size: 13px;
}
</style>