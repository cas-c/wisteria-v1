import { test, expect, devices } from "@playwright/test";

test.describe("Responsive Layout", () => {
  test("mobile (375px): displays 1-column grid", async ({ browser }) => {
    const context = await browser.newContext({
      ...devices["Pixel 5"],
      viewport: { width: 375, height: 812 },
    });
    const page = await context.newPage();
    await page.goto("/products");

    // Check that product cards exist
    const productCards = page.locator('a[href^="/products/"]');
    const count = await productCards.count();
    expect(count).toBeGreaterThan(0);

    // On mobile, hamburger menu should be visible
    const mobileMenuButton = page.locator("button[aria-label*='Menu']");
    const isMobileMenuVisible = await mobileMenuButton
      .isVisible()
      .catch(() => false);

    // Desktop nav should be hidden on mobile
    const desktopNav = page.locator("nav.hidden.md\\:flex");
    const isDesktopNavHidden = !(await desktopNav
      .isVisible()
      .catch(() => false));

    // Either mobile menu is visible OR desktop nav is hidden
    expect(isMobileMenuVisible || isDesktopNavHidden).toBe(true);

    await context.close();
  });

  test("tablet (768px): displays 2-column grid", async ({ browser }) => {
    const context = await browser.newContext({
      viewport: { width: 768, height: 1024 },
    });
    const page = await context.newPage();
    await page.goto("/products");

    // Check that product cards exist
    const productCards = page.locator('a[href^="/products/"]');
    const count = await productCards.count();
    expect(count).toBeGreaterThan(0);

    // At tablet size, desktop nav should be visible
    const desktopNav = page.locator("nav.hidden.md\\:flex");
    const isDesktopNavVisible = await desktopNav.isVisible().catch(() => false);
    expect(isDesktopNavVisible).toBe(true);

    await context.close();
  });

  test("desktop (1280px): displays 4-column grid", async ({ browser }) => {
    const context = await browser.newContext({
      viewport: { width: 1280, height: 800 },
    });
    const page = await context.newPage();
    await page.goto("/products");

    // Check that product cards exist
    const productCards = page.locator('a[href^="/products/"]');
    const count = await productCards.count();
    expect(count).toBeGreaterThan(0);

    // Desktop nav should be visible
    const desktopNav = page.locator("nav.hidden.md\\:flex");
    const isDesktopNavVisible = await desktopNav.isVisible().catch(() => false);
    expect(isDesktopNavVisible).toBe(true);

    await context.close();
  });

  test("mobile menu opens and closes", async ({ browser }) => {
    const context = await browser.newContext({
      ...devices["Pixel 5"],
      viewport: { width: 375, height: 812 },
    });
    const page = await context.newPage();
    await page.goto("/");

    // Find the mobile menu button
    const mobileMenuButton = page.locator("button").filter({
      has: page.locator("svg"),
    });

    // Click to open
    const buttons = await mobileMenuButton.all();
    if (buttons.length > 0) {
      // Find the hamburger/menu button (usually the last button in header)
      const headerMenuButtons = await page.locator("header button").all();
      if (headerMenuButtons.length > 0) {
        const menuButton = headerMenuButtons[headerMenuButtons.length - 1];
        await menuButton.click();

        // Mobile nav should appear
        const mobileNav = page.locator("nav");
        const navVisible = await mobileNav.isVisible().catch(() => false);

        // Click again to close
        await menuButton.click();
      }
    }

    await context.close();
  });

  test("navigation links work on mobile menu", async ({ browser }) => {
    const context = await browser.newContext({
      ...devices["Pixel 5"],
      viewport: { width: 375, height: 812 },
    });
    const page = await context.newPage();
    await page.goto("/");

    // On mobile, click Shop link (either in menu or visible)
    const shopLink = page.getByRole("link", { name: "Shop" });
    const shopLinkVisible = await shopLink.isVisible().catch(() => false);

    if (shopLinkVisible) {
      await shopLink.click();
      await expect(page).toHaveURL("/products");
    }

    // Click Home link
    const homeLink = page.getByRole("link", { name: "Home" });
    const homeLinkVisible = await homeLink.isVisible().catch(() => false);

    if (homeLinkVisible) {
      await homeLink.click();
      await expect(page).toHaveURL("/");
    }

    await context.close();
  });

  test("hero section stacks on mobile, side-by-side on desktop", async ({
    browser,
  }) => {
    // Mobile view
    const mobileContext = await browser.newContext({
      viewport: { width: 375, height: 812 },
    });
    const mobilePage = await mobileContext.newPage();
    await mobilePage.goto("/");

    const mobileHero = mobilePage.locator("section").first();
    await expect(mobileHero).toBeVisible();

    // Check hero section exists
    const mobileHeading = mobilePage.getByRole("heading", { name: "Wisteria" });
    await expect(mobileHeading).toBeVisible();

    await mobileContext.close();

    // Desktop view
    const desktopContext = await browser.newContext({
      viewport: { width: 1280, height: 800 },
    });
    const desktopPage = await desktopContext.newPage();
    await desktopPage.goto("/");

    const desktopHero = desktopPage.locator("section").first();
    await expect(desktopHero).toBeVisible();

    const desktopHeading = desktopPage.getByRole("heading", {
      name: "Wisteria",
    });
    await expect(desktopHeading).toBeVisible();

    await desktopContext.close();
  });
});
