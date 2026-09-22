<script setup lang="ts">
import {
  onMounted,
  ref,
} from 'vue'

import {
  useRouter,
} from 'vue-router'

import ProductForm from '../../components/admin/ProductForm.vue'

import {
  createProduct,
  getCategories,
} from '../../services/api'

import type {
  Category,
} from '../../types/category'

import type {
  ProductCreate,
  ProductUpdate,
} from '../../types/product'


const router = useRouter()

const categories = ref<Category[]>([])
const isLoading = ref(true)
const isSubmitting = ref(false)
const errorMessage = ref('')


async function loadCategories() {
  try {
    categories.value =
      await getCategories()
  } catch (error) {
    console.error(error)

    errorMessage.value =
      'Unable to load categories.'
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
    const product =
      await createProduct(
        data as ProductCreate,
      )

    await router.push({
      name: 'admin-products',
    })
  } catch (error) {
    console.error(error)

    errorMessage.value =
      error instanceof Error
        ? error.message
        : 'Unable to create product.'
  } finally {
    isSubmitting.value = false
  }
}


function cancel() {
  router.push({
    name: 'admin-products',
  })
}


onMounted(loadCategories)
</script>


<template>
  <section class="product-editor">
    <div class="page-heading">
      <div>
        <p class="eyebrow">
          Products
        </p>

        <h1>Add product</h1>

        <p>
          Create a new marketplace
          listing.
        </p>
      </div>
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
      Loading...
    </div>


    <ProductForm
      v-else
      mode="create"
      :categories="categories"
      :is-submitting="isSubmitting"
      @submit="handleSubmit"
      @cancel="cancel"
    />
  </section>
</template>


<style scoped>
.product-editor {
  width: 100%;
  max-width: 950px;
}

.page-heading {
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