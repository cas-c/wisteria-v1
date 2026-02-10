"use client";

import { Button } from "@/components/ui/Button";
import { type Product } from "@/types";

interface AddToCartButtonProps {
  product: Product;
}

/**
 * Add to cart button placeholder for Phase 4.
 * Currently logs to console; will integrate with cart store later.
 */
export function AddToCartButton({ product }: AddToCartButtonProps) {
  const handleClick = () => {
    console.log("Add to cart:", product.name);
    // TODO: Phase 4 — integrate with Zustand cart store
  };

  return (
    <Button variant="primary" size="lg" onClick={handleClick}>
      Add to Cart
    </Button>
  );
}
