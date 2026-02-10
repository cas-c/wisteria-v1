import { Skeleton } from "@/components/ui/Skeleton";

/**
 * Loading skeleton for product detail page.
 * Matches the 2-column layout of the detail page.
 */
function ProductDetailLoading() {
  return (
    <div className="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8">
      <div className="grid grid-cols-1 gap-8 md:grid-cols-2 lg:gap-12">
        {/* Left: Image Skeleton */}
        <Skeleton className="h-96 w-full rounded-lg" />

        {/* Right: Info Skeleton */}
        <div className="space-y-6">
          <div>
            <Skeleton className="h-10 w-3/4" />
            <Skeleton className="mt-2 h-5 w-32" />
          </div>

          <div className="flex items-center gap-3">
            <Skeleton className="h-9 w-24" />
            <Skeleton className="h-6 w-20 rounded-full" />
          </div>

          <Skeleton className="h-20 w-full" />

          <Skeleton className="h-12 w-40 rounded-lg" />
        </div>
      </div>
    </div>
  );
}

export { ProductDetailLoading as default };
