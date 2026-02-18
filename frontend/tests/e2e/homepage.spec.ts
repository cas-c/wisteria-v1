import { test, expect } from "@playwright/test";

test.describe("Homepage", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto("/");
  });

  test("displays hero section with Wisteria heading and tagline", async ({
    page,
  }) => {
    await expect(page.getByRole("heading", { name: "Wisteria" })).toBeVisible();
    await expect(
      page.getByText("Curated Japanese figurines & collectibles"),
    ).toBeVisible();
  });

  test("Browse Collection button links to /products", async ({ page }) => {
    const browseButton = page.getByRole("button", {
      name: "Browse Collection",
    });
    await expect(browseButton).toBeVisible();
    await browseButton.click();
    await expect(page).toHaveURL("/products");
  });

  test("displays Latest Arrivals section", async ({ page }) => {
    await expect(
      page.getByRole("heading", { name: "Latest Arrivals" }),
    ).toBeVisible();
  });

  test("shows 8 product cards in Latest Arrivals", async ({ page }) => {
    // Product cards are links to /products/{slug} containing price
    const productCards = page.locator('a[href^="/products/"]');
    await expect(productCards).toHaveCount(8);
  });

  test("product cards display image, name, price, and condition badge", async ({
    page,
  }) => {
    // Get the first product card
    const firstCard = page.locator('a[href^="/products/"]').first();

    // Check for image (within the card)
    const image = firstCard.locator("img");
    await expect(image).toBeVisible();

    // Check for product name (h3 inside card)
    const productName = firstCard.locator("h3");
    await expect(productName).toBeVisible();

    // Check for price (contains $ symbol)
    const price = firstCard.locator("text=/\\$/");
    await expect(price).toBeVisible();

    // Check for condition badge (New/Like New/Used)
    const badge = firstCard.locator("span").filter({
      has: page.locator("text=/New|Like New|Used/"),
    });
    await expect(badge).toBeVisible();
  });

  test("clicking a product card navigates to product detail page", async ({
    page,
  }) => {
    const firstCard = page.locator('a[href^="/products/"]').first();
    const href = await firstCard.getAttribute("href");

    await firstCard.click();
    await expect(page).toHaveURL(href!);
  });

  test("header renders with logo and navigation", async ({ page }) => {
    const header = page.locator("header");
    await expect(header).toBeVisible();

    // Check for Wisteria logo
    const logo = page.getByRole("link", { name: "Wisteria" }).first();
    await expect(logo).toBeVisible();

    // Check for desktop navigation links
    const homeLink = page.getByRole("link", { name: "Home" });
    const shopLink = page.getByRole("link", { name: "Shop" });

    expect(page.viewportSize()).not.toBeNull();

    // These should be visible on desktop (hidden on mobile)
    if (page.viewportSize()!.width! >= 768) {
      await expect(homeLink).toBeVisible();
      await expect(shopLink).toBeVisible();
    }
  });

  test("footer renders on page", async ({ page }) => {
    const footer = page.locator("footer");
    await expect(footer).toBeVisible();
  });

  test("logo links back to homepage", async ({ page }) => {
    // Navigate to products
    await page.goto("/products");

    // Click logo
    const logo = page.getByRole("link", { name: "Wisteria" }).first();
    await logo.click();

    // Should return to homepage
    await expect(page).toHaveURL("/");
  });
});
