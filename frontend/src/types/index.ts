// Product condition — matches backend enum
export type ProductCondition = "new" | "like_new" | "used";

// Product category — matches backend enum
export type ProductCategory = "nendoroid" | "scale_figure" | "plush" | "goods";

// Order status — matches backend enum
export type OrderStatus = "pending" | "paid" | "shipped" | "cancelled";

export interface Product {
  id: string;
  name: string;
  slug: string;
  description: string;
  price_cents: number;
  condition: ProductCondition;
  category: ProductCategory;
  image_url: string;
  is_available: boolean;
  quantity: number;
  created_at: string;
  updated_at: string;
}

export interface OrderItem {
  id: string;
  order_id: string;
  product_id: string;
  price_cents: number;
  quantity: number;
  product?: Product;
}

export interface Order {
  id: string;
  stripe_checkout_session_id: string;
  stripe_payment_intent_id: string | null;
  status: OrderStatus;
  customer_email: string;
  customer_name: string;
  shipping_address_json: Record<string, string>;
  total_cents: number;
  items: OrderItem[];
  created_at: string;
  updated_at: string;
}

// Paginated response envelope from the API
export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  per_page: number;
  pages: number;
}
