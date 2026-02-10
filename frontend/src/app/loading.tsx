import { ProductCardSkeleton } from "@/components/product/ProductCardSkeleton";
import { Skeleton } from "@/components/ui/Skeleton";

/**
 * Loading skeleton for homepage.
 * Matches the structure of the hero section + product grid.
 */
function HomeLoading() {
  return (
    <div className="min-h-screen">
      {/* Hero Skeleton */}
      <section className="border-b border-border bg-gradient-to-b from-muted/50 to-background">
        <div className="mx-auto max-w-7xl px-4 py-16 sm:px-6 lg:px-8 lg:py-24">
          <div className="flex flex-col items-center gap-4">
            <Skeleton className="h-14 w-64" />
            <Skeleton className="h-6 w-80" />
            <Skeleton className="h-12 w-48 rounded-lg" />
          </div>
        </div>
      </section>

      {/* Product Grid Skeleton */}
      <section className="mx-auto max-w-7xl px-4 py-16 sm:px-6 lg:px-8">
        <Skeleton className="h-8 w-48" />
        <div className="mt-8 grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
          {Array.from({ length: 8 }).map((_, i) => (
            <ProductCardSkeleton key={i} />
          ))}
        </div>
      </section>
    </div>
  );
}

export { HomeLoading as default };
