import { API_BASE_URL } from "./constants";

/**
 * Thin fetch wrapper for calling the FastAPI backend.
 *
 * - Automatically prepends the API base URL
 * - Sets JSON content type for request bodies
 * - Throws on non-2xx responses with the error detail from FastAPI
 * - Supports Next.js fetch extensions (cache, revalidate) for ISR
 *
 * Usage:
 *   const products = await api<PaginatedResponse<Product>>("/products");
 *   const product = await api<Product>("/products/my-slug", {
 *     next: { revalidate: 60 }
 *   });
 */
export async function api<T>(
  path: string,
  options: RequestInit & { next?: { revalidate?: number } } = {},
): Promise<T> {
  const url = `${API_BASE_URL}${path}`;

  const headers: Record<string, string> = {
    ...(options.headers as Record<string, string>),
  };

  // Auto-set Content-Type for JSON bodies
  if (options.body && typeof options.body === "string") {
    headers["Content-Type"] = "application/json";
  }

  const response = await fetch(url, {
    ...options,
    headers,
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: "Request failed" }));
    throw new Error(error.detail ?? `API error: ${response.status}`);
  }

  return response.json() as Promise<T>;
}
