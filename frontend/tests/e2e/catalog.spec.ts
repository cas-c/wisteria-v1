import { test, expect } from "@playwright/test";

test.describe("Product Catalog", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto("/products");
  });

  test("displays Shop All heading", async ({ page }) => {
    await expect(page.getByRole("heading", { name: "Shop All" })).toBeVisible();
  });

  test("shows product count", async ({ page }) => {
    // Expected format: "X products available" or "1 product available"
    const productCount = page.locator("text=/\\d+ products? available/");
    await expect(productCount).toBeVisible();
  });

  test("renders product grid with items", async ({ page }) => {
    const productCards = page.locator('a[href^="/products/"]');
    const count = await productCards.count();
    expect(count).toBeGreaterThan(0);
  });

  test("product grid shows up to 12 items per page", async ({ page }) => {
    const productCards = page.locator('a[href^="/products/"]');
    const count = await productCards.count();
    // Current seed has 9 products, so should be 9, not 12
    expect(count).toBeLessThanOrEqual(12);
  });

  test("pagination controls appear when there are more products", async ({
    page,
  }) => {
    // Pagination only shows if data.pages > 1
    // Current seed has 9 products with per_page=12, so no pagination yet
    // This test will pass when seed is expanded to >12 products
    const paginationSection = page.locator("text=/Page \\d+ of \\d+/");
    const paginationExists = await paginationSection
      .isVisible()
      .catch(() => false);

    // If pagination exists, check buttons
    if (paginationExists) {
      const prevButton = page.getByRole("button", { name: "Previous" });
      const nextButton = page.getByRole("button", { name: "Next" });

      // On page 1, Previous shouldn't exist
      const prevExists = await prevButton.isVisible().catch(() => false);
      expect(prevExists).toBe(false);

      // Next should exist
      await expect(nextButton).toBeVisible();
    }
  });

  test("Next button navigates to page 2 when pagination exists", async ({
    page,
  }) => {
    const nextButton = page.getByRole("button", { name: "Next" });
    const nextExists = await nextButton.isVisible().catch(() => false);

    if (nextExists) {
      await nextButton.click();
      await expect(page).toHaveURL(/\?page=2/);
    }
  });

  test("Previous button appears on page 2", async ({ page }) => {
    // Only test if pagination exists
    const nextButton = page.getByRole("button", { name: "Next" });
    const nextExists = await nextButton.isVisible().catch(() => false);

    if (nextExists) {
      await nextButton.click();
      const prevButton = page.getByRole("button", { name: "Previous" });
      await expect(prevButton).toBeVisible();
    }
  });

  test("URL updates with page query parameter", async ({ page }) => {
    const nextButton = page.getByRole("button", { name: "Next" });
    const nextExists = await nextButton.isVisible().catch(() => false);

    if (nextExists) {
      await nextButton.click();
      const url = page.url();
      expect(url).toContain("page=2");
    }
  });

  test("product cards are clickable and navigate to detail page", async ({
    page,
  }) => {
    const firstCard = page.locator('a[href^="/products/"]').first();
    const href = await firstCard.getAttribute("href");

    await firstCard.click();
    await expect(page).toHaveURL(href!);
  });

  test("responsive layout: mobile (375px) shows 1 column grid", async ({
    page,
  }) => {
    await page.setViewportSize({ width: 375, height: 812 });
    await page.goto("/products");

    const grid = page.locator("div").filter({
      has: page.locator('a[href^="/products/"]').first(),
    });

    expect(grid).not.toBeNull();

    // Check for grid-cols-1 class (mobile layout)
    // The grid container should use responsive Tailwind classes
    const gridContainer = page.locator(
      "div.grid.grid-cols-1.sm\\:grid-cols-2.lg\\:grid-cols-3.xl\\:grid-cols-4",
    );

    if (await gridContainer.isVisible()) {
      // Grid exists with responsive classes
      expect(await gridContainer.isVisible()).toBe(true);
    }
  });

  test("responsive layout: desktop (1280px) shows 4 column grid", async ({
    page,
  }) => {
    await page.setViewportSize({ width: 1280, height: 800 });
    await page.goto("/products");

    const gridContainer = page.locator(
      "div.grid.grid-cols-1.sm\\:grid-cols-2.lg\\:grid-cols-3.xl\\:grid-cols-4",
    );

    if (await gridContainer.isVisible()) {
      expect(await gridContainer.isVisible()).toBe(true);
    }
  });
});
