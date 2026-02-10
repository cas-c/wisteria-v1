/**
 * Badge displaying product condition with color coding.
 * Maps to theme CSS variables for consistent styling.
 */
interface ConditionBadgeProps {
  condition: "new" | "like_new" | "used";
}

const conditionLabels: Record<string, string> = {
  new: "New",
  like_new: "Like New",
  used: "Used",
};

const conditionStyles: Record<string, string> = {
  new: "bg-badge-new text-badge-new-foreground",
  like_new: "bg-badge-like-new text-badge-like-new-foreground",
  used: "bg-badge-used text-badge-used-foreground",
};

export function ConditionBadge({ condition }: ConditionBadgeProps) {
  return (
    <span
      className={`inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-semibold ${conditionStyles[condition]}`}
    >
      {conditionLabels[condition]}
    </span>
  );
}
