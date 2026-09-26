
export interface ProductImage {
  id: number
  storage_path: string
  image_url: string
  display_order: number
  is_primary: boolean
  created_at: string
}


export interface ProductCategory {
  id: number
  name: string
  slug: string
}


export interface Product {
  id: number
  name: string
  slug: string

  category_id: number | null
  category: ProductCategory | null

  description: string | null
  price: number
  condition: string

  location: string | null
  contact_phone: string | null

  status: string

  images: ProductImage[]
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

export type ImageBackground =
  | 'white'
  | 'grey'
  | 'black'


export type ImageRotation =
  | 0
  | 90
  | 180
  | 270


export interface ImageCrop {
  x: number
  y: number
  width: number
  height: number
}


export interface ImageEditRequest {
  background: ImageBackground
  rotation: ImageRotation
  crop: ImageCrop | null
}


export interface ImageProcessResponse {
  image_base64: string
  content_type: string
}