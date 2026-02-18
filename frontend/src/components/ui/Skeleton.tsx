import { cn } from "@/lib/utils";
import { type ComponentPropsWithoutRef } from "react";

// interface SkeletonProps extends ComponentPropsWithoutRef<"div"> {}
type SkeletonProps = ComponentPropsWithoutRef<"div">;

/**
 * Skeleton loading placeholder with pulse animation.
 * Consumer sets dimensions via className.
 */
export function Skeleton({ className, ...props }: SkeletonProps) {
  return (
    <div
      className={cn("animate-pulse rounded-md bg-muted", className)}
      {...props}
    />
  );
}
