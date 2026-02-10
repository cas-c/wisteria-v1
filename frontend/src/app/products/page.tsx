import { api } from "@/lib/api";
import { type PaginatedResponse, type Product } from "@/types";
import { ProductGrid } from "@/components/product/ProductGrid";
import { Button } from "@/components/ui/Button";

interface ProductsPageProps {
  searchParams: Promise<{
    page?: string;
    category?: string;
    condition?: string;
    search?: string;
  }>;
}

/**
 * Product catalog page with pagination and filtering.
 * Server Component — reads searchParams and fetches products from API.
 */
async function ProductsPage({ searchParams }: ProductsPageProps) {
  // Next.js 15+: searchParams is a Promise
  const params = await searchParams;
  const page = parseInt(params.page ?? "1", 10);
  const category = params.category;
  const condition = params.condition;
  const search = params.search;

  // Build query string
  const queryParams = new URLSearchParams({
    page: page.toString(),
    per_page: "12",
  });
  if (category) queryParams.set("category", category);
  if (condition) queryParams.set("condition", condition);
  if (search) queryParams.set("search", search);

  const data = await api<PaginatedResponse<Product>>(
    `/products?${queryParams.toString()}`,
    { next: { revalidate: 60 } },
  );

  const hasPrev = page > 1;
  const hasNext = page < data.pages;

  return (
    <div className="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-foreground">Shop All</h1>
        <p className="mt-2 text-muted-foreground">
          {data.total} {data.total === 1 ? "product" : "products"} available
        </p>
      </div>

      {/* Product Grid */}
      <ProductGrid
        products={data.items}
        emptyMessage="No products match your filters."
      />

      {/* Pagination */}
      {data.pages > 1 && (
        <div className="mt-12 flex items-center justify-center gap-4">
          {hasPrev && (
            <Button
              href={`/products?page=${page - 1}`}
              variant="secondary"
              size="md"
            >
              Previous
            </Button>
          )}
          <span className="text-sm text-muted-foreground">
            Page {page} of {data.pages}
          </span>
          {hasNext && (
            <Button
              href={`/products?page=${page + 1}`}
              variant="secondary"
              size="md"
            >
              Next
            </Button>
          )}
        </div>
      )}
    </div>
  );
}

export { ProductsPage as default };
