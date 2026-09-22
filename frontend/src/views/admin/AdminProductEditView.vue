<script setup lang="ts">
import {
  onMounted,
  ref,
} from 'vue'

import {
  useRoute,
  useRouter,
} from 'vue-router'

import ProductForm from '../../components/admin/ProductForm.vue'
import ProductImageManager from '../../components/admin/ProductImageManager.vue'

import {
  getCategories,
  getProduct,
  updateProduct,
} from '../../services/api'

import type {
  Category,
} from '../../types/category'

import type {
  Product,
  ProductCreate,
  ProductUpdate,
} from '../../types/product'


const route = useRoute()
const router = useRouter()

const product = ref<Product | null>(null)
const categories = ref<Category[]>([])

const isLoading = ref(true)
const isSubmitting = ref(false)
const errorMessage = ref('')


const productId = Number(
  route.params.id,
)


async function loadPage() {
  if (
    !Number.isInteger(productId) ||
    productId <= 0
  ) {
    errorMessage.value =
      'Invalid product ID.'

    isLoading.value = false

    return
  }

  try {
    const [
      productResponse,
      categoryResponse,
    ] = await Promise.all([
      getProduct(productId),
      getCategories(),
    ])

    product.value =
      productResponse

    categories.value =
      categoryResponse
  } catch (error) {
    console.error(error)

    errorMessage.value =
      error instanceof Error
        ? error.message
        : 'Unable to load product.'
  } finally {
    isLoading.value = false
  }
}


async function handleSubmit(
  data: ProductCreate | ProductUpdate,
) {
  isSubmitting.value = true
  errorMessage.value = ''

  try {
    product.value =
      await updateProduct(
        productId,
        data as ProductUpdate,
      )
  } catch (error) {
    console.error(error)

    errorMessage.value =
      error instanceof Error
        ? error.message
        : 'Unable to update product.'
  } finally {
    isSubmitting.value = false
  }
}


function cancel() {
  router.push({
    name: 'admin-products',
  })
}


onMounted(loadPage)
</script>


<template>
  <section class="product-editor">
    <div class="page-heading">
      <div>
        <p class="eyebrow">
          Products
        </p>

        <h1>Edit product</h1>

        <p v-if="product">
          {{ product.name }}
        </p>
      </div>

      <RouterLink
        to="/admin/products"
        class="back-link"
      >
        ← Products
      </RouterLink>
    </div>


    <div
      v-if="errorMessage"
      class="page-error"
    >
      {{ errorMessage }}
    </div>


    <div
      v-if="isLoading"
      class="loading-state"
    >
      Loading product...
    </div>


    <ProductForm
      v-else-if="product"
      mode="edit"
      :product="product"
      :categories="categories"
      :is-submitting="isSubmitting"
      @submit="handleSubmit"
      @cancel="cancel"
    />

    <ProductImageManager
      v-if="product"
      :product-id="product.id"
    />
  </section>
</template>


<style scoped>
.product-editor {
  width: 100%;
  max-width: 950px;
}

.page-heading {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 20px;
  margin-bottom: 28px;
}

.eyebrow {
  margin: 0 0 8px;
  color: #777;
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.page-heading h1 {
  margin: 0 0 8px;
  font-size: 34px;
}

.page-heading p {
  margin: 0;
  color: #666;
}

.back-link {
  color: #555;
  font-size: 14px;
  text-decoration: none;
}

.back-link:hover {
  color: #111;
}

.page-error {
  margin-bottom: 20px;
  padding: 12px 14px;
  border: 1px solid #f3c7c7;
  border-radius: 9px;
  background: #fff5f5;
  color: #b42318;
}

.loading-state {
  padding: 40px;
  border: 1px solid #e5e5e5;
  border-radius: 12px;
  background: #fff;
  color: #666;
  text-align: center;
}
</style>