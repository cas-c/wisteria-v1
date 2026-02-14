"use client";

import Link from "next/link";
import { useCartStore } from "@/stores/cart";
import { CartItem } from "@/components/cart/CartItem";
import { CartSummary } from "@/components/cart/CartSummary";
import { Button } from "@/components/ui/Button";

export default function CartPage() {
  const items = useCartStore((state) => state.items);
  const clearCart = useCartStore((state) => state.clearCart);

  if (items.length === 0) {
    return (
      <div className="max-w-4xl mx-auto px-4 py-16 text-center">
        <h1 className="text-2xl font-semibold text-gray-900 mb-4">
          Your cart is empty
        </h1>
        <p className="text-gray-500 mb-8">
          Browse our collection and find something you love.
        </p>
        <Button href="/products" variant="primary">
          Continue Shopping
        </Button>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <div className="flex items-center justify-between mb-8">
        <h1 className="text-2xl font-semibold text-gray-900">Your Cart</h1>
        <button
          onClick={clearCart}
          className="text-sm text-gray-500 hover:text-red-600 transition-colors"
        >
          Clear cart
        </button>
      </div>

      <div className="space-y-0">
        {items.map((product) => (
          <CartItem key={product.id} product={product} />
        ))}
      </div>

      <div className="mt-8">
        <CartSummary />
      </div>

      <div className="mt-6 flex flex-col sm:flex-row gap-4 sm:justify-between sm:items-center">
        <Link
          href="/products"
          className="text-sm text-gray-600 hover:text-gray-900 transition-colors"
        >
          &larr; Continue shopping
        </Link>
        <Button variant="primary" size="lg">
          Proceed to Checkout
        </Button>
      </div>
    </div>
  );
}
