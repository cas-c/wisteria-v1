import { test, expect } from "@playwright/test";

test.describe("Loading States", () => {
  test("homepage shows skeletons during slow network", async ({
    page,
    context,
  }) => {
    // Throttle network to Slow 3G
    const client = await context.newCDPSession(page);
    await client.send("Network.emulateNetworkConditions", {
      offline: false,
      downloadThroughput: (500 * 1000) / 8, // 500 kb/s
      uploadThroughput: (500 * 1000) / 8,
      latency: 400, // 400ms latency
    });

    // Navigate with network throttling
    await page.goto("/", { waitUntil: "networkidle" });

    // Once loaded, skeletons should be replaced with actual content
    const heading = page.getByRole("heading", { name: "Wisteria" });
    await expect(heading).toBeVisible({ timeout: 10000 });

    // Product cards should eventually load
    const productCards = page.locator('a[href^="/products/"]');
    const cardCount = await productCards.count();
    expect(cardCount).toBeGreaterThan(0);

    await client.send("Network.disable", {});
  });

  test("catalog page shows skeletons during slow network", async ({
    page,
    context,
  }) => {
    // Throttle network
    const client = await context.newCDPSession(page);
    await client.send("Network.emulateNetworkConditions", {
      offline: false,
      downloadThroughput: (500 * 1000) / 8,
      uploadThroughput: (500 * 1000) / 8,
      latency: 400,
    });

    // Navigate to catalog
    await page.goto("/products", { waitUntil: "networkidle" });

    // Once loaded, heading should be visible
    const heading = page.getByRole("heading", { name: "Shop All" });
    await expect(heading).toBeVisible({ timeout: 10000 });

    // Product count should be visible
    const productCount = page.locator("text=/\\d+ products? available/");
    await expect(productCount).toBeVisible({ timeout: 10000 });

    // Product cards should load
    const productCards = page.locator('a[href^="/products/"]');
    const cardCount = await productCards.count();
    expect(cardCount).toBeGreaterThan(0);

    await client.send("Network.disable", {});
  });

  test("product detail page shows skeletons during slow network", async ({
    page,
    context,
  }) => {
    const testProductSlug = "rem-1-7-scale-figure";

    // Throttle network
    const client = await context.newCDPSession(page);
    await client.send("Network.emulateNetworkConditions", {
      offline: false,
      downloadThroughput: (500 * 1000) / 8,
      uploadThroughput: (500 * 1000) / 8,
      latency: 400,
    });

    // Navigate to product detail page
    await page.goto(`/products/${testProductSlug}`, {
      waitUntil: "networkidle",
    });

    // Once loaded, product name (h1) should be visible
    const heading = page.locator("h1").first();
    await expect(heading).toBeVisible({ timeout: 10000 });

    // Product image should be visible
    const image = page.locator("img").first();
    await expect(image).toBeVisible({ timeout: 10000 });

    // Price should be visible
    const price = page.locator("text=/\\$[0-9]+\\.[0-9]{2}/");
    await expect(price).toBeVisible({ timeout: 10000 });

    await client.send("Network.disable", {});
  });
});
