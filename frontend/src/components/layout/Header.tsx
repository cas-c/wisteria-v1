"use client";

import { useState } from "react";
import { MobileNav } from "./MobileNav";
import { CartDrawer } from "@/components/cart/CartDrawer";
import { useCartStore, selectCartItemCount } from "@/stores/cart";
import Link from "next/link";

/**
 * Site header with logo, navigation, and cart icon.
 * Sticky with backdrop blur for a modern glass effect.
 */
export function Header() {
  const [mobileNavOpen, setMobileNavOpen] = useState(false);
  const itemCount = useCartStore(selectCartItemCount);
  const openDrawer = useCartStore((state) => state.openDrawer);

  return (
    <>
      <header className="sticky top-0 z-40 border-b border-border bg-background/80 backdrop-blur-sm">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="flex h-16 items-center justify-between">
            {/* Logo */}
            <Link
              href="/"
              className="font-serif text-2xl font-bold text-foreground"
            >
              Wisteria
            </Link>

            {/* Desktop Navigation */}
            <nav className="hidden md:flex items-center gap-6">
              <Link
                href="/"
                className="text-sm font-medium text-foreground hover:text-accent transition-colors"
              >
                Home
              </Link>
              <Link
                href="/products"
                className="text-sm font-medium text-foreground hover:text-accent transition-colors"
              >
                Shop
              </Link>
            </nav>

            {/* Right side: Cart + Mobile Menu */}
            <div className="flex items-center gap-4">
              {/* Cart Icon with Badge */}
              <button
                onClick={openDrawer}
                className="relative p-2 text-foreground hover:text-accent transition-colors"
                aria-label={`Shopping cart (${itemCount} items)`}
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                  strokeWidth={1.5}
                  stroke="currentColor"
                  className="h-6 w-6"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    d="M15.75 10.5V6a3.75 3.75 0 1 0-7.5 0v4.5m11.356-1.993 1.263 12c.07.665-.45 1.243-1.119 1.243H4.25a1.125 1.125 0 0 1-1.12-1.243l1.264-12A1.125 1.125 0 0 1 5.513 7.5h12.974c.576 0 1.059.435 1.119 1.007ZM8.625 10.5a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Zm7.5 0a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Z"
                  />
                </svg>
                {itemCount > 0 && (
                  <span className="absolute -top-1 -right-1 flex h-5 w-5 items-center justify-center rounded-full bg-accent text-xs font-semibold text-white">
                    {itemCount}
                  </span>
                )}
              </button>

              {/* Mobile Menu Toggle */}
              <button
                className="md:hidden p-2 text-foreground hover:text-accent transition-colors"
                onClick={() => setMobileNavOpen(true)}
                aria-label="Open menu"
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                  strokeWidth={1.5}
                  stroke="currentColor"
                  className="h-6 w-6"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5"
                  />
                </svg>
              </button>
            </div>
          </div>
        </div>
      </header>

      <MobileNav
        isOpen={mobileNavOpen}
        onClose={() => setMobileNavOpen(false)}
      />
      <CartDrawer />
    </>
  );
}
