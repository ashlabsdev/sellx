import type {
  Admin,
  LoginRequest,
  TokenResponse,
} from '../types/admin'

import { getToken } from './auth'


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
    throw new Error(
      `API request failed with status ${response.status}`,
    )
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

  const queryString = query.toString()

  const endpoint = queryString
    ? `/api/products?${queryString}`
    : '/api/products'

  return request<
    import('../types/product').Product[]
  >(endpoint)
}


export async function getProduct(
  productId: number,
) {
  return request<
    import('../types/product').Product
  >(`/api/products/${productId}`)
}


export async function getCategories() {
  return request<
    import('../types/category').Category[]
  >('/api/categories')
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