"use client";

import { useEffect } from "react";

interface MobileNavProps {
  isOpen: boolean;
  onClose: () => void;
}

/**
 * Full-screen mobile navigation overlay.
 */
export function MobileNav({ isOpen, onClose }: MobileNavProps) {
  // Close on escape key
  useEffect(() => {
    if (!isOpen) return;

    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === "Escape") onClose();
    };

    document.addEventListener("keydown", handleEscape);
    return () => document.removeEventListener("keydown", handleEscape);
  }, [isOpen, onClose]);

  // Prevent body scroll when open
  useEffect(() => {
    if (isOpen) {
      document.body.style.overflow = "hidden";
    } else {
      document.body.style.overflow = "";
    }
    return () => {
      document.body.style.overflow = "";
    };
  }, [isOpen]);

  if (!isOpen) return null;

  return (
    <div
      className="fixed inset-0 z-40 bg-background/95 backdrop-blur-sm md:hidden"
      onClick={onClose}
    >
      <div className="flex min-h-screen flex-col p-6">
        {/* Close button */}
        <div className="flex justify-end">
          <button
            onClick={onClose}
            className="p-2 text-foreground hover:text-accent transition-colors"
            aria-label="Close menu"
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
                d="M6 18 18 6M6 6l12 12"
              />
            </svg>
          </button>
        </div>

        {/* Navigation links */}
        <nav className="flex flex-col items-center justify-center flex-1 gap-8">
          <a
            href="/"
            className="text-2xl font-medium text-foreground hover:text-accent transition-colors"
            onClick={onClose}
          >
            Home
          </a>
          <a
            href="/products"
            className="text-2xl font-medium text-foreground hover:text-accent transition-colors"
            onClick={onClose}
          >
            Shop
          </a>
        </nav>
      </div>
    </div>
  );
}
