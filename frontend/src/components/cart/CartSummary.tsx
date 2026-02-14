"use client";

import { formatPrice } from "@/lib/utils";
import { useCartStore, selectCartTotal, selectCartItemCount } from "@/stores/cart";

/**
 * CartSummary displays the item count and subtotal.
 * Used in both CartDrawer and the cart page.
 */
export function CartSummary() {
  const itemCount = useCartStore(selectCartItemCount);
  const total = useCartStore(selectCartTotal);

  return (
    <div className="border-t border-gray-200 pt-4 space-y-2">
      <div className="flex justify-between text-sm text-gray-600">
        <span>
          {itemCount} {itemCount === 1 ? "item" : "items"}
        </span>
        <span>Subtotal</span>
      </div>
      <div className="flex justify-between text-lg font-semibold text-gray-900">
        <span></span>
        <span>{formatPrice(total)}</span>
      </div>
      <p className="text-xs text-gray-500">
        Shipping and taxes calculated at checkout
      </p>
    </div>
  );
}
