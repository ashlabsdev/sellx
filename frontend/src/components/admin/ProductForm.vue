<script setup lang="ts">
import {
  reactive,
  ref,
  watch,
} from 'vue'

import type {
  Category,
} from '../../types/category'

import type {
  Product,
  ProductCreate,
  ProductUpdate,
} from '../../types/product'


const props = withDefaults(
  defineProps<{
    categories: Category[]
    product?: Product | null
    mode: 'create' | 'edit'
    isSubmitting?: boolean
  }>(),
  {
    product: null,
    isSubmitting: false,
  },
)


const emit = defineEmits<{
  submit: [
    data: ProductCreate | ProductUpdate,
  ]
  cancel: []
}>()


const errorMessage = ref('')


const form = reactive({
  name: '',
  category_id: '',
  description: '',
  price: '',
  condition: '',
  location: '',
  contact_phone: '',
  status: 'draft',
})


function populateForm() {
  if (!props.product) {
    form.name = ''
    form.category_id = ''
    form.description = ''
    form.price = ''
    form.condition = ''
    form.location = ''
    form.contact_phone = ''
    form.status = 'draft'

    return
  }

  form.name = props.product.name

  form.category_id =
    props.product.category_id !== null
      ? String(props.product.category_id)
      : ''

  form.description =
    props.product.description ?? ''

  form.price =
    String(props.product.price)

  form.condition =
    props.product.condition

  form.location =
    props.product.location ?? ''

  form.contact_phone =
    props.product.contact_phone ?? ''

  form.status =
    props.product.status
}


watch(
  () => props.product,
  populateForm,
  {
    immediate: true,
  },
)


function handleSubmit() {
  errorMessage.value = ''

  const name = form.name.trim()
  const price = Number(form.price)
  const condition =
    form.condition.trim()

  if (!name) {
    errorMessage.value =
      'Product name is required.'

    return
  }

  if (
    !form.price ||
    Number.isNaN(price) ||
    price < 0
  ) {
    errorMessage.value =
      'Enter a valid product price.'

    return
  }

  if (!condition) {
    errorMessage.value =
      'Product condition is required.'

    return
  }

  const commonData = {
    name,

    category_id:
      form.category_id
        ? Number(form.category_id)
        : null,

    description:
      form.description.trim() ||
      null,

    price,

    condition,

    location:
      form.location.trim() ||
      null,

    contact_phone:
      form.contact_phone.trim() ||
      null,
  }

  if (props.mode === 'create') {
    const data: ProductCreate = {
      ...commonData,
    }

    emit('submit', data)

    return
  }

  const data: ProductUpdate = {
    ...commonData,
    status: form.status,
  }

  emit('submit', data)
}
</script>


<template>
  <form
    class="product-form"
    @submit.prevent="handleSubmit"
  >
    <div
      v-if="errorMessage"
      class="validation-error"
    >
      {{ errorMessage }}
    </div>


    <section class="form-section">
      <div class="section-heading">
        <h2>Product details</h2>

        <p>
          Basic information shown on
          the marketplace.
        </p>
      </div>


      <div class="form-grid">
        <label class="field field-full">
          <span>
            Product name
            <strong>*</strong>
          </span>

          <input
            v-model="form.name"
            type="text"
            maxlength="200"
            placeholder="e.g. iPhone 15 Pro"
            :disabled="isSubmitting"
          />
        </label>


        <label class="field">
          <span>Category</span>

          <select
            v-model="form.category_id"
            :disabled="isSubmitting"
          >
            <option value="">
              No category
            </option>

            <option
              v-for="category in categories"
              :key="category.id"
              :value="String(category.id)"
            >
              {{ category.name }}
            </option>
          </select>
        </label>


        <label class="field">
          <span>
            Price
            <strong>*</strong>
          </span>

          <input
            v-model="form.price"
            type="number"
            min="0"
            step="0.01"
            placeholder="0.00"
            :disabled="isSubmitting"
          />
        </label>


        <label class="field">
          <span>
            Condition
            <strong>*</strong>
          </span>

          <select
            v-model="form.condition"
            :disabled="isSubmitting"
          >
            <option value="">
              Select condition
            </option>

            <option value="new">
              New
            </option>

            <option value="like_new">
              Like new
            </option>

            <option value="good">
              Good
            </option>

            <option value="fair">
              Fair
            </option>
          </select>
        </label>


        <label
          v-if="mode === 'edit'"
          class="field"
        >
          <span>Status</span>

          <select
            v-model="form.status"
            :disabled="isSubmitting"
          >
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
        </label>


        <label class="field field-full">
          <span>Description</span>

          <textarea
            v-model="form.description"
            rows="6"
            placeholder="Describe the product..."
            :disabled="isSubmitting"
          />
        </label>
      </div>
    </section>


    <section class="form-section">
      <div class="section-heading">
        <h2>Seller details</h2>

        <p>
          Location and contact information
          for the listing.
        </p>
      </div>


      <div class="form-grid">
        <label class="field">
          <span>Location</span>

          <input
            v-model="form.location"
            type="text"
            placeholder="e.g. Bengaluru"
            :disabled="isSubmitting"
          />
        </label>


        <label class="field">
          <span>Contact phone</span>

          <input
            v-model="form.contact_phone"
            type="tel"
            placeholder="+91..."
            :disabled="isSubmitting"
          />
        </label>
      </div>
    </section>


    <div class="form-actions">
      <button
        type="button"
        class="secondary-button"
        :disabled="isSubmitting"
        @click="emit('cancel')"
      >
        Cancel
      </button>

      <button
        type="submit"
        class="primary-button"
        :disabled="isSubmitting"
      >
        {{
          isSubmitting
            ? 'Saving...'
            : mode === 'create'
              ? 'Create product'
              : 'Save changes'
        }}
      </button>
    </div>
  </form>
</template>


<style scoped>
.product-form {
  display: grid;
  gap: 22px;
}

.form-section {
  padding: 24px;
  border: 1px solid #e5e5e5;
  border-radius: 14px;
  background: #fff;
}

.section-heading {
  margin-bottom: 24px;
}

.section-heading h2 {
  margin: 0 0 6px;
  font-size: 18px;
}

.section-heading p {
  margin: 0;
  color: #777;
  font-size: 14px;
}

.form-grid {
  display: grid;
  grid-template-columns:
    repeat(2, minmax(0, 1fr));
  gap: 20px;
}

.field {
  display: grid;
  gap: 8px;
}

.field-full {
  grid-column: 1 / -1;
}

.field span {
  color: #444;
  font-size: 13px;
  font-weight: 700;
}

.field strong {
  color: #b42318;
}

.field input,
.field select,
.field textarea {
  width: 100%;
  padding: 11px 12px;
  border: 1px solid #dcdcdc;
  border-radius: 8px;
  background: #fff;
  color: #111;
  font: inherit;
}

.field input,
.field select {
  min-height: 44px;
}

.field textarea {
  resize: vertical;
  line-height: 1.6;
}

.field input:focus,
.field select:focus,
.field textarea:focus {
  border-color: #777;
  outline: none;
}

.field input:disabled,
.field select:disabled,
.field textarea:disabled {
  background: #f6f6f6;
  cursor: not-allowed;
}

.validation-error {
  padding: 12px 14px;
  border: 1px solid #f3c7c7;
  border-radius: 9px;
  background: #fff5f5;
  color: #b42318;
  font-size: 14px;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.primary-button,
.secondary-button {
  min-height: 44px;
  padding: 0 18px;
  border-radius: 9px;
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

.primary-button:disabled,
.secondary-button:disabled {
  cursor: not-allowed;
  opacity: 0.55;
}

@media (max-width: 700px) {
  .form-grid {
    grid-template-columns: 1fr;
  }

  .field-full {
    grid-column: auto;
  }

  .form-actions {
    flex-direction: column-reverse;
  }

  .primary-button,
  .secondary-button {
    width: 100%;
  }
}
</style>