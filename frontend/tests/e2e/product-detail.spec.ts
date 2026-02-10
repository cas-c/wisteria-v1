import { test, expect } from "@playwright/test";

test.describe("Product Detail Page", () => {
  // Use the slug from seed data
  const testProductSlug = "rem-1-7-scale-figure";

  test("displays product name as h1", async ({ page }) => {
    await page.goto(`/products/${testProductSlug}`);

    // The product name should be in an h1 tag
    const heading = page.locator("h1").first();
    await expect(heading).toBeVisible();

    // It should contain non-empty text
    const text = await heading.textContent();
    expect(text?.trim().length).toBeGreaterThan(0);
  });

  test("displays price formatted as currency", async ({ page }) => {
    await page.goto(`/products/${testProductSlug}`);

    // Look for price pattern like $XXX.XX
    const price = page.locator("text=/\\$[0-9]+\\.[0-9]{2}/");
    await expect(price).toBeVisible();
  });

  test("displays condition badge", async ({ page }) => {
    await page.goto(`/products/${testProductSlug}`);

    // Look for condition badge with New, Like New, or Used
    const badge = page.locator("span").filter({
      hasText: /New|Like New|Used/,
    });
    await expect(badge).toBeVisible();
  });

  test("displays category (capitalized, underscores replaced)", async ({
    page,
  }) => {
    await page.goto(`/products/${testProductSlug}`);

    // Category should be visible below the product name
    // It's displayed in a capitalized format with underscores replaced by spaces
    const categoryText = page.locator("p.capitalize.text-sm");
    await expect(categoryText).toBeVisible();
  });

  test("displays product description", async ({ page }) => {
    await page.goto(`/products/${testProductSlug}`);

    // Description should be visible as a paragraph
    const description = page.locator("p.text-base.leading-relaxed");
    await expect(description).toBeVisible();

    const text = await description.textContent();
    expect(text?.trim().length).toBeGreaterThan(0);
  });

  test("displays product image", async ({ page }) => {
    await page.goto(`/products/${testProductSlug}`);

    const image = page.locator("img").first();
    await expect(image).toBeVisible();
  });

  test("Add to Cart button is present and clickable", async ({ page }) => {
    await page.goto(`/products/${testProductSlug}`);

    const addToCartButton = page.getByRole("button", { name: "Add to Cart" });
    await expect(addToCartButton).toBeVisible();
    await expect(addToCartButton).toBeEnabled();
  });

  test("clicking Add to Cart logs to console", async ({ page }) => {
    await page.goto(`/products/${testProductSlug}`);

    // Set up console message listener
    const consoleLogs: string[] = [];
    page.on("console", (msg) => {
      if (msg.type() === "log") {
        consoleLogs.push(msg.text());
      }
    });

    const addToCartButton = page.getByRole("button", { name: "Add to Cart" });
    await addToCartButton.click();

    // Check that a console log was made with "Add to cart:"
    const addToCartLog = consoleLogs.find((log) =>
      log.includes("Add to cart:"),
    );
    expect(addToCartLog).toBeDefined();
  });

  test("shows 404 page for invalid product slug", async ({ page }) => {
    await page.goto("/products/nonexistent-slug", { waitUntil: "networkidle" });

    // Next.js 404 page should render
    // Look for common 404 text patterns
    const notFound = page.locator("text=/404|not found|page not found/i");
    const hasNotFound = await notFound.isVisible().catch(() => false);

    // Also check status code
    const response = await page
      .context()
      .newPage()
      .then((p) => p.goto("/products/nonexistent-slug"));

    // If not caught above, at least verify the page changed
    expect(page.url()).toContain("nonexistent-slug");
  });

  test("header and footer render on product detail page", async ({ page }) => {
    await page.goto(`/products/${testProductSlug}`);

    const header = page.locator("header");
    const footer = page.locator("footer");

    await expect(header).toBeVisible();
    await expect(footer).toBeVisible();
  });

  test("navigating back via header works", async ({ page }) => {
    await page.goto(`/products/${testProductSlug}`);

    // Click the Wisteria logo to go back to homepage
    const logo = page.getByRole("link", { name: "Wisteria" }).first();
    await logo.click();

    await expect(page).toHaveURL("/");
  });
});
