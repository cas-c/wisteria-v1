import { notFound } from "next/navigation";
import type { Metadata } from "next";
import { api } from "@/lib/api";
import { formatPrice } from "@/lib/utils";
import { type Product } from "@/types";
import { ProductImage } from "@/components/product/ProductImage";
import { ConditionBadge } from "@/components/product/ConditionBadge";
import { AddToCartButton } from "@/components/product/AddToCartButton";
import { Badge } from "@/components/ui/Badge";

interface ProductDetailPageProps {
  params: Promise<{ slug: string }>;
}

/**
 * Fetch product by slug from the API.
 * Returns null if not found (triggers notFound()).
 */
async function getProduct(slug: string): Promise<Product | null> {
  try {
    return await api<Product>(`/products/${slug}`, {
      next: { revalidate: 60 },
    });
  } catch (error) {
    return null;
  }
}

/**
 * Generate SEO metadata for the product detail page.
 */
export async function generateMetadata({
  params,
}: ProductDetailPageProps): Promise<Metadata> {
  const { slug } = await params;
  const product = await getProduct(slug);

  if (!product) {
    return {
      title: "Product Not Found",
    };
  }

  return {
    title: product.name,
    description: product.description,
  };
}

/**
 * Product detail page with large image, info, and add-to-cart.
 * Server Component — fetches product data at build/request time with ISR.
 */
async function ProductDetailPage({ params }: ProductDetailPageProps) {
  const { slug } = await params;
  const product = await getProduct(slug);

  if (!product) {
    notFound();
  }

  const categoryLabel = product.category.replace(/_/g, " ");

  return (
    <div className="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8">
      <div className="grid grid-cols-1 gap-8 md:grid-cols-2 lg:gap-12">
        {/* Left: Image */}
        <div>
          <ProductImage
            name={product.name}
            category={product.category}
            className="w-full h-96"
          />
        </div>

        {/* Right: Info */}
        <div className="space-y-6">
          <div>
            <h1 className="text-3xl font-bold text-foreground lg:text-4xl">
              {product.name}
            </h1>
            <p className="mt-2 text-sm text-muted-foreground capitalize">
              {categoryLabel}
            </p>
          </div>

          <div className="flex items-center gap-3">
            <p className="text-3xl font-bold text-foreground">
              {formatPrice(product.price_cents)}
            </p>
            <ConditionBadge condition={product.condition} />
          </div>

          {!product.is_available && (
            <Badge variant="muted">Sold Out</Badge>
          )}

          <p className="text-base text-foreground leading-relaxed">
            {product.description}
          </p>

          {product.is_available && <AddToCartButton product={product} />}
        </div>
      </div>
    </div>
  );
}

export { ProductDetailPage as default };
