"use client";

import { Button } from "@/components/ui/Button";
import { useCartStore } from "@/stores/cart";
import { type Product } from "@/types";

interface AddToCartButtonProps {
  product: Product;
}

export function AddToCartButton({ product }: AddToCartButtonProps) {
  const addItem = useCartStore((state) => state.addItem);

  return (
    <Button variant="primary" size="lg" onClick={() => addItem(product)}>
      Add to Cart
    </Button>
  );
}
