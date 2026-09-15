<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { RouterLink, useRoute } from 'vue-router'

import { getProduct } from '../../services/api'

import type { Product } from '../../types/product'

const route = useRoute()

const product = ref<Product | null>(null)

const isLoading = ref(true)
const errorMessage = ref('')

async function loadProduct() {
  isLoading.value = true
  errorMessage.value = ''

  try {
    const productId = Number(route.params.id)

    product.value = await getProduct(productId)
  } catch {
    errorMessage.value =
      'Unable to load this product.'
  } finally {
    isLoading.value = false
  }
}

onMounted(loadProduct)
</script>

<template>
  <main class="details-page">

    <div class="details-container">

      <RouterLink
        to="/"
        class="back-link"
      >
        ← Back to products
      </RouterLink>

      <div
        v-if="isLoading"
        class="state"
      >
        Loading product...
      </div>

      <div
        v-else-if="errorMessage"
        class="state error"
      >
        {{ errorMessage }}
      </div>

      <section
        v-else-if="product"
        class="product-details"
      >
        <div class="product-image">
          <span>No Image</span>
        </div>

        <div class="product-info">

          <span class="condition">
            {{ product.condition }}
          </span>

          <h1>
            {{ product.name }}
          </h1>

          <p class="price">
            ₹{{ product.price.toLocaleString('en-IN') }}
          </p>

          <p
            v-if="product.description"
            class="description"
          >
            {{ product.description }}
          </p>

          <div class="details-list">

            <div v-if="product.location">
              <span>Location</span>
              <strong>
                {{ product.location }}
              </strong>
            </div>

            <div>
              <span>Status</span>
              <strong>
                {{ product.status }}
              </strong>
            </div>

          </div>

          <div class="actions">
            <a
              v-if="product.contact_phone"
              :href="`tel:${product.contact_phone}`"
              class="primary-button"
            >
              Contact Seller
            </a>

            <a
              v-if="product.contact_phone"
              :href="`https://wa.me/${product.contact_phone}`"
              target="_blank"
              rel="noopener noreferrer"
              class="secondary-button"
            >
              WhatsApp
            </a>
          </div>

        </div>
      </section>

    </div>

  </main>
</template>

<style scoped>
.details-page {
  min-height: calc(100vh - 72px);
  padding: 50px 20px 80px;
  background: #fafafa;
}

.details-container {
  max-width: 1100px;
  margin: 0 auto;
}

.back-link {
  display: inline-block;
  margin-bottom: 30px;
  color: #555;
  text-decoration: none;
}

.back-link:hover {
  color: #111;
}

.product-details {
  display: grid;
  grid-template-columns:
    minmax(0, 1.1fr)
    minmax(0, 0.9fr);
  gap: 50px;
  padding: 30px;
  border: 1px solid #e5e5e5;
  border-radius: 20px;
  background: #fff;
}

.product-image {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 500px;
  border-radius: 14px;
  background: #f3f3f3;
  color: #999;
}

.product-info {
  padding: 20px 0;
}

.condition {
  display: inline-block;
  padding: 6px 10px;
  border-radius: 999px;
  background: #f1f1f1;
  color: #555;
  font-size: 12px;
  text-transform: capitalize;
}

.product-info h1 {
  margin: 18px 0 12px;
  font-size: 42px;
  line-height: 1.1;
  letter-spacing: -0.03em;
}

.price {
  margin: 0 0 25px;
  font-size: 30px;
  font-weight: 700;
}

.description {
  color: #666;
  line-height: 1.7;
}

.details-list {
  margin-top: 30px;
  border-top: 1px solid #eee;
}

.details-list div {
  display: flex;
  justify-content: space-between;
  gap: 20px;
  padding: 15px 0;
  border-bottom: 1px solid #eee;
}

.details-list span {
  color: #888;
}

.details-list strong {
  text-align: right;
  text-transform: capitalize;
}

.actions {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 30px;
}

.primary-button,
.secondary-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 46px;
  padding: 0 20px;
  border-radius: 9px;
  text-decoration: none;
  font-weight: 600;
}

.primary-button {
  background: #111;
  color: #fff;
}

.secondary-button {
  border: 1px solid #ddd;
  background: #fff;
  color: #111;
}

.state {
  padding: 80px 20px;
  border-radius: 16px;
  background: #fff;
  text-align: center;
}

.state.error {
  color: #b00020;
}

@media (max-width: 800px) {
  .product-details {
    grid-template-columns: 1fr;
    gap: 20px;
    padding: 20px;
  }

  .product-image {
    min-height: 350px;
  }

  .product-info h1 {
    font-size: 34px;
  }
}
</style>