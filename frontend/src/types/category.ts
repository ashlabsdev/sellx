export interface Category {
  id: number
  name: string
  slug: string
  description: string | null
  is_active: boolean
}

export interface CategoryCreate {
  name: string
  description?: string | null
}

export interface CategoryUpdate {
  name: string
  description?: string | null
  is_active: boolean
}