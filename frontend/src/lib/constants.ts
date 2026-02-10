/**
 * API base URL for server-side requests (SSR/ISR).
 * Uses internal Docker network URL when available, falls back to localhost.
 */
export const API_BASE_URL =
  process.env.API_URL_INTERNAL ??
  process.env.NEXT_PUBLIC_API_URL ??
  "http://localhost:8000/api/v1";

/**
 * API base URL for client-side requests (browser).
 * Always uses localhost since the browser is outside the Docker network.
 */
export const API_BASE_URL_CLIENT =
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
