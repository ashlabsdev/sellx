import type {
  Admin,
  LoginRequest,
  TokenResponse,
} from '../types/admin'

import { getToken } from './auth'

import type {
  Product,
  ProductCreate,
  ProductUpdate,
} from '../types/product'

import type {
  Category,
} from '../types/category'

const API_BASE_URL =
  'http://127.0.0.1:8000'


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
      const errorData = await response.json()

      if (
        typeof errorData.detail === 'string'
      ) {
        message = errorData.detail
      }
    } catch {
      // Keep the default message.
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