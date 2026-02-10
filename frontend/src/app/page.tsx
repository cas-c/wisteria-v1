import { api } from "@/lib/api";
import { type PaginatedResponse, type Product } from "@/types";
import { ProductGrid } from "@/components/product/ProductGrid";
import { Button } from "@/components/ui/Button";

/**
 * Homepage with hero section and latest arrivals.
 * Server Component — fetches data at build/request time with ISR.
 */
async function HomePage() {
  // Fetch first 8 products with ISR revalidation
  const data = await api<PaginatedResponse<Product>>("/products?per_page=8", {
    next: { revalidate: 60 },
  });

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="border-b border-border bg-gradient-to-b from-muted/50 to-background">
        <div className="mx-auto max-w-7xl px-4 py-16 sm:px-6 lg:px-8 lg:py-24">
          <div className="text-center">
            <h1 className="font-serif text-4xl font-bold tracking-tight text-foreground sm:text-5xl lg:text-6xl">
              Wisteria
            </h1>
            <p className="mt-4 text-lg text-muted-foreground sm:text-xl">
              Curated Japanese figurines & collectibles
            </p>
            <div className="mt-8">
              <Button href="/products" variant="primary" size="lg">
                Browse Collection
              </Button>
            </div>
          </div>
        </div>
      </section>

      {/* Latest Arrivals */}
      <section className="mx-auto max-w-7xl px-4 py-16 sm:px-6 lg:px-8">
        <h2 className="text-2xl font-bold text-foreground sm:text-3xl">
          Latest Arrivals
        </h2>
        <div className="mt-8">
          <ProductGrid products={data.items} />
        </div>
      </section>
    </div>
  );
}

export { HomePage as default };
