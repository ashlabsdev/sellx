<script setup lang="ts">
import {
  onMounted,
  reactive,
  ref,
} from 'vue'

import {
  createCategory,
  deleteCategory,
  getCategories,
  updateCategory,
} from '../../services/api'

import type {
  Category,
  CategoryCreate,
  CategoryUpdate,
} from '../../types/category'


const categories = ref<Category[]>([])

const isLoading = ref(true)
const isSaving = ref(false)

const errorMessage = ref('')
const successMessage = ref('')

const editingCategory =
  ref<Category | null>(null)

const categoryToDelete =
  ref<Category | null>(null)

const deletingCategoryId =
  ref<number | null>(null)


const form = reactive({
  name: '',
  description: '',
  is_active: true,
})


async function loadCategories() {
  isLoading.value = true
  errorMessage.value = ''

  try {
    categories.value =
      await getCategories()
  } catch (error) {
    console.error(error)

    errorMessage.value =
      error instanceof Error
        ? error.message
        : 'Unable to load categories.'
  } finally {
    isLoading.value = false
  }
}


function resetForm() {
  editingCategory.value = null

  form.name = ''
  form.description = ''
  form.is_active = true
}


function startEdit(
  category: Category,
) {
  editingCategory.value = category

  form.name = category.name
  form.description =
    category.description ?? ''
  form.is_active =
    category.is_active

  successMessage.value = ''
  errorMessage.value = ''

  window.scrollTo({
    top: 0,
    behavior: 'smooth',
  })
}


function cancelEdit() {
  resetForm()
  errorMessage.value = ''
}


async function saveCategory() {
  const name = form.name.trim()

  if (!name) {
    errorMessage.value =
      'Category name is required.'

    return
  }

  isSaving.value = true
  errorMessage.value = ''
  successMessage.value = ''

  try {
    if (editingCategory.value) {
      const data: CategoryUpdate = {
        name,
        description:
          form.description.trim() ||
          null,
        is_active:
          form.is_active,
      }

      await updateCategory(
        editingCategory.value.id,
        data,
      )

      successMessage.value =
        'Category updated successfully.'
    } else {
      const data: CategoryCreate = {
        name,
        description:
          form.description.trim() ||
          null,
      }

      await createCategory(data)

      successMessage.value =
        'Category created successfully.'
    }

    resetForm()

    await loadCategories()
  } catch (error) {
    console.error(error)

    errorMessage.value =
      error instanceof Error
        ? error.message
        : 'Unable to save category.'
  } finally {
    isSaving.value = false
  }
}


async function toggleCategory(
  category: Category,
) {
  errorMessage.value = ''
  successMessage.value = ''

  try {
    await updateCategory(
      category.id,
      {
        name: category.name,
        description:
          category.description,
        is_active:
          !category.is_active,
      },
    )

    successMessage.value =
      category.is_active
        ? 'Category deactivated.'
        : 'Category activated.'

    await loadCategories()
  } catch (error) {
    console.error(error)

    errorMessage.value =
      error instanceof Error
        ? error.message
        : 'Unable to update category.'
  }
}


function openDeleteModal(
  category: Category,
) {
  categoryToDelete.value =
    category
}


function closeDeleteModal() {
  if (
    deletingCategoryId.value !== null
  ) {
    return
  }

  categoryToDelete.value = null
}


async function confirmDelete() {
  const category =
    categoryToDelete.value

  if (!category) {
    return
  }

  deletingCategoryId.value =
    category.id

  errorMessage.value = ''
  successMessage.value = ''

  try {
    await deleteCategory(
      category.id,
    )

    categoryToDelete.value = null

    successMessage.value =
      'Category deleted successfully.'

    if (
      editingCategory.value?.id ===
      category.id
    ) {
      resetForm()
    }

    await loadCategories()
  } catch (error) {
    console.error(error)

    errorMessage.value =
      error instanceof Error
        ? error.message
        : 'Unable to delete category.'
  } finally {
    deletingCategoryId.value =
      null
  }
}


onMounted(loadCategories)
</script>


<template>
  <section class="categories-page">
    <div class="page-heading">
      <div>
        <p class="eyebrow">
          Catalogue
        </p>

        <h1>Categories</h1>

        <p>
          Organize products into
          marketplace categories.
        </p>
      </div>
    </div>


    <div
      v-if="errorMessage"
      class="message error-message"
    >
      {{ errorMessage }}
    </div>

    <div
      v-if="successMessage"
      class="message success-message"
    >
      {{ successMessage }}
    </div>


    <div class="category-layout">

      <!-- Form -->

      <section class="form-card">
        <div class="card-heading">
          <div>
            <p class="eyebrow">
              {{
                editingCategory
                  ? 'Editing'
                  : 'New category'
              }}
            </p>

            <h2>
              {{
                editingCategory
                  ? 'Edit category'
                  : 'Add category'
              }}
            </h2>
          </div>
        </div>


        <form
          class="category-form"
          @submit.prevent="saveCategory"
        >
          <label class="field">
            <span>
              Category name
              <strong>*</strong>
            </span>

            <input
              v-model="form.name"
              type="text"
              maxlength="100"
              placeholder="e.g. Mobile Phones"
              :disabled="isSaving"
            />
          </label>


          <label class="field">
            <span>Description</span>

            <textarea
              v-model="form.description"
              rows="5"
              placeholder="Optional category description..."
              :disabled="isSaving"
            />
          </label>


          <label
            v-if="editingCategory"
            class="toggle-field"
          >
            <input
              v-model="form.is_active"
              type="checkbox"
              :disabled="isSaving"
            />

            <span>
              Category is active
            </span>
          </label>


          <div class="form-actions">
            <button
              type="submit"
              class="primary-button"
              :disabled="isSaving"
            >
              {{
                isSaving
                  ? 'Saving...'
                  : editingCategory
                    ? 'Save changes'
                    : 'Create category'
              }}
            </button>

            <button
              v-if="editingCategory"
              type="button"
              class="secondary-button"
              :disabled="isSaving"
              @click="cancelEdit"
            >
              Cancel
            </button>
          </div>
        </form>
      </section>


      <!-- Category list -->

      <section class="list-card">
        <div class="card-heading">
          <div>
            <p class="eyebrow">
              Existing
            </p>

            <h2>
              All categories
            </h2>
          </div>

          <span class="count">
            {{ categories.length }}
          </span>
        </div>


        <div
          v-if="isLoading"
          class="state"
        >
          Loading categories...
        </div>


        <div
          v-else-if="
            categories.length === 0
          "
          class="state"
        >
          No categories yet.
        </div>


        <div
          v-else
          class="category-list"
        >
          <article
            v-for="category in categories"
            :key="category.id"
            class="category-item"
          >
            <div class="category-info">
              <div class="category-title">
                <h3>
                  {{ category.name }}
                </h3>

                <span
                  class="status-badge"
                  :class="{
                    inactive:
                      !category.is_active,
                  }"
                >
                  {{
                    category.is_active
                      ? 'Active'
                      : 'Inactive'
                  }}
                </span>
              </div>

              <p
                v-if="category.description"
              >
                {{ category.description }}
              </p>

              <small>
                /{{ category.slug }}
              </small>
            </div>


            <div class="category-actions">
              <button
                type="button"
                class="secondary-button small"
                @click="
                  startEdit(category)
                "
              >
                Edit
              </button>

              <button
                type="button"
                class="secondary-button small"
                @click="
                  toggleCategory(
                    category,
                  )
                "
              >
                {{
                  category.is_active
                    ? 'Deactivate'
                    : 'Activate'
                }}
              </button>

              <button
                type="button"
                class="danger-button small"
                @click="
                  openDeleteModal(
                    category,
                  )
                "
              >
                Delete
              </button>
            </div>
          </article>
        </div>
      </section>

    </div>


    <!-- SellX confirmation modal -->

    <div
      v-if="categoryToDelete"
      class="modal-backdrop"
      @click.self="closeDeleteModal"
    >
      <section
        class="delete-modal"
        role="dialog"
        aria-modal="true"
        aria-labelledby="delete-category-title"
      >
        <div class="warning-icon">
          !
        </div>

        <h2 id="delete-category-title">
          Delete category?
        </h2>

        <p>
          You're about to delete
          <strong>
            {{ categoryToDelete.name }}
          </strong>.
        </p>

        <p class="modal-note">
          This action cannot be undone.
        </p>

        <div class="modal-actions">
          <button
            type="button"
            class="secondary-button"
            :disabled="
              deletingCategoryId !== null
            "
            @click="closeDeleteModal"
          >
            Cancel
          </button>

          <button
            type="button"
            class="danger-button"
            :disabled="
              deletingCategoryId !== null
            "
            @click="confirmDelete"
          >
            {{
              deletingCategoryId !== null
                ? 'Deleting...'
                : 'Delete category'
            }}
          </button>
        </div>
      </section>
    </div>
  </section>
</template>


<style scoped>
.categories-page {
  max-width: 1200px;
  margin: 0 auto;
}

.page-heading {
  margin-bottom: 28px;
}

.page-heading h1 {
  margin: 4px 0 8px;
  color: #111;
  font-size: 34px;
}

.page-heading p {
  margin: 0;
  color: #666;
}

.eyebrow {
  color: #777;
  font-size: 12px;
  font-weight: 800;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.message {
  margin-bottom: 20px;
  padding: 12px 14px;
  border-radius: 9px;
}

.error-message {
  border: 1px solid #f0c7c7;
  background: #fff5f5;
  color: #a22;
}

.success-message {
  border: 1px solid #cfe4d4;
  background: #f3faf5;
  color: #286238;
}

.category-layout {
  display: grid;
  grid-template-columns:
    minmax(280px, 0.8fr)
    minmax(0, 1.4fr);
  gap: 24px;
  align-items: start;
}

.form-card,
.list-card {
  padding: 24px;
  border: 1px solid #e5e5e5;
  border-radius: 14px;
  background: #fff;
}

.form-card {
  position: sticky;
  top: 24px;
}

.card-heading {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
  margin-bottom: 22px;
}

.card-heading h2 {
  margin: 3px 0 0;
  color: #111;
}

.count {
  display: grid;
  min-width: 34px;
  height: 34px;
  place-items: center;
  border-radius: 999px;
  background: #111;
  color: #fff;
  font-size: 13px;
  font-weight: 700;
}

.category-form {
  display: grid;
  gap: 18px;
}

.field {
  display: grid;
  gap: 7px;
}

.field span {
  color: #333;
  font-size: 13px;
  font-weight: 700;
}

.field strong {
  color: #c33;
}

.field input,
.field textarea {
  width: 100%;
  padding: 11px 12px;
  border: 1px solid #d8d8d8;
  border-radius: 8px;
  background: #fff;
  color: #111;
  font: inherit;
}

.field textarea {
  resize: vertical;
}

.field input:focus,
.field textarea:focus {
  border-color: #777;
  outline: none;
}

.toggle-field {
  display: flex;
  align-items: center;
  gap: 9px;
  color: #444;
  font-size: 14px;
}

.form-actions,
.category-actions,
.modal-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.primary-button,
.secondary-button,
.danger-button {
  min-height: 40px;
  padding: 0 14px;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 700;
}

.primary-button {
  border: 1px solid #111;
  background: #111;
  color: #fff;
}

.secondary-button {
  border: 1px solid #ddd;
  background: #fff;
  color: #333;
}

.danger-button {
  border: 1px solid #e1b9b9;
  background: #fff7f7;
  color: #a22;
}

.small {
  min-height: 34px;
  padding: 0 10px;
  font-size: 12px;
}

button:disabled {
  cursor: not-allowed;
  opacity: 0.55;
}

.category-list {
  display: grid;
}

.category-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
  padding: 18px 0;
  border-bottom: 1px solid #eee;
}

.category-item:first-child {
  padding-top: 0;
}

.category-item:last-child {
  padding-bottom: 0;
  border-bottom: 0;
}

.category-info {
  min-width: 0;
}

.category-title {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 9px;
}

.category-title h3 {
  margin: 0;
  color: #111;
}

.category-info p {
  margin: 7px 0;
  color: #666;
  line-height: 1.5;
}

.category-info small {
  color: #999;
}

.status-badge {
  padding: 4px 8px;
  border-radius: 999px;
  background: #eaf7ee;
  color: #26733a;
  font-size: 11px;
  font-weight: 800;
}

.status-badge.inactive {
  background: #f1f1f1;
  color: #777;
}

.state {
  padding: 40px 10px;
  color: #777;
  text-align: center;
}

.modal-backdrop {
  display: grid;
  position: fixed;
  z-index: 1000;
  inset: 0;
  place-items: center;
  padding: 20px;
  background: rgb(0 0 0 / 45%);
}

.delete-modal {
  width: min(440px, 100%);
  padding: 28px;
  border-radius: 16px;
  background: #fff;
  box-shadow:
    0 20px 60px rgb(0 0 0 / 18%);
}

.warning-icon {
  display: grid;
  width: 42px;
  height: 42px;
  margin-bottom: 18px;
  place-items: center;
  border-radius: 50%;
  background: #fff0f0;
  color: #a22;
  font-weight: 900;
}

.delete-modal h2 {
  margin: 0 0 10px;
}

.delete-modal p {
  color: #555;
  line-height: 1.6;
}

.modal-note {
  color: #888 !important;
  font-size: 13px;
}

.modal-actions {
  justify-content: flex-end;
  margin-top: 24px;
}

@media (max-width: 850px) {
  .category-layout {
    grid-template-columns: 1fr;
  }

  .form-card {
    position: static;
  }

  .category-item {
    align-items: flex-start;
    flex-direction: column;
  }
}
</style>