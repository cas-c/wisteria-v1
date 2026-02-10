import { Card, CardContent } from "@/components/ui/Card";
import { Skeleton } from "@/components/ui/Skeleton";

/**
 * Loading skeleton for ProductCard.
 * Matches the structure and dimensions of the real card.
 */
export function ProductCardSkeleton() {
  return (
    <Card className="h-full">
      <Skeleton className="h-48 w-full rounded-t-xl rounded-b-none" />
      <CardContent className="space-y-2">
        <Skeleton className="h-5 w-3/4" />
        <div className="flex items-center justify-between">
          <Skeleton className="h-6 w-20" />
          <Skeleton className="h-5 w-16 rounded-full" />
        </div>
      </CardContent>
    </Card>
  );
}
