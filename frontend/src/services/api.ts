import type {
  Admin,
  LoginRequest,
  TokenResponse,
} from '../types/admin'

import { getToken } from './auth'

import type {
  ImageEditRequest,
  ImageProcessResponse,
  Product,
  ProductCreate,
  ProductImage,
  ProductUpdate,
  ImageBackground,
  ImageCrop,
  ImageRotation,
} from '../types/product'

import type {
  Category,
  CategoryCreate,
  CategoryUpdate,
} from '../types/category'

// const API_BASE_URL = (
//   import.meta.env.VITE_API_BASE_URL ||
//   'http://127.0.0.1:8000'
// ).replace(/\/+$/, '')

const API_BASE_URL = (
'http://127.0.0.1:8000'
).replace(/\/+$/, '')

export async function getProductImages(
  productId: number,
) {
  return request<ProductImage[]>(
    `/api/products/${productId}/images`,
  )
}

export async function reorderProductImages(
  productId: number,
  imageIds: number[],
) {
  return request<ProductImage[]>(
    `/api/products/${productId}/images/reorder`,
    {
      method: 'PUT',
      body: JSON.stringify({
        image_ids: imageIds,
      }),
    },
    true,
  )
}

export async function uploadProductImages(
  productId: number,
  files: File[],
) {
  const formData = new FormData()

  for (const file of files) {
    formData.append('files', file)
  }

  return request<ProductImage[]>(
    `/api/products/${productId}/images/upload-multiple`,
    {
      method: 'POST',
      body: formData,
    },
    true,
  )
}


export async function updateProductImage(
  productId: number,
  imageId: number,
  data: {
    display_order?: number
    is_primary?: boolean
  },
) {
  return request<ProductImage>(
    `/api/products/${productId}/images/${imageId}`,
    {
      method: 'PUT',
      body: JSON.stringify(data),
    },
    true,
  )
}

export async function previewProductImageEdit(
  productId: number,
  imageId: number,
  data: ImageEditRequest,
) {
  return request<ImageProcessResponse>(
    `/api/products/${productId}/images/${imageId}/preview-edit`,
    {
      method: 'POST',
      body: JSON.stringify(data),
    },
    true,
  )
}

export async function saveProductImageEdit(
  productId: number,
  imageId: number,
  data: {
    background: ImageBackground
    rotation: ImageRotation
    crop: ImageCrop | null
  },
) {
  return request<ProductImage>(
    `/api/products/${productId}/images/${imageId}/save-edit`,
    {
      method: 'POST',
      body: JSON.stringify(data),
    },
    true,
  )
}

export async function deleteProductImage(
  productId: number,
  imageId: number,
) {
  return request<{
    message: string
  }>(
    `/api/products/${productId}/images/${imageId}`,
    {
      method: 'DELETE',
    },
    true,
  )
}


async function request<T>(
  endpoint: string,
  options: RequestInit = {},
  authenticated = false,
): Promise<T> {
  const headers = new Headers(
    options.headers,
  )

  if (
    options.body &&
    !(options.body instanceof FormData) &&
    !headers.has('Content-Type')
  ) {
    headers.set(
      'Content-Type',
      'application/json',
    )
  }

  if (authenticated) {
    const token = getToken()

    if (token) {
      headers.set(
        'Authorization',
        `Bearer ${token}`,
      )
    }
  }

  const response = await fetch(
    `${API_BASE_URL}${endpoint}`,
    {
      ...options,
      headers,
    },
  )

  if (!response.ok) {
    let message =
      `API request failed with status ${response.status}`

    try {
      const errorData =
        await response.json()

      if (
        typeof errorData.detail ===
        'string'
      ) {
        message =
          errorData.detail
      } else if (
        errorData.detail?.message
      ) {
        const details =
          Array.isArray(
            errorData.detail.errors,
          )
            ? errorData.detail.errors
            : []

        message = [
          errorData.detail.message,
          ...details,
        ].join('\n')
      }
    } catch {
      // Keep fallback message.
    }

    throw new Error(message)
  }

  return response.json()
}


export async function healthCheck() {
  return request<{ status: string }>(
    '/api/health',
  )
}


export async function getProducts(params?: {
  search?: string
  category_id?: number
  status?: string
  page?: number
  page_size?: number
}) {
  const query = new URLSearchParams()

  if (params?.search) {
    query.set(
      'search',
      params.search,
    )
  }

  if (
    params?.category_id !== undefined
  ) {
    query.set(
      'category_id',
      params.category_id.toString(),
    )
  }

  if (params?.status) {
    query.set(
      'status',
      params.status,
    )
  }

  if (params?.page !== undefined) {
    query.set(
      'page',
      params.page.toString(),
    )
  }

  if (
    params?.page_size !== undefined
  ) {
    query.set(
      'page_size',
      params.page_size.toString(),
    )
  }

  const queryString = query.toString()

  const endpoint = queryString
    ? `/api/products?${queryString}`
    : '/api/products'

  return request<Product[]>(
    endpoint,
  )
}

export async function getProduct(
  productId: number,
) {
  return request<Product>(
    `/api/products/${productId}`,
  )
}


export async function getCategories() {
  return request<Category[]>(
    '/api/categories',
  )
}

export async function createCategory(
  data: CategoryCreate,
) {
  return request<Category>(
    '/api/categories',
    {
      method: 'POST',
      body: JSON.stringify(data),
    },
    true,
  )
}


export async function updateCategory(
  categoryId: number,
  data: CategoryUpdate,
) {
  return request<Category>(
    `/api/categories/${categoryId}`,
    {
      method: 'PUT',
      body: JSON.stringify(data),
    },
    true,
  )
}


export async function deleteCategory(
  categoryId: number,
) {
  return request<{
    message: string
  }>(
    `/api/categories/${categoryId}`,
    {
      method: 'DELETE',
    },
    true,
  )
}

export async function loginAdmin(
  data: LoginRequest,
) {
  return request<TokenResponse>(
    '/api/auth/login',
    {
      method: 'POST',
      body: JSON.stringify(data),
    },
  )
}


export async function getCurrentAdmin() {
  return request<Admin>(
    '/api/auth/me',
    {},
    true,
  )
}

export async function createProduct(
  data: ProductCreate,
) {
  return request<Product>(
    '/api/products',
    {
      method: 'POST',
      body: JSON.stringify(data),
    },
    true,
  )
}


export async function updateProduct(
  productId: number,
  data: ProductUpdate,
) {
  return request<Product>(
    `/api/products/${productId}`,
    {
      method: 'PUT',
      body: JSON.stringify(data),
    },
    true,
  )
}


export async function deleteProduct(
  productId: number,
) {
  return request<{
    message: string
  }>(
    `/api/products/${productId}`,
    {
      method: 'DELETE',
    },
    true,
  )
}