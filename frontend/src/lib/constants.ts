export const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000/api/v1";

export const SITE_NAME = "Wisteria";
export const SITE_DESCRIPTION = "Curated Japanese figurines & collectibles";

export const CONDITION_LABELS: Record<string, string> = {
  new: "New",
  like_new: "Like New",
  used: "Used",
};

export const CATEGORY_LABELS: Record<string, string> = {
  nendoroid: "Nendoroid",
  scale_figure: "Scale Figure",
  plush: "Plush",
  goods: "Goods",
};
