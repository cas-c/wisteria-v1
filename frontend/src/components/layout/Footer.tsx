/**
 * Site footer with logo, tagline, and links.
 */
export function Footer() {
  return (
    <footer className="border-t border-border bg-card">
      <div className="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 gap-8 md:grid-cols-3">
          {/* Logo & Tagline */}
          <div>
            <h3 className="font-serif text-xl font-bold text-foreground">
              Wisteria
            </h3>
            <p className="mt-2 text-sm text-muted-foreground">
              Curated Japanese figurines and collectibles.
            </p>
          </div>

          {/* Quick Links */}
          <div>
            <h4 className="text-sm font-semibold text-foreground">Shop</h4>
            <ul className="mt-4 space-y-2">
              <li>
                <a
                  href="/products"
                  className="text-sm text-muted-foreground hover:text-accent transition-colors"
                >
                  All Products
                </a>
              </li>
            </ul>
          </div>

          {/* Info */}
          <div>
            <h4 className="text-sm font-semibold text-foreground">Info</h4>
            <ul className="mt-4 space-y-2">
              <li>
                <a
                  href="#"
                  className="text-sm text-muted-foreground hover:text-accent transition-colors"
                >
                  About Us
                </a>
              </li>
              <li>
                <a
                  href="#"
                  className="text-sm text-muted-foreground hover:text-accent transition-colors"
                >
                  Contact
                </a>
              </li>
            </ul>
          </div>
        </div>

        {/* Copyright */}
        <div className="mt-8 border-t border-border pt-8">
          <p className="text-center text-sm text-muted-foreground">
            &copy; {new Date().getFullYear()} Wisteria. All rights reserved.
          </p>
        </div>
      </div>
    </footer>
  );
}
