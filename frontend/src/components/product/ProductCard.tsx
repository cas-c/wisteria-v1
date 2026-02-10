import { Card, CardContent } from "@/components/ui/Card";
import { formatPrice } from "@/lib/utils";
import { type Product } from "@/types";
import { ProductImage } from "./ProductImage";
import { ConditionBadge } from "./ConditionBadge";

interface ProductCardProps {
  product: Product;
}

/**
 * Compact product card for grid display.
 * Links to product detail page.
 */
export function ProductCard({ product }: ProductCardProps) {
  return (
    <a href={`/products/${product.slug}`} className="group block">
      <Card className="h-full transition-shadow hover:shadow-md">
        <ProductImage
          name={product.name}
          category={product.category}
          className="rounded-t-xl"
        />
        <CardContent className="space-y-2">
          <h3 className="font-medium text-foreground group-hover:text-accent transition-colors line-clamp-2">
            {product.name}
          </h3>
          <div className="flex items-center justify-between">
            <p className="text-lg font-bold text-foreground">
              {formatPrice(product.price_cents)}
            </p>
            <ConditionBadge condition={product.condition} />
          </div>
        </CardContent>
      </Card>
    </a>
  );
}
