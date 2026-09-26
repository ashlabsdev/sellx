<script setup lang="ts">
import {
  computed,
  onBeforeUnmount,
  onMounted,
  ref,
} from 'vue'

import {
  useRouter,
} from 'vue-router'

import {
  deleteProductImage,
  getProductImages,
  reorderProductImages,
  updateProductImage,
  uploadProductImages,
} from '../../services/api'

import type {
  ProductImage,
} from '../../types/product'

const isReordering = ref(false)

const updatingImageId =
  ref<number | null>(null)

const imageToDelete =
  ref<ProductImage | null>(null)

const deletingImageId =
  ref<number | null>(null)

const props = defineProps<{
  productId: number
}>()

const router = useRouter()

function editImage(
  image: ProductImage,
) {
  router.push({
    name: 'admin-image-editor',

    params: {
      productId:
        props.productId.toString(),

      imageId:
        image.id.toString(),
    },
  })
}

const cameraInput =
  ref<HTMLInputElement | null>(null)

function openCamera() {
  cameraInput.value?.click()
}

function openDeleteModal(
  image: ProductImage,
) {
  imageToDelete.value = image
}

function closeDeleteModal() {
  if (deletingImageId.value !== null) {
    return
  }

  imageToDelete.value = null
}

async function moveImage(
  imageId: number,
  direction: 'left' | 'right',
) {
  if (isReordering.value) {
    return
  }

  const currentIndex =
    images.value.findIndex(
      (image) => image.id === imageId,
    )

  if (currentIndex === -1) {
    return
  }

  const targetIndex =
    direction === 'left'
      ? currentIndex - 1
      : currentIndex + 1

  if (
    targetIndex < 0 ||
    targetIndex >= images.value.length
  ) {
    return
  }

  const reordered = [
    ...images.value,
  ]

  const currentImage =
    reordered[currentIndex]

  const targetImage =
    reordered[targetIndex]

  if (!currentImage || !targetImage) {
    return
  }

  reordered[currentIndex] =
    targetImage

  reordered[targetIndex] =
    currentImage

  isReordering.value = true
  errorMessage.value = ''
  successMessage.value = ''

  try {
    images.value =
      await reorderProductImages(
        props.productId,
        reordered.map(
          (image) => image.id,
        ),
      )

    successMessage.value =
      'Image order updated.'
  } catch (error) {
    console.error(error)

    errorMessage.value =
      error instanceof Error
        ? error.message
        : 'Unable to reorder images.'

    await loadImages()
  } finally {
    isReordering.value = false
  }
}

async function confirmDelete() {
  const image = imageToDelete.value

  if (!image) {
    return
  }

  deletingImageId.value = image.id
  errorMessage.value = ''
  successMessage.value = ''

  try {
    await deleteProductImage(
      props.productId,
      image.id,
    )

    imageToDelete.value = null

    await loadImages()

    successMessage.value =
      'Image deleted successfully.'
  } catch (error) {
    console.error(error)

    errorMessage.value =
      error instanceof Error
        ? error.message
        : 'Unable to delete image.'
  } finally {
    deletingImageId.value = null
  }
}

async function makePrimary(
  image: ProductImage,
) {
  if (image.is_primary) {
    return
  }

  updatingImageId.value = image.id
  errorMessage.value = ''
  successMessage.value = ''

  try {
    await updateProductImage(
      props.productId,
      image.id,
      {
        is_primary: true,
      },
    )

    await loadImages()

    successMessage.value =
      'Primary image updated.'
  } catch (error) {
    console.error(error)

    errorMessage.value =
      error instanceof Error
        ? error.message
        : 'Unable to update primary image.'
  } finally {
    updatingImageId.value = null
  }
}

interface SelectedImage {
  id: string
  file: File
  previewUrl: string
}


const images = ref<ProductImage[]>([])
const selectedImages =
  ref<SelectedImage[]>([])

const fileInput =
  ref<HTMLInputElement | null>(null)

const isLoading = ref(true)
const isUploading = ref(false)

const errorMessage = ref('')
const successMessage = ref('')


const hasSelectedImages = computed(
  () => selectedImages.value.length > 0,
)


function createSelectedImage(
  file: File,
): SelectedImage {
  return {
    id: `${file.name}-${file.size}-${file.lastModified}`,
    file,
    previewUrl:
      URL.createObjectURL(file),
  }
}


function revokePreview(
  image: SelectedImage,
) {
  URL.revokeObjectURL(
    image.previewUrl,
  )
}


async function loadImages() {
  isLoading.value = true
  errorMessage.value = ''

  try {
    images.value =
      await getProductImages(
        props.productId,
      )
  } catch (error) {
    console.error(error)

    errorMessage.value =
      error instanceof Error
        ? error.message
        : 'Unable to load product images.'
  } finally {
    isLoading.value = false
  }
}


function openFilePicker() {
  fileInput.value?.click()
}


function handleFileSelection(
  event: Event,
) {
  const input =
    event.target as HTMLInputElement

  if (!input.files) {
    return
  }

  errorMessage.value = ''
  successMessage.value = ''

  const files =
    Array.from(input.files)

  const validFiles =
    files.filter((file) => {
      return [
        'image/jpeg',
        'image/png',
        'image/webp',
      ].includes(file.type)
    })

  if (
    validFiles.length !==
    files.length
  ) {
    errorMessage.value =
      'Only JPEG, PNG and WebP images are supported.'
  }

  for (const file of validFiles) {
    const alreadySelected =
      selectedImages.value.some(
        (selected) =>
          selected.file.name ===
            file.name &&
          selected.file.size ===
            file.size &&
          selected.file.lastModified ===
            file.lastModified,
      )

    if (alreadySelected) {
      continue
    }

    selectedImages.value.push(
      createSelectedImage(file),
    )
  }

  /*
   * Resetting allows selecting the
   * same file again after removing it.
   */
  input.value = ''
}


function removeSelectedImage(
  id: string,
) {
  const index =
    selectedImages.value.findIndex(
      (image) => image.id === id,
    )

  if (index === -1) {
    return
  }

  const image =
    selectedImages.value[index]

  if (image) {
    revokePreview(image)
  }

  selectedImages.value.splice(
    index,
    1,
  )
}


function clearSelectedImages() {
  for (
    const image
    of selectedImages.value
  ) {
    revokePreview(image)
  }

  selectedImages.value = []
}


async function uploadImages() {
  if (!selectedImages.value.length) {
    return
  }

  isUploading.value = true
  errorMessage.value = ''
  successMessage.value = ''

  try {
    const files =
      selectedImages.value.map(
        (image) => image.file,
      )

    await uploadProductImages(
      props.productId,
      files,
    )

    clearSelectedImages()

    await loadImages()

    successMessage.value =
      files.length === 1
        ? 'Image uploaded successfully.'
        : `${files.length} images uploaded successfully.`
  } catch (error) {
    console.error(error)

    errorMessage.value =
      error instanceof Error
        ? error.message
        : 'Unable to upload images.'
  } finally {
    isUploading.value = false
  }
}


onMounted(loadImages)


onBeforeUnmount(() => {
  for (
    const image
    of selectedImages.value
  ) {
    revokePreview(image)
  }
})
</script>


<template>
  <section class="image-manager">
    <div class="section-heading">
      <div>
        <h2>Product images</h2>

        <p>
          Add photos that customers will
          see on the marketplace.
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


    <input
      ref="fileInput"
      class="hidden-file-input"
      type="file"
      accept="image/jpeg,image/png,image/webp"
      multiple
      @change="handleFileSelection"
    />

    <input
      ref="cameraInput"
      class="hidden-file-input"
      type="file"
      accept="image/*"
      capture="environment"
      @change="handleFileSelection"
    />

    <div class="upload-area">
      <div class="upload-icon">
        +
      </div>

      <h3>Add product photos</h3>

      <p>
        Choose one or multiple JPEG,
        PNG or WebP images.
      </p>

      <div class="picker-actions">
        <button
          type="button"
          class="choose-button"
          :disabled="isUploading"
          @click="openFilePicker"
        >
          Choose photos
        </button>

        <button
          type="button"
          class="camera-button"
          :disabled="isUploading"
          @click="openCamera"
        >
          Take photo
        </button>
      </div>

      <small>
        On supported phones, the system
        picker can also offer the camera.
      </small>
    </div>


    <div
      v-if="hasSelectedImages"
      class="selected-section"
    >
      <div class="selected-heading">
        <div>
          <h3>
            Ready to upload
          </h3>

          <p>
            {{ selectedImages.length }}
            {{
              selectedImages.length === 1
                ? 'photo'
                : 'photos'
            }}
            selected
          </p>
        </div>

        <button
          type="button"
          class="clear-selection"
          :disabled="isUploading"
          @click="clearSelectedImages"
        >
          Clear
        </button>
      </div>


      <div class="preview-grid">
        <article
          v-for="image in selectedImages"
          :key="image.id"
          class="preview-card"
        >
          <img
            :src="image.previewUrl"
            :alt="image.file.name"
          />

          <button
            type="button"
            class="remove-preview"
            :disabled="isUploading"
            aria-label="Remove selected image"
            @click="
              removeSelectedImage(
                image.id,
              )
            "
          >
            ×
          </button>

          <div class="preview-info">
            <span>
              {{ image.file.name }}
            </span>

            <small>
              {{
                (
                  image.file.size /
                  1024 /
                  1024
                ).toFixed(2)
              }}
              MB
            </small>
          </div>
        </article>
      </div>


      <div class="upload-actions">
        <button
          type="button"
          class="upload-button"
          :disabled="isUploading"
          @click="uploadImages"
        >
          {{
            isUploading
              ? 'Uploading...'
              : `Upload ${selectedImages.length} ${
                  selectedImages.length === 1
                    ? 'photo'
                    : 'photos'
                }`
          }}
        </button>
      </div>
    </div>


    <div class="existing-section">
      <div class="existing-heading">
        <h3>Uploaded images</h3>

        <span>
          {{ images.length }}
        </span>
      </div>


      <div
        v-if="isLoading"
        class="state-card"
      >
        Loading images...
      </div>


      <div
        v-else-if="images.length === 0"
        class="state-card"
      >
        <strong>
          No images yet
        </strong>

        <p>
          Upload the first photos for
          this product.
        </p>
      </div>


      <div
        v-else
        class="existing-grid"
      >
        <article
          v-for="(image, index) in images"
          :key="image.id"
          class="existing-card"
        >
          <div class="existing-image">
            <img
              :src="image.image_url"
              alt="Product image"
            />

            <span
              v-if="image.is_primary"
              class="primary-badge"
            >
              Primary
            </span>

            <button
              type="button"
              class="edit-image-button"
              @click="editImage(image)"
            >
              Edit image
            </button>
          </div>

          <div class="image-details">
            <div class="order-actions">
              <button
                type="button"
                class="order-button"
                :disabled="
                  index === 0 ||
                  isReordering
                "
                @click="
                  moveImage(
                    image.id,
                    'left',
                  )
                "
              >
                ← Left
              </button>

              <button
                type="button"
                class="order-button"
                :disabled="
                  index === images.length - 1 ||
                  isReordering
                "
                @click="
                  moveImage(
                    image.id,
                    'right',
                  )
                "
              >
                Right →
              </button>
            </div>

            <div class="image-meta">
              <span>
                Order
                {{ image.display_order }}
              </span>
            </div>

            <button
              v-if="!image.is_primary"
              type="button"
              class="primary-action"
              :disabled="
                updatingImageId === image.id
              "
              @click="makePrimary(image)"
            >
              {{
                updatingImageId === image.id
                  ? 'Updating...'
                  : 'Make primary'
              }}
            </button>
           
            <span
              v-else
              class="primary-label"
            >
              Primary image
            </span>

            <button
              type="button"
              class="delete-image-button"
              @click="openDeleteModal(image)"
            >
              Delete image
            </button>

          </div>
        </article>
      </div>
    </div>
  </section>

  <Teleport to="body">
    <div
      v-if="imageToDelete"
      class="modal-backdrop"
      @click.self="closeDeleteModal"
    >
      <div
        class="delete-modal"
        role="dialog"
        aria-modal="true"
        aria-labelledby="image-delete-title"
      >
        <div class="delete-icon">
          !
        </div>

        <h2 id="image-delete-title">
          Delete image?
        </h2>

        <p>
          This photo will be permanently
          removed from the product.
        </p>

        <div class="delete-preview">
          <img
            :src="imageToDelete.image_url"
            alt="Image to delete"
          />
        </div>

        <p class="delete-warning">
          This action cannot be undone.
        </p>

        <div class="modal-actions">
          <button
            type="button"
            class="modal-cancel"
            :disabled="
              deletingImageId !== null
            "
            @click="closeDeleteModal"
          >
            Cancel
          </button>

          <button
            type="button"
            class="modal-delete"
            :disabled="
              deletingImageId !== null
            "
            @click="confirmDelete"
          >
            {{
              deletingImageId !== null
                ? 'Deleting...'
                : 'Delete image'
            }}
          </button>
        </div>
      </div>
    </div>
  </Teleport>
</template>


<style scoped>
.edit-image-button {
  width: 100%;
  border: 1px solid #d7dce5;
  border-radius: 10px;
  padding: 0.7rem 0.9rem;
  background: #ffffff;
  color: #202735;
  font-weight: 700;
  cursor: pointer;
  transition:
    border-color 0.2s ease,
    background 0.2s ease,
    transform 0.2s ease;
}

.edit-image-button:hover {
  background: #f7f8fa;
  border-color: #aeb6c4;
  transform: translateY(-1px);
}

.order-actions {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 6px;
}

.order-button {
  min-height: 32px;
  border: 1px solid #ddd;
  border-radius: 7px;
  background: #fff;
  color: #444;
  cursor: pointer;
  font-size: 11px;
  font-weight: 700;
}

.order-button:hover:not(:disabled) {
  border-color: #999;
  background: #f8f8f8;
}

.order-button:disabled {
  cursor: not-allowed;
  opacity: 0.4;
}

.modal-backdrop {
  display: grid;
  position: fixed;
  z-index: 1100;
  inset: 0;
  place-items: center;
  padding: 20px;
  background: rgba(0, 0, 0, 0.48);
}

.delete-modal {
  width: 100%;
  max-width: 430px;
  padding: 26px;
  border-radius: 16px;
  background: #fff;
  box-shadow:
    0 24px 70px
    rgba(0, 0, 0, 0.22);
}

.delete-icon {
  display: grid;
  width: 42px;
  height: 42px;
  margin-bottom: 16px;
  place-items: center;
  border-radius: 50%;
  background: #fff0f0;
  color: #b42318;
  font-size: 20px;
  font-weight: 800;
}

.delete-modal h2 {
  margin: 0 0 8px;
}

.delete-modal > p {
  margin: 0;
  color: #666;
  line-height: 1.6;
}

.delete-preview {
  width: 100px;
  margin-top: 18px;
  overflow: hidden;
  border-radius: 9px;
}

.delete-preview img {
  display: block;
  width: 100%;
  aspect-ratio: 1;
  object-fit: cover;
}

.delete-warning {
  margin-top: 14px !important;
  color: #b42318 !important;
  font-size: 13px;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 24px;
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

.delete-image-button {
  min-height: 34px;
  border: 1px solid #f0c5c5;
  border-radius: 7px;
  background: #fff;
  color: #b42318;
  cursor: pointer;
  font-size: 12px;
  font-weight: 700;
}

.delete-image-button:hover {
  background: #fff5f5;
}

.image-details {
  display: grid;
  gap: 8px;
  padding: 10px;
}

.image-details .image-meta {
  padding: 0;
}

.primary-action {
  min-height: 34px;
  border: 1px solid #ddd;
  border-radius: 7px;
  background: #fff;
  color: #333;
  cursor: pointer;
  font-size: 12px;
  font-weight: 700;
}

.primary-action:hover {
  border-color: #999;
}

.primary-action:disabled {
  cursor: not-allowed;
  opacity: 0.5;
}

.primary-label {
  color: #18753c;
  font-size: 12px;
  font-weight: 700;
}

.image-manager {
  display: grid;
  gap: 22px;
  margin-top: 22px;
}

.picker-actions {
  display: flex;
  justify-content: center;
  gap: 10px;
  flex-wrap: wrap;
}

.camera-button {
  min-height: 42px;
  padding: 0 18px;
  border: 1px solid #d5d5d5;
  border-radius: 9px;
  background: #fff;
  color: #222;
  cursor: pointer;
  font-weight: 700;
}

.camera-button:disabled {
  cursor: not-allowed;
  opacity: 0.55;
}

.section-heading h2,
.selected-heading h3,
.existing-heading h3 {
  margin: 0;
}

.section-heading p,
.selected-heading p {
  margin: 6px 0 0;
  color: #777;
  font-size: 14px;
}

.message {
  padding: 12px 14px;
  border-radius: 9px;
  font-size: 14px;
}

.error-message {
  border: 1px solid #f3c7c7;
  background: #fff5f5;
  color: #b42318;
}

.success-message {
  border: 1px solid #bfe3c9;
  background: #f1fbf4;
  color: #18753c;
}

.hidden-file-input {
  display: none;
}

.upload-area {
  padding: 38px 24px;
  border: 2px dashed #d7d7d7;
  border-radius: 14px;
  background: #fff;
  text-align: center;
}

.upload-icon {
  display: grid;
  width: 48px;
  height: 48px;
  margin: 0 auto 15px;
  place-items: center;
  border-radius: 50%;
  background: #f2f2f2;
  font-size: 26px;
}

.upload-area h3 {
  margin: 0 0 7px;
}

.upload-area p {
  margin: 0 0 18px;
  color: #777;
}

.upload-area small {
  display: block;
  margin-top: 12px;
  color: #999;
}

.choose-button,
.upload-button {
  min-height: 42px;
  padding: 0 18px;
  border: 0;
  border-radius: 9px;
  background: #111;
  color: #fff;
  cursor: pointer;
  font-weight: 700;
}

.choose-button:disabled,
.upload-button:disabled {
  cursor: not-allowed;
  opacity: 0.55;
}

.selected-section,
.existing-section {
  padding: 22px;
  border: 1px solid #e5e5e5;
  border-radius: 14px;
  background: #fff;
}

.selected-heading,
.existing-heading {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
  margin-bottom: 18px;
}

.existing-heading span {
  display: grid;
  min-width: 27px;
  height: 27px;
  place-items: center;
  border-radius: 999px;
  background: #f1f1f1;
  font-size: 12px;
  font-weight: 700;
}

.clear-selection {
  border: 0;
  background: transparent;
  color: #666;
  cursor: pointer;
  font-weight: 600;
}

.preview-grid,
.existing-grid {
  display: grid;
  grid-template-columns:
    repeat(4, minmax(0, 1fr));
  gap: 14px;
}

.preview-card,
.existing-card {
  overflow: hidden;
  border: 1px solid #e5e5e5;
  border-radius: 10px;
  background: #fff;
}

.preview-card {
  position: relative;
}

.preview-card img,
.existing-image img {
  display: block;
  width: 100%;
  aspect-ratio: 1;
  object-fit: cover;
}

.remove-preview {
  display: grid;
  position: absolute;
  top: 8px;
  right: 8px;
  width: 30px;
  height: 30px;
  place-items: center;
  border: 0;
  border-radius: 50%;
  background: rgba(0, 0, 0, 0.72);
  color: #fff;
  cursor: pointer;
  font-size: 20px;
}

.preview-info,
.image-meta {
  padding: 10px;
}

.preview-info span {
  display: block;
  overflow: hidden;
  margin-bottom: 4px;
  font-size: 12px;
  font-weight: 600;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.preview-info small,
.image-meta {
  color: #888;
  font-size: 11px;
}

.upload-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 18px;
}

.existing-image {
  position: relative;
}

.primary-badge {
  position: absolute;
  top: 8px;
  left: 8px;
  padding: 5px 8px;
  border-radius: 999px;
  background: #111;
  color: #fff;
  font-size: 10px;
  font-weight: 700;
}

.state-card {
  padding: 30px;
  border-radius: 10px;
  background: #f8f8f8;
  color: #777;
  text-align: center;
}

.state-card strong {
  display: block;
  margin-bottom: 6px;
  color: #333;
}

.state-card p {
  margin: 0;
}

@media (max-width: 900px) {
  .preview-grid,
  .existing-grid {
    grid-template-columns:
      repeat(3, minmax(0, 1fr));
  }
}

@media (max-width: 650px) {
  .preview-grid,
  .existing-grid {
    grid-template-columns:
      repeat(2, minmax(0, 1fr));
  }

  .selected-section,
  .existing-section {
    padding: 16px;
  }
}
</style>