"use client";

import Image from "next/image";
import Link from "next/link";
import type { Product } from "@/types";
import { formatPrice } from "@/lib/utils";
import { useCartStore } from "@/stores/cart";

interface CartItemProps {
  product: Product;
}

/**
 * CartItem displays a single product in the cart with image, name, price,
 * and a remove button. Used in both CartDrawer and the cart page.
 */
export function CartItem({ product }: CartItemProps) {
  const removeItem = useCartStore((state) => state.removeItem);

  return (
    <div className="flex gap-4 py-4 border-b border-gray-200">
      {/* Product Image */}
      <Link
        href={`/products/${product.slug}`}
        className="flex-shrink-0 w-20 h-20 relative overflow-hidden rounded-md bg-gray-100"
      >
        <Image
          src={product.image_url}
          alt={product.name}
          fill
          className="object-cover"
          sizes="80px"
        />
      </Link>

      {/* Product Info */}
      <div className="flex-1 min-w-0">
        <Link
          href={`/products/${product.slug}`}
          className="font-medium text-gray-900 hover:text-gray-600 transition-colors line-clamp-2"
        >
          {product.name}
        </Link>
        <p className="mt-1 text-sm text-gray-600">
          {formatPrice(product.price_cents)}
        </p>
      </div>

      {/* Remove Button */}
      <button
        onClick={() => removeItem(product.id)}
        className="flex-shrink-0 text-sm text-red-600 hover:text-red-700 transition-colors self-start"
        aria-label={`Remove ${product.name} from cart`}
      >
        Remove
      </button>
    </div>
  );
}
