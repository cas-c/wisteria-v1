"""Rate limiter singleton.

slowapi is a FastAPI wrapper around the `limits` library. It works like
Flask-Limiter if you've used that.

**How it works:**
- You decorate a route with `@limiter.limit("5/minute")` to cap that
  endpoint at 5 requests per minute per client IP.
- When the limit is exceeded, slowapi raises `RateLimitExceeded`, which
  the exception handler in main.py converts to a 429 Too Many Requests response.
- Hit counts are stored in memory by default (fine for single-process dev).
  For production with multiple workers, use Redis as the storage backend.

**Why a separate module?**
The limiter instance needs to be imported by both `main.py` (to register
the exception handler) and individual routers (to decorate endpoints).
Putting it in main.py would create circular imports.
"""

from slowapi import Limiter
from slowapi.util import get_remote_address

# get_remote_address extracts the client IP from the request.
# Behind a reverse proxy (Railway, Vercel), you'd use a header like
# X-Forwarded-For instead. We'll update this at deploy time (Phase 7).
limiter = Limiter(key_func=get_remote_address)
