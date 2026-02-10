import { ProductCardSkeleton } from "@/components/product/ProductCardSkeleton";
import { Skeleton } from "@/components/ui/Skeleton";

/**
 * Loading skeleton for product catalog page.
 * Matches the structure of the catalog header + product grid.
 */
function ProductsLoading() {
  return (
    <div className="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8">
      {/* Header Skeleton */}
      <div className="mb-8">
        <Skeleton className="h-9 w-40" />
        <Skeleton className="mt-2 h-5 w-48" />
      </div>

      {/* Product Grid Skeleton */}
      <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
        {Array.from({ length: 12 }).map((_, i) => (
          <ProductCardSkeleton key={i} />
        ))}
      </div>
    </div>
  );
}

export { ProductsLoading as default };
