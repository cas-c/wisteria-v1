"use client";

import { useEffect } from "react";
import Link from "next/link";
import { useCartStore } from "@/stores/cart";
import { CartItem } from "./CartItem";
import { CartSummary } from "./CartSummary";
import { Button } from "@/components/ui/Button";

/**
 * CartDrawer is a slide-out panel from the right side showing cart contents.
 * Drawer state persists across page refreshes.
 * Users can freely navigate and browse while the drawer is open.
 */
export function CartDrawer() {
  const items = useCartStore((state) => state.items);
  const isOpen = useCartStore((state) => state.isDrawerOpen);
  const closeDrawer = useCartStore((state) => state.closeDrawer);

  // Close drawer on Escape key
  useEffect(() => {
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === "Escape" && isOpen) {
        closeDrawer();
      }
    };
    document.addEventListener("keydown", handleEscape);
    return () => document.removeEventListener("keydown", handleEscape);
  }, [isOpen, closeDrawer]);

  return (
    <div
      className={`fixed top-0 right-0 h-full w-full max-w-md bg-white shadow-xl z-40 transform transition-transform duration-300 ease-in-out ${
        isOpen ? "translate-x-0" : "translate-x-full"
      }`}
    >
      <div className="flex flex-col h-full">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-gray-200">
          <h2 className="text-lg font-semibold text-gray-900">Your Cart</h2>
          <button
            onClick={closeDrawer}
            className="text-gray-400 hover:text-gray-600 transition-colors"
            aria-label="Close cart"
          >
            <svg
              className="w-6 h-6"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M6 18L18 6M6 6l12 12"
              />
            </svg>
          </button>
        </div>

        {/* Cart Items */}
        <div className="flex-1 overflow-y-auto p-6">
          {items.length === 0 ? (
            <div className="text-center py-12">
              <p className="text-gray-500">Your cart is empty</p>
              <Link
                href="/products"
                onClick={closeDrawer}
                className="inline-block mt-4 text-sm text-gray-900 hover:text-gray-600 underline"
              >
                Continue shopping
              </Link>
            </div>
          ) : (
            <div className="space-y-0 -mx-6 px-6">
              {items.map((product) => (
                <CartItem key={product.id} product={product} />
              ))}
            </div>
          )}
        </div>

        {/* Footer with Summary and View Cart Link */}
        {items.length > 0 && (
          <div className="border-t border-gray-200 p-6 space-y-4">
            <CartSummary />
            <Link href="/cart" onClick={closeDrawer}>
              <Button className="w-full">View Cart</Button>
            </Link>
          </div>
        )}
      </div>
    </div>
  );
}
