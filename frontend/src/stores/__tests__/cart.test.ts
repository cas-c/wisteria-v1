import { renderHook, act } from "@testing-library/react";
import toast from "react-hot-toast";
import {
  useCartStore,
  selectCartTotal,
  selectCartItemCount,
} from "../cart";
import type { Product } from "@/types";

// Mock react-hot-toast
jest.mock("react-hot-toast");

// Mock product fixtures
const mockProduct1: Product = {
  id: "1",
  name: "Nendoroid Hatsune Miku",
  slug: "nendoroid-hatsune-miku",
  description: "Cute Miku figure",
  price_cents: 4500,
  condition: "new",
  category: "nendoroid",
  image_url: "https://example.com/miku.jpg",
  is_available: true,
  quantity: 1,
  created_at: "2024-01-01T00:00:00Z",
  updated_at: "2024-01-01T00:00:00Z",
};

const mockProduct2: Product = {
  id: "2",
  name: "Scale Figure Rem",
  slug: "scale-figure-rem",
  description: "Beautiful Rem figure",
  price_cents: 12000,
  condition: "like_new",
  category: "scale_figure",
  image_url: "https://example.com/rem.jpg",
  is_available: true,
  quantity: 1,
  created_at: "2024-01-01T00:00:00Z",
  updated_at: "2024-01-01T00:00:00Z",
};

describe("useCartStore", () => {
  beforeEach(() => {
    // Clear the store before each test
    const { result } = renderHook(() => useCartStore());
    act(() => {
      result.current.clearCart();
    });
    // Clear mock calls
    jest.clearAllMocks();
  });

  afterEach(() => {
    // Clear localStorage after each test
    localStorage.clear();
  });

  describe("addItem", () => {
    it("should add a product to the cart", () => {
      const { result } = renderHook(() => useCartStore());

      act(() => {
        result.current.addItem(mockProduct1);
      });

      expect(result.current.items).toHaveLength(1);
      expect(result.current.items[0]).toEqual(mockProduct1);
      expect(toast.success).toHaveBeenCalledWith("Added to cart");
    });

    it("should add multiple different products to the cart", () => {
      const { result } = renderHook(() => useCartStore());

      act(() => {
        result.current.addItem(mockProduct1);
        result.current.addItem(mockProduct2);
      });

      expect(result.current.items).toHaveLength(2);
      expect(result.current.items[0]).toEqual(mockProduct1);
      expect(result.current.items[1]).toEqual(mockProduct2);
    });

    it("should not add duplicate products and show error toast", () => {
      const { result } = renderHook(() => useCartStore());

      act(() => {
        result.current.addItem(mockProduct1);
      });

      expect(result.current.items).toHaveLength(1);

      act(() => {
        result.current.addItem(mockProduct1);
      });

      expect(result.current.items).toHaveLength(1);
      expect(toast.error).toHaveBeenCalledWith(
        "This item is already in your cart"
      );
    });
  });

  describe("removeItem", () => {
    it("should remove a product from the cart by id", () => {
      const { result } = renderHook(() => useCartStore());

      act(() => {
        result.current.addItem(mockProduct1);
        result.current.addItem(mockProduct2);
      });

      expect(result.current.items).toHaveLength(2);

      act(() => {
        result.current.removeItem(mockProduct1.id);
      });

      expect(result.current.items).toHaveLength(1);
      expect(result.current.items[0]).toEqual(mockProduct2);
    });

    it("should do nothing if product id does not exist", () => {
      const { result } = renderHook(() => useCartStore());

      act(() => {
        result.current.addItem(mockProduct1);
      });

      expect(result.current.items).toHaveLength(1);

      act(() => {
        result.current.removeItem("non-existent-id");
      });

      expect(result.current.items).toHaveLength(1);
    });
  });

  describe("clearCart", () => {
    it("should remove all items from the cart", () => {
      const { result } = renderHook(() => useCartStore());

      act(() => {
        result.current.addItem(mockProduct1);
        result.current.addItem(mockProduct2);
      });

      expect(result.current.items).toHaveLength(2);

      act(() => {
        result.current.clearCart();
      });

      expect(result.current.items).toHaveLength(0);
    });

    it("should work when cart is already empty", () => {
      const { result } = renderHook(() => useCartStore());

      expect(result.current.items).toHaveLength(0);

      act(() => {
        result.current.clearCart();
      });

      expect(result.current.items).toHaveLength(0);
    });
  });

  describe("selectCartTotal", () => {
    it("should return 0 for empty cart", () => {
      const { result } = renderHook(() => useCartStore());

      const total = selectCartTotal(result.current);
      expect(total).toBe(0);
    });

    it("should calculate total for single item", () => {
      const { result } = renderHook(() => useCartStore());

      act(() => {
        result.current.addItem(mockProduct1);
      });

      const total = selectCartTotal(result.current);
      expect(total).toBe(4500);
    });

    it("should calculate total for multiple items", () => {
      const { result } = renderHook(() => useCartStore());

      act(() => {
        result.current.addItem(mockProduct1);
        result.current.addItem(mockProduct2);
      });

      const total = selectCartTotal(result.current);
      expect(total).toBe(16500); // 4500 + 12000
    });
  });

  describe("selectCartItemCount", () => {
    it("should return 0 for empty cart", () => {
      const { result } = renderHook(() => useCartStore());

      const count = selectCartItemCount(result.current);
      expect(count).toBe(0);
    });

    it("should return correct count for multiple items", () => {
      const { result } = renderHook(() => useCartStore());

      act(() => {
        result.current.addItem(mockProduct1);
        result.current.addItem(mockProduct2);
      });

      const count = selectCartItemCount(result.current);
      expect(count).toBe(2);
    });
  });

  describe("persistence", () => {
    it("should persist cart to localStorage", () => {
      const { result } = renderHook(() => useCartStore());

      act(() => {
        result.current.addItem(mockProduct1);
      });

      // Check that localStorage was updated
      const stored = localStorage.getItem("wisteria-cart");
      expect(stored).toBeTruthy();

      const parsed = JSON.parse(stored!);
      expect(parsed.state.items).toHaveLength(1);
      expect(parsed.state.items[0].id).toBe(mockProduct1.id);
    });

    // Note: Testing restore from localStorage is tricky because the store is a singleton
    // and rehydration only happens on initial creation. The persist-to-localStorage test
    // above validates that the middleware is working correctly.
  });
});
