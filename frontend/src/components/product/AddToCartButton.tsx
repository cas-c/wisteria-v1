"use client";

import { Button } from "@/components/ui/Button";
import { useCartStore } from "@/stores/cart";
import { type Product } from "@/types";

interface AddToCartButtonProps {
  product: Product;
}

export function AddToCartButton({ product }: AddToCartButtonProps) {
  const addItem = useCartStore((state) => state.addItem);
  const openDrawer = useCartStore((state) => state.openDrawer);
  const alreadyInCart = useCartStore(
    (state) => !!state.items.find((p) => p.id === product.id),
  );

  return (
    <Button
      variant="primary"
      size="lg"
      onClick={() => {
        if (alreadyInCart) {
          return;
        }
        addItem(product);
        openDrawer();
      }}
      disabled={alreadyInCart}
    >
      {alreadyInCart ? "In" : "Add to"} Cart
    </Button>
  );
}
