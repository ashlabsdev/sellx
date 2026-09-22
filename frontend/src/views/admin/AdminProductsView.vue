<script setup lang="ts">
import {
  onMounted,
  ref,
} from 'vue'

import {
  deleteProduct,
  getCategories,
  getProducts,
} from '../../services/api'

import type {
  Category,
} from '../../types/category'

import type {
  Product,
} from '../../types/product'


const products = ref<Product[]>([])
const categories = ref<Category[]>([])

const deletingProductId =
  ref<number | null>(null)

const productToDelete =
  ref<Product | null>(null)

const search = ref('')
const selectedCategory = ref('')
const selectedStatus = ref('')

const isLoading = ref(true)
const errorMessage = ref('')


async function loadCategories() {
  try {
    categories.value =
      await getCategories()
  } catch (error) {
    console.error(
      'Failed to load categories:',
      error,
    )
  }
}
function openDeleteModal(
  product: Product,
) {
  productToDelete.value = product
}


function closeDeleteModal() {
  if (deletingProductId.value !== null) {
    return
  }

  productToDelete.value = null
}


async function confirmDelete() {
  const product = productToDelete.value

  if (!product) {
    return
  }

  deletingProductId.value = product.id
  errorMessage.value = ''

  try {
    await deleteProduct(product.id)

    products.value =
      products.value.filter(
        (item) =>
          item.id !== product.id,
      )

    productToDelete.value = null
  } catch (error) {
    console.error(error)

    errorMessage.value =
      error instanceof Error
        ? error.message
        : 'Unable to delete product.'
  } finally {
    deletingProductId.value = null
  }
}

async function loadProducts() {
  isLoading.value = true
  errorMessage.value = ''

  try {
    products.value =
      await getProducts({
        search:
          search.value.trim() ||
          undefined,

        category_id:
          selectedCategory.value
            ? Number(
                selectedCategory.value,
              )
            : undefined,

        status:
          selectedStatus.value ||
          undefined,

        page: 1,
        page_size: 100,
      })
  } catch (error) {
    console.error(error)

    errorMessage.value =
      error instanceof Error
        ? error.message
        : 'Unable to load products.'
  } finally {
    isLoading.value = false
  }
}


async function applyFilters() {
  await loadProducts()
}


async function clearFilters() {
  search.value = ''
  selectedCategory.value = ''
  selectedStatus.value = ''

  await loadProducts()
}


function formatPrice(
  price: number,
): string {
  return new Intl.NumberFormat(
    'en-IN',
    {
      style: 'currency',
      currency: 'INR',
      maximumFractionDigits: 2,
    },
  ).format(price)
}


function getPrimaryImage(
  product: Product,
): string | null {
  if (!product.images.length) {
    return null
  }

  const primaryImage =
    product.images.find(
      (image) => image.is_primary,
    )

  return (
    primaryImage?.image_url ??
    product.images[0]?.image_url ??
    null
  )
}


onMounted(async () => {
  await Promise.all([
    loadCategories(),
    loadProducts(),
  ])
})
</script>


<template>
  <section class="products-page">
    <div class="page-heading">
      <div>
        <p class="eyebrow">
          Inventory
        </p>

        <h1>Products</h1>

        <p>
          Manage your SellX marketplace
          listings.
        </p>
      </div>

      <RouterLink
        to="/admin/products/new"
        class="primary-button"
      >
        + Add product
      </RouterLink>
    </div>


    <form
      class="filters"
      @submit.prevent="applyFilters"
    >
      <div class="search-field">
        <label for="product-search">
          Search
        </label>

        <input
          id="product-search"
          v-model="search"
          type="search"
          placeholder="Search products..."
        />
      </div>


      <div class="filter-field">
        <label for="category-filter">
          Category
        </label>

        <select
          id="category-filter"
          v-model="selectedCategory"
        >
          <option value="">
            All categories
          </option>

          <option
            v-for="category in categories"
            :key="category.id"
            :value="String(category.id)"
          >
            {{ category.name }}
          </option>
        </select>
      </div>


      <div class="filter-field">
        <label for="status-filter">
          Status
        </label>

        <select
          id="status-filter"
          v-model="selectedStatus"
        >
          <option value="">
            All statuses
          </option>

          <option value="draft">
            Draft
          </option>

          <option value="active">
            Active
          </option>

          <option value="sold">
            Sold
          </option>
        </select>
      </div>


      <div class="filter-actions">
        <button
          type="submit"
          class="filter-button"
          :disabled="isLoading"
        >
          Apply
        </button>

        <button
          type="button"
          class="clear-button"
          :disabled="isLoading"
          @click="clearFilters"
        >
          Clear
        </button>
      </div>
    </form>


    <div
      v-if="errorMessage"
      class="error-state"
    >
      {{ errorMessage }}

      <button
        type="button"
        @click="loadProducts"
      >
        Try again
      </button>
    </div>


    <div
      v-else-if="isLoading"
      class="loading-state"
    >
      Loading products...
    </div>


    <div
      v-else-if="products.length === 0"
      class="empty-state"
    >
      <h2>No products found</h2>

      <p>
        Try changing your search or
        filters.
      </p>
    </div>


    <div
      v-else
      class="products-table-wrapper"
    >
      <table class="products-table">
        <thead>
          <tr>
            <th>Product</th>
            <th>Category</th>
            <th>Condition</th>
            <th>Price</th>
            <th>Status</th>
            <th class="actions-column">
              Actions
            </th>
          </tr>
        </thead>

        <tbody>
          <tr
            v-for="product in products"
            :key="product.id"
          >
            <td>
              <div class="product-cell">
                <div class="product-image">
                  <img
                    v-if="
                      getPrimaryImage(product)
                    "
                    :src="
                      getPrimaryImage(product)!
                    "
                    :alt="product.name"
                  />

                  <span v-else>
                    No image
                  </span>
                </div>

                <div>
                  <strong>
                    {{ product.name }}
                  </strong>

                  <small>
                    #{{ product.id }}
                  </small>
                </div>
              </div>
            </td>

            <td>
              {{
                product.category?.name ??
                'Uncategorized'
              }}
            </td>

            <td>
              {{ product.condition }}
            </td>

            <td class="price-cell">
              {{ formatPrice(product.price) }}
            </td>

            <td>
              <span
                class="status-badge"
                :class="
                  `status-${product.status}`
                "
              >
                {{ product.status }}
              </span>
            </td>

            <td class="actions-column">
              <div class="row-actions">
                <RouterLink
                  :to="{
                    name: 'admin-product-edit',
                    params: {
                      id: product.id,
                    },
                  }"
                  class="edit-button"
                >
                  Edit
                </RouterLink>

                <button
                  type="button"
                  class="delete-button"
                  @click="openDeleteModal(product)"
                >
                  Delete
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <Teleport to="body">
      <div
        v-if="productToDelete"
        class="modal-backdrop"
        @click.self="closeDeleteModal"
      >
        <div
          class="delete-modal"
          role="dialog"
          aria-modal="true"
          aria-labelledby="delete-title"
        >
          <div class="delete-icon">
            !
          </div>

          <div class="delete-modal-content">
            <h2 id="delete-title">
              Delete product?
            </h2>

            <p>
              You're about to permanently delete
              <strong>
                {{ productToDelete.name }}
              </strong>.
            </p>

            <p class="delete-warning">
              This action cannot be undone.
            </p>
          </div>

          <div class="modal-actions">
            <button
              type="button"
              class="modal-cancel"
              :disabled="
                deletingProductId !== null
              "
              @click="closeDeleteModal"
            >
              Cancel
            </button>

            <button
              type="button"
              class="modal-delete"
              :disabled="
                deletingProductId !== null
              "
              @click="confirmDelete"
            >
              {{
                deletingProductId !== null
                  ? 'Deleting...'
                  : 'Delete product'
              }}
            </button>
          </div>
        </div>
      </div>
    </Teleport>
  </section>
</template>


<style scoped>
.products-page {
  width: 100%;
}

.modal-backdrop {
  display: grid;
  position: fixed;
  z-index: 1000;
  inset: 0;
  place-items: center;
  padding: 20px;
  background: rgba(0, 0, 0, 0.45);
}

.delete-modal {
  width: 100%;
  max-width: 440px;
  padding: 28px;
  border-radius: 16px;
  background: #fff;
  box-shadow:
    0 24px 70px
    rgba(0, 0, 0, 0.2);
}

.delete-icon {
  display: grid;
  width: 42px;
  height: 42px;
  margin-bottom: 18px;
  place-items: center;
  border-radius: 50%;
  background: #fff0f0;
  color: #b42318;
  font-size: 20px;
  font-weight: 800;
}

.delete-modal-content h2 {
  margin: 0 0 10px;
  font-size: 21px;
}

.delete-modal-content p {
  margin: 0;
  color: #666;
  line-height: 1.6;
}

.delete-modal-content strong {
  color: #111;
}

.delete-warning {
  margin-top: 8px !important;
  color: #b42318 !important;
  font-size: 13px;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 26px;
}

.modal-cancel,
.modal-delete {
  min-height: 42px;
  padding: 0 16px;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 700;
}

.modal-cancel {
  border: 1px solid #ddd;
  background: #fff;
  color: #333;
}

.modal-delete {
  border: 1px solid #b42318;
  background: #b42318;
  color: #fff;
}

.modal-cancel:disabled,
.modal-delete:disabled {
  cursor: not-allowed;
  opacity: 0.55;
}

.page-heading {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 24px;
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

.row-actions {
  display: flex;
  justify-content: flex-end;
  gap: 7px;
}

.delete-button {
  padding: 7px 12px;
  border: 1px solid #f0c5c5;
  border-radius: 7px;
  background: #fff;
  color: #b42318;
  cursor: pointer;
  font-weight: 600;
}

.delete-button:hover {
  background: #fff5f5;
}

.delete-button:disabled {
  cursor: not-allowed;
  opacity: 0.5;
}

.primary-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 42px;
  padding: 0 18px;
  border: 0;
  border-radius: 9px;
  background: #111;
  color: #fff;
  font-weight: 700;
  text-decoration: none;
}


.filters {
  display: grid;
  grid-template-columns:
    minmax(220px, 2fr)
    minmax(160px, 1fr)
    minmax(140px, 1fr)
    auto;
  gap: 14px;
  align-items: end;
  margin-bottom: 24px;
  padding: 18px;
  border: 1px solid #e5e5e5;
  border-radius: 12px;
  background: #fff;
}

.search-field,
.filter-field {
  display: grid;
  gap: 7px;
}

.filters label {
  color: #555;
  font-size: 12px;
  font-weight: 700;
}

.filters input,
.filters select {
  width: 100%;
  min-height: 42px;
  padding: 0 12px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background: #fff;
  color: #111;
}

.filters input:focus,
.filters select:focus {
  border-color: #888;
  outline: none;
}

.filter-actions {
  display: flex;
  gap: 8px;
}

.filter-button,
.clear-button {
  min-height: 42px;
  padding: 0 15px;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
}

.filter-button {
  border: 1px solid #111;
  background: #111;
  color: #fff;
}

.clear-button {
  border: 1px solid #ddd;
  background: #fff;
  color: #333;
}

.filter-button:disabled,
.clear-button:disabled {
  cursor: not-allowed;
  opacity: 0.5;
}

.products-table-wrapper {
  overflow-x: auto;
  border: 1px solid #e5e5e5;
  border-radius: 12px;
  background: #fff;
}

.products-table {
  width: 100%;
  border-collapse: collapse;
}

.products-table th,
.products-table td {
  padding: 15px 16px;
  border-bottom: 1px solid #eee;
  text-align: left;
  vertical-align: middle;
}

.products-table th {
  background: #fafafa;
  color: #666;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.04em;
  text-transform: uppercase;
}

.products-table tbody tr:last-child td {
  border-bottom: 0;
}

.products-table tbody tr:hover {
  background: #fcfcfc;
}

.product-cell {
  display: flex;
  align-items: center;
  gap: 12px;
  min-width: 230px;
}

.product-image {
  display: grid;
  flex: 0 0 52px;
  width: 52px;
  height: 52px;
  overflow: hidden;
  place-items: center;
  border: 1px solid #eee;
  border-radius: 8px;
  background: #f5f5f5;
  color: #999;
  font-size: 9px;
}

.product-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.product-cell strong {
  display: block;
  margin-bottom: 4px;
}

.product-cell small {
  color: #999;
}

.price-cell {
  white-space: nowrap;
  font-weight: 600;
}

.status-badge {
  display: inline-flex;
  align-items: center;
  min-height: 26px;
  padding: 0 9px;
  border-radius: 999px;
  background: #eee;
  color: #555;
  font-size: 11px;
  font-weight: 700;
  text-transform: capitalize;
}

.status-draft {
  background: #f1f1f1;
  color: #555;
}

.status-active {
  background: #e9f8ee;
  color: #18753c;
}

.status-sold {
  background: #fff2e5;
  color: #9a4c00;
}

.actions-column {
  text-align: right !important;
}

.edit-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 7px 12px;
  border: 1px solid #ddd;
  border-radius: 7px;
  background: #fff;
  color: #333;
  font-weight: 600;
  text-decoration: none;
}

.edit-button:hover {
  border-color: #aaa;
}

.loading-state,
.empty-state,
.error-state {
  padding: 50px 24px;
  border: 1px solid #e5e5e5;
  border-radius: 12px;
  background: #fff;
  text-align: center;
}

.loading-state {
  color: #666;
}

.empty-state h2 {
  margin: 0 0 8px;
  font-size: 20px;
}

.empty-state p {
  margin: 0;
  color: #777;
}

.error-state {
  color: #b42318;
}

.error-state button {
  display: block;
  margin: 16px auto 0;
  padding: 8px 14px;
}

@media (max-width: 1000px) {
  .filters {
    grid-template-columns:
      repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 650px) {
  .page-heading {
    flex-direction: column;
  }

  .filters {
    grid-template-columns: 1fr;
  }

  .filter-actions {
    width: 100%;
  }

  .filter-button,
  .clear-button {
    flex: 1;
  }
}
</style>