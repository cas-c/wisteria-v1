import { cn } from "@/lib/utils";
import { type ComponentPropsWithoutRef } from "react";

interface BadgeProps extends ComponentPropsWithoutRef<"span"> {
  variant?: "default" | "accent" | "muted";
  children: React.ReactNode;
}

/**
 * Badge component for labels and tags.
 */
export function Badge({
  variant = "default",
  className,
  children,
  ...props
}: BadgeProps) {
  const variantClasses = {
    default: "bg-card text-card-foreground border border-border",
    accent: "bg-accent text-accent-foreground",
    muted: "bg-muted text-muted-foreground",
  };

  return (
    <span
      className={cn(
        "inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-semibold",
        variantClasses[variant],
        className,
      )}
      {...props}
    >
      {children}
    </span>
  );
}
