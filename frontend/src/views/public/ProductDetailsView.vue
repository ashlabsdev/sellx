<script setup lang="ts">
import {
  computed,
  onMounted,
  ref,
} from 'vue'
import { RouterLink, useRoute } from 'vue-router'

import { getProduct } from '../../services/api'

import type { Product } from '../../types/product'

const route = useRoute()

const product = ref<Product | null>(null)

  const selectedImageUrl =
  ref<string | null>(null)


const orderedImages = computed(() => {
  if (!product.value) {
    return []
  }

  return [...product.value.images]
    .sort(
      (a, b) =>
        a.display_order -
        b.display_order,
    )
})


function selectInitialImage() {
  if (!product.value) {
    return
  }

  const primaryImage =
    product.value.images.find(
      (image) => image.is_primary,
    )

  selectedImageUrl.value =
    primaryImage?.image_url ??
    orderedImages.value[0]?.image_url ??
    null
}

const isLoading = ref(true)
const errorMessage = ref('')

async function loadProduct() {
  isLoading.value = true
  errorMessage.value = ''

  try {
    const productId = Number(route.params.id)

    product.value =
    await getProduct(productId)

  selectInitialImage()
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
        <div class="product-gallery">
          <div class="product-image">
            <img
              v-if="selectedImageUrl"
              :src="selectedImageUrl"
              :alt="product.name"
            />

            <span v-else>
              No Image
            </span>
          </div>

          <div
            v-if="orderedImages.length > 1"
            class="thumbnail-list"
          >
            <button
              v-for="image in orderedImages"
              :key="image.id"
              type="button"
              class="thumbnail"
              :class="{
                active:
                  selectedImageUrl ===
                  image.image_url,
              }"
              @click="
                selectedImageUrl =
                  image.image_url
              "
            >
              <img
                :src="image.image_url"
                :alt="product.name"
              />
            </button>
          </div>
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

.product-gallery {
  min-width: 0;
}

.product-image {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 500px;
  overflow: hidden;
  border-radius: 14px;
  background: #f3f3f3;
  color: #999;
}

.product-image img {
  display: block;
  width: 100%;
  height: 500px;
  object-fit: contain;
}

.thumbnail-list {
  display: flex;
  gap: 10px;
  margin-top: 12px;
  overflow-x: auto;
  padding-bottom: 4px;
}

.thumbnail {
  flex: 0 0 78px;
  width: 78px;
  height: 78px;
  overflow: hidden;
  padding: 0;
  border: 2px solid transparent;
  border-radius: 9px;
  background: #f3f3f3;
  cursor: pointer;
}

.thumbnail.active {
  border-color: #111;
}

.thumbnail img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

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
  
  .product-image {
    min-height: 320px;
  }

  .product-image img {
    height: 320px;
  }
}
</style>