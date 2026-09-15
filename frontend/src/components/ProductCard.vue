<script setup lang="ts">
import type { Product } from '../types/product'

defineProps<{
  product: Product
}>()
</script>

<template>
  <article class="product-card">
    <div class="product-image">
      <span>No Image</span>
    </div>

    <div class="product-content">
      <h2>{{ product.name }}</h2>

      <p class="product-price">
        ₹{{ product.price.toLocaleString('en-IN') }}
      </p>

      <p
        v-if="product.description"
        class="product-description"
      >
        {{ product.description }}
      </p>

      <div class="product-meta">
        <span>{{ product.condition }}</span>

        <span v-if="product.location">
          {{ product.location }}
        </span>
      </div>
    </div>
  </article>
</template>

<style scoped>
.product-card {
  overflow: hidden;
  border: 1px solid #ddd;
  border-radius: 12px;
  background: #fff;
}

.product-image {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 220px;
  background: #f3f3f3;
  color: #777;
}

.product-content {
  padding: 16px;
}

.product-content h2 {
  margin: 0 0 8px;
  font-size: 20px;
}

.product-price {
  margin: 0 0 12px;
  font-size: 18px;
  font-weight: 700;
}

.product-description {
  margin: 0 0 12px;
  color: #555;
}

.product-meta {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  color: #666;
  font-size: 14px;
}
</style>