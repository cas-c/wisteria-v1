/**
 * Product image placeholder.
 * Uses colored div based on category until real images are added.
 */
interface ProductImageProps {
  name: string;
  category: string;
  className?: string;
}

const categoryColors: Record<string, string> = {
  scale_figures: "bg-violet-400",
  nendoroids: "bg-rose-400",
  figmas: "bg-amber-400",
  prize_figures: "bg-sky-400",
};

export function ProductImage({ name, category, className = "" }: ProductImageProps) {
  const bgColor = categoryColors[category] ?? "bg-muted";

  return (
    <div
      className={`flex items-center justify-center rounded-lg ${bgColor} ${className}`}
      style={{ aspectRatio: "4/3" }}
    >
      <span className="text-center text-sm font-medium text-white px-4">
        {name}
      </span>
    </div>
  );
}
