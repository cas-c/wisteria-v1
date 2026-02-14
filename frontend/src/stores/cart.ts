import { create } from "zustand";
import { persist } from "zustand/middleware";
import toast from "react-hot-toast";
import type { Product } from "@/types";

interface CartStore {
  items: Product[];
  isDrawerOpen: boolean;
  addItem: (product: Product) => void;
  removeItem: (productId: string) => void;
  clearCart: () => void;
  openDrawer: () => void;
  closeDrawer: () => void;
}

/**
 * Cart store using Zustand with localStorage persistence.
 *
 * Key behaviors:
 * - Resale items are unique, so adding a duplicate shows a toast instead of incrementing quantity
 * - Cart persists to localStorage under the key "wisteria-cart"
 * - Total is computed from items in components/selectors
 */
export const useCartStore = create<CartStore>()(
  persist(
    (set, get) => ({
      items: [],
      isDrawerOpen: false,

      addItem: (product) => {
        const exists = get().items.find((item) => item.id === product.id);

        if (exists) {
          toast.error("This item is already in your cart");
          return;
        }

        set((state) => ({ items: [...state.items, product] }));
        toast.success("Added to cart");
      },

      removeItem: (productId) => {
        set((state) => ({
          items: state.items.filter((item) => item.id !== productId),
        }));
      },

      clearCart: () => {
        set({ items: [] });
      },

      openDrawer: () => {
        set({ isDrawerOpen: true });
      },

      closeDrawer: () => {
        set({ isDrawerOpen: false });
      },
    }),
    {
      name: "wisteria-cart",
    }
  )
);

/**
 * Selector to compute cart total in cents.
 * Usage: const total = useCartStore(selectCartTotal);
 */
export const selectCartTotal = (state: CartStore): number =>
  state.items.reduce((sum, item) => sum + item.price_cents, 0);

/**
 * Selector to get cart item count.
 * Usage: const count = useCartStore(selectCartItemCount);
 */
export const selectCartItemCount = (state: CartStore): number =>
  state.items.length;
