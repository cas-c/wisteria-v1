import { cn } from "@/lib/utils";
import { type ComponentPropsWithoutRef } from "react";

interface CardProps extends ComponentPropsWithoutRef<"div"> {
  children: React.ReactNode;
}

/**
 * Card container with rounded corners and subtle shadow.
 */
export function Card({ className, children, ...props }: CardProps) {
  return (
    <div
      className={cn(
        "rounded-xl border border-border bg-card text-card-foreground shadow-sm",
        className,
      )}
      {...props}
    >
      {children}
    </div>
  );
}

interface CardContentProps extends ComponentPropsWithoutRef<"div"> {
  children: React.ReactNode;
}

/**
 * Card content area with standard padding.
 */
export function CardContent({ className, children, ...props }: CardContentProps) {
  return (
    <div className={cn("p-4", className)} {...props}>
      {children}
    </div>
  );
}
