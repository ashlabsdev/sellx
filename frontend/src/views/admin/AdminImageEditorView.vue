<script setup lang="ts">
import {
  computed,
  nextTick,
  onBeforeUnmount,
  onMounted,
  ref,
} from 'vue'

import Cropper from 'cropperjs'
import 'cropperjs/dist/cropper.css'

import {
  useRoute,
  useRouter,
} from 'vue-router'

import {
  getProductImages,
  previewProductImageEdit,
} from '../../services/api'

import type {
  ImageBackground,
  ImageCrop,
  ImageProcessResponse,
  ImageRotation,
  ProductImage,
} from '../../types/product'

const route = useRoute()
const router = useRouter()


const productId = Number(
  route.params.productId,
)

const imageId = Number(
  route.params.imageId,
)


const image =
  ref<ProductImage | null>(null)

const preview =
  ref<ImageProcessResponse | null>(
    null,
  )


const background =
  ref<ImageBackground>('white')

const rotation =
  ref<ImageRotation>(0)

const cropImageElement =
  ref<HTMLImageElement | null>(null)

const crop =
  ref<ImageCrop | null>(null)

const isCropMode = ref(false)

let cropper: Cropper | null = null

async function startCrop() {
  if (!image.value) {
    return
  }

  isCropMode.value = true
  preview.value = null
  crop.value = null

  await nextTick()

  if (!cropImageElement.value) {
    return
  }

  destroyCropper()

  cropper = new Cropper(
    cropImageElement.value,
    {
      viewMode: 1,

      dragMode: 'crop',

      autoCropArea: 0.8,

      responsive: true,

      restore: false,

      guides: true,

      center: true,

      highlight: true,

      background: false,

      movable: false,

      zoomable: false,

      rotatable: false,

      scalable: false,

      cropBoxMovable: true,

      cropBoxResizable: true,
    },
  )
}

function applyCrop() {
  if (!cropper) {
    return
  }

  const data =
    cropper.getData(true)

  const x = Math.max(
    0,
    Math.round(data.x),
  )

  const y = Math.max(
    0,
    Math.round(data.y),
  )

  const width = Math.max(
    1,
    Math.round(data.width),
  )

  const height = Math.max(
    1,
    Math.round(data.height),
  )

  crop.value = {
    x,
    y,
    width,
    height,
  }

  isCropMode.value = false

  destroyCropper()
}

function cancelCrop() {
  isCropMode.value = false

  destroyCropper()
}

function clearCrop() {
  crop.value = null
  preview.value = null
}

function destroyCropper() {
  if (!cropper) {
    return
  }

  cropper.destroy()
  cropper = null
}

const isLoading = ref(true)
const isProcessing = ref(false)

const errorMessage = ref('')


const previewUrl = computed(() => {
  if (!preview.value) {
    return null
  }

  return (
    `data:${preview.value.content_type};base64,` +
    preview.value.image_base64
  )
})


async function loadImage() {
  isLoading.value = true
  errorMessage.value = ''

  try {
    const images =
      await getProductImages(
        productId,
      )

    const selectedImage =
      images.find(
        (item) =>
          item.id === imageId,
      )

    if (!selectedImage) {
      throw new Error(
        'Product image not found.',
      )
    }

    image.value = selectedImage
  } catch (error) {
    console.error(error)

    errorMessage.value =
      error instanceof Error
        ? error.message
        : 'Unable to load image.'
  } finally {
    isLoading.value = false
  }
}


async function generatePreview() {
  if (!image.value) {
    return
  }

  isProcessing.value = true
  errorMessage.value = ''

  try {
    preview.value =
      await previewProductImageEdit(
        productId,
        imageId,
        {
          background:
            background.value,

          rotation:
            rotation.value,

          crop: crop.value,
        },
      )
  } catch (error) {
    console.error(error)

    errorMessage.value =
      error instanceof Error
        ? error.message
        : 'Unable to process image.'
  } finally {
    isProcessing.value = false
  }
}


function rotateLeft() {
  const next =
    rotation.value - 90

  rotation.value =
    (
      next < 0
        ? 270
        : next
    ) as ImageRotation

  crop.value = null
  preview.value = null

  destroyCropper()
  isCropMode.value = false
}

function rotateRight() {
  rotation.value =
    (
      (rotation.value + 90) %
      360
    ) as ImageRotation

  crop.value = null
  preview.value = null

  destroyCropper()
  isCropMode.value = false
}

function resetEditor() {
  destroyCropper()

  background.value = 'white'
  rotation.value = 0

  crop.value = null
  preview.value = null

  isCropMode.value = false
  errorMessage.value = ''
}


function goBack() {
  router.push({
    name: 'admin-product-edit',

    params: {
      id: productId.toString(),
    },
  })
}


onMounted(loadImage)
</script>


<template>
  <section class="editor-page">
    <div class="editor-header">
      <div>
        <button
          type="button"
          class="back-button"
          @click="goBack"
        >
          ← Back to product
        </button>

        <h1>
          SellX Image Editor
        </h1>

        <p>
          Prepare product photos for
          the marketplace.
        </p>
      </div>
    </div>


    <div
      v-if="errorMessage"
      class="error-message"
    >
      {{ errorMessage }}
    </div>


    <div
      v-if="isLoading"
      class="state-card"
    >
      Loading image...
    </div>


    <div
      v-else-if="image"
      class="editor-layout"
    >
      <div class="preview-panel">
        <div class="preview-heading">
          <div>
            <h2>
              Image preview
            </h2>

            <p>
              Preview your edits before
              saving.
            </p>
          </div>
        </div>


        <div
          class="image-stage"
          :class="{
            'crop-mode': isCropMode,
          }"
        >
          <img
            v-if="isCropMode"
            ref="cropImageElement"
            :src="image.image_url"
            alt="Crop product image"
            class="crop-source-image"
          />

          <img
            v-else
            :src="
              previewUrl ||
              image.image_url
            "
            alt="Product image preview"
            class="preview-image"
          />
        </div>

        <div
          v-if="isCropMode"
          class="crop-actions"
        >
          <div>
            <strong>
              Crop mode
            </strong>

            <p>
              Drag and resize the box around
              the area you want to keep.
            </p>
          </div>

          <div class="crop-action-buttons">
            <button
              type="button"
              class="cancel-crop-button"
              @click="cancelCrop"
            >
              Cancel
            </button>

            <button
              type="button"
              class="apply-crop-button"
              @click="applyCrop"
            >
              Apply crop
            </button>
          </div>
        </div>


        <div
          v-if="!isCropMode"
          class="preview-status"
        >
          <span
            v-if="previewUrl"
            class="edited-badge"
          >
            Edited preview
          </span>

          <span v-else>
            Original image
          </span>
        </div>
      </div>


      <aside class="controls-panel">
        <div class="control-section">
          <h3>
            Background
          </h3>

          <p>
            Remove the original
            background and replace it.
          </p>


          <div class="background-options">
            <button
              type="button"
              :class="{
                selected:
                  background === 'white',
              }"
              @click="
                background = 'white';
                preview = null
              "
            >
              <span
                class="color-circle white"
              />

              White
            </button>


            <button
              type="button"
              :class="{
                selected:
                  background === 'grey',
              }"
              @click="
                background = 'grey';
                preview = null
              "
            >
              <span
                class="color-circle grey"
              />

              Grey
            </button>


            <button
              type="button"
              :class="{
                selected:
                  background === 'black',
              }"
              @click="
                background = 'black';
                preview = null
              "
            >
              <span
                class="color-circle black"
              />

              Black
            </button>
          </div>
        </div>


        <div class="control-section">
          <h3>
            Rotation
          </h3>

          <div class="rotation-actions">
            <button
              type="button"
              @click="rotateLeft"
            >
              ↶ Rotate left
            </button>

            <button
              type="button"
              @click="rotateRight"
            >
              Rotate right ↷
            </button>
          </div>

          <p class="rotation-value">
            {{ rotation }}°
          </p>
        </div>


        <div class="control-section">
          <h3>
            Crop
          </h3>

          <p>
            Select the part of the
            product photo you want to keep.
          </p>

          <button
            v-if="!crop"
            type="button"
            class="crop-button"
            :disabled="
              isProcessing ||
              isCropMode
            "
            @click="startCrop"
          >
            Crop image
          </button>

          <div
            v-else
            class="crop-summary"
          >
            <div>
              <strong>
                Crop applied
              </strong>

              <span>
                {{ crop.width }}
                ×
                {{ crop.height }}
                px
              </span>
            </div>

            <div class="crop-summary-actions">
              <button
                type="button"
                @click="startCrop"
              >
                Change
              </button>

              <button
                type="button"
                @click="clearCrop"
              >
                Clear
              </button>
            </div>
          </div>
        </div>

        <div class="edit-summary">
          <h3>
            Current edits
          </h3>

          <div>
            <span>Background</span>

            <strong>
              {{ background }}
            </strong>
          </div>

          <div>
            <span>Rotation</span>

            <strong>
              {{ rotation }}°
            </strong>
          </div>

          <div>
            <span>Crop</span>

            <strong>
              {{
                crop
                  ? `${crop.width} × ${crop.height}`
                  : 'None'
              }}
            </strong>
          </div>
        </div>

        <div class="editor-actions">
          <button
            type="button"
            class="reset-button"
            :disabled="
              isProcessing ||
              isCropMode
            "
            @click="resetEditor"
          >
            Reset
          </button>

          <button
            type="button"
            class="preview-button"
            :disabled="
              isProcessing ||
              isCropMode
            "
            @click="generatePreview"
          >
            {{
              isProcessing
                ? 'Processing...'
                : 'Generate preview'
            }}
          </button>
        </div>
      </aside>
    </div>
    onBeforeUnmount(() => {
      destroyCropper()
    })
  </section>
</template>


<style scoped>
.crop-button {
  width: 100%;
  border: 1px solid #dfe3ea;
  border-radius: 10px;
  padding: 0.75rem;
  background: #ffffff;
  font-weight: 700;
  cursor: pointer;
}

.crop-button:hover {
  background: #f7f8fa;
}

.crop-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.crop-source-image {
  display: block;
  max-width: 100%;
}

.crop-mode {
  display: block;
  min-height: auto;
  padding: 1rem;
}

.crop-actions {
  display: flex;
  justify-content: space-between;
  gap: 1rem;
  align-items: center;

  margin-top: 1rem;
  padding: 1rem;

  border: 1px solid #e1e5ec;
  border-radius: 12px;

  background: #f8f9fb;
}

.crop-actions p {
  margin: 0.25rem 0 0;
  color: #747b89;
  font-size: 0.9rem;
}

.crop-action-buttons {
  display: flex;
  gap: 0.65rem;
}

.cancel-crop-button,
.apply-crop-button {
  border-radius: 9px;
  padding: 0.7rem 1rem;
  font-weight: 700;
  cursor: pointer;
}

.cancel-crop-button {
  border: 1px solid #d8dde6;
  background: #ffffff;
}

.apply-crop-button {
  border: 0;
  background: #222938;
  color: #ffffff;
}

.crop-summary {
  padding: 0.8rem;
  border-radius: 10px;
  background: #f6f7f9;
}

.crop-summary > div:first-child {
  display: flex;
  justify-content: space-between;
  gap: 1rem;
}

.crop-summary span {
  color: #737b8b;
}

.crop-summary-actions {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.5rem;
  margin-top: 0.7rem;
}

.crop-summary-actions button {
  border: 1px solid #dfe3ea;
  border-radius: 8px;
  padding: 0.55rem;
  background: #ffffff;
  cursor: pointer;
}

.edit-summary {
  margin-bottom: 1.25rem;
  padding: 1rem;

  border-radius: 12px;
  background: #f7f8fa;
}

.edit-summary h3 {
  margin: 0 0 0.8rem;
}

.edit-summary > div {
  display: flex;
  justify-content: space-between;
  gap: 1rem;

  padding: 0.35rem 0;

  font-size: 0.9rem;
}

.edit-summary span {
  color: #737b8b;
}

.edit-summary strong {
  text-transform: capitalize;
}

@media (max-width: 600px) {
  .crop-actions {
    flex-direction: column;
    align-items: stretch;
  }

  .crop-action-buttons {
    display: grid;
    grid-template-columns: 1fr 1fr;
  }
}

.editor-page {
  width: 100%;
}

.editor-header {
  margin-bottom: 1.5rem;
}

.editor-header h1 {
  margin: 0.6rem 0 0.25rem;
  font-size: 2rem;
}

.editor-header p {
  margin: 0;
  color: #687083;
}

.back-button {
  border: 0;
  padding: 0;
  background: transparent;
  color: #5865d8;
  font-weight: 700;
  cursor: pointer;
}

.editor-layout {
  display: grid;
  grid-template-columns:
    minmax(0, 1fr)
    340px;
  gap: 1.5rem;
  align-items: start;
}

.preview-panel,
.controls-panel {
  border: 1px solid #e1e5ec;
  border-radius: 18px;
  background: #ffffff;
}

.preview-panel {
  padding: 1.25rem;
}

.preview-heading h2 {
  margin: 0;
}

.preview-heading p {
  margin: 0.35rem 0 0;
  color: #747b89;
}

.image-stage {
  min-height: 520px;
  margin-top: 1.25rem;
  border-radius: 14px;
  background:
    linear-gradient(
      45deg,
      #eceff3 25%,
      transparent 25%
    ),
    linear-gradient(
      -45deg,
      #eceff3 25%,
      transparent 25%
    ),
    linear-gradient(
      45deg,
      transparent 75%,
      #eceff3 75%
    ),
    linear-gradient(
      -45deg,
      transparent 75%,
      #eceff3 75%
    );
  background-size: 24px 24px;
  background-position:
    0 0,
    0 12px,
    12px -12px,
    -12px 0;

  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.image-stage img {
  display: block;
  max-width: 100%;
  max-height: 620px;
  object-fit: contain;
}

.preview-status {
  margin-top: 1rem;
  color: #707789;
  font-size: 0.9rem;
}

.edited-badge {
  display: inline-flex;
  border-radius: 999px;
  padding: 0.35rem 0.7rem;
  background: #ecf8ef;
  color: #267a3e;
  font-weight: 700;
}

.controls-panel {
  padding: 1.25rem;
}

.control-section {
  padding-bottom: 1.4rem;
  margin-bottom: 1.4rem;
  border-bottom: 1px solid #eceef2;
}

.control-section h3 {
  margin: 0 0 0.4rem;
}

.control-section p {
  margin: 0 0 1rem;
  color: #737b8b;
  font-size: 0.9rem;
}

.background-options {
  display: grid;
  gap: 0.65rem;
}

.background-options button {
  display: flex;
  align-items: center;
  gap: 0.7rem;

  width: 100%;
  padding: 0.75rem;

  border: 1px solid #dfe3ea;
  border-radius: 10px;

  background: #ffffff;
  cursor: pointer;
}

.background-options button.selected {
  border-color: #5965dc;
  box-shadow:
    0 0 0 2px
    rgba(89, 101, 220, 0.12);
}

.color-circle {
  width: 22px;
  height: 22px;
  border-radius: 50%;
  border: 1px solid #cfd4dc;
}

.color-circle.white {
  background: #ffffff;
}

.color-circle.grey {
  background: #808080;
}

.color-circle.black {
  background: #000000;
}

.rotation-actions {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.65rem;
}

.rotation-actions button {
  border: 1px solid #dfe3ea;
  border-radius: 10px;
  padding: 0.7rem;
  background: #ffffff;
  cursor: pointer;
}

.rotation-value {
  margin-top: 0.8rem !important;
  text-align: center;
  font-weight: 700;
}

.editor-actions {
  display: grid;
  gap: 0.75rem;
}

.reset-button,
.preview-button {
  border-radius: 11px;
  padding: 0.85rem 1rem;
  font-weight: 700;
  cursor: pointer;
}

.reset-button {
  border: 1px solid #dfe3ea;
  background: #ffffff;
}

.preview-button {
  border: 0;
  background: #222938;
  color: #ffffff;
}

.preview-button:disabled,
.reset-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.error-message {
  margin-bottom: 1rem;
  padding: 0.9rem 1rem;
  border-radius: 10px;
  background: #fff0f0;
  color: #a33434;
}

.state-card {
  padding: 2rem;
  border: 1px solid #e1e5ec;
  border-radius: 16px;
  background: #ffffff;
  text-align: center;
}

@media (max-width: 900px) {
  .editor-layout {
    grid-template-columns: 1fr;
  }

  .image-stage {
    min-height: 360px;
  }
}
</style>