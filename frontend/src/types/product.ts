export interface Product {
  id: number
  name: string
  slug: string
  category_id: number | null
  description: string | null
  price: number
  condition: string
  location: string | null
  contact_phone: string | null
  status: string
}

export interface ProductCreate {
  name: string
  category_id?: number | null
  description?: string | null
  price: number
  condition: string
  location?: string | null
  contact_phone?: string | null
}

export interface ProductUpdate {
  name: string
  category_id?: number | null
  description?: string | null
  price: number
  condition: string
  location?: string | null
  contact_phone?: string | null
  status: string
}