# Z: API Documentation Standards

## RESTful Conventions
- URL: `https://api.example.com/v2/{resources}/{id}/{sub-resources}`
- Nouns only, no verbs: `/orders` not `/getOrders`
- Plural for collections: `/users`, `/users/123`
- Actions as sub-resources: `/users/123/activate`
- Version in URL path: `/v2/...` (not header-based versioning)

## Request/Response Format
```json
{
  "data": { ... },           // single object or array
  "meta": {                  // pagination, etc.
    "page": 1,
    "per_page": 20,
    "total": 142,
    "total_pages": 8
  },
  "error": null              // null on success
}
```

## Pagination
- **Page-based**: `?page=1&per_page=20` (default 20, max 100)
- **Cursor-based**: `?cursor=eyJsYXN0X2lkIjogeyJpZCI6IDQyfX0=&limit=20`
- Response includes: `Link` header for prev/next/first/last
- Cursor recommended for real-time feeds (stable ordering)

## Error Codes
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Email is required",
    "details": [{ "field": "email", "reason": "required" }],
    "trace_id": "abc-123-def"
  }
}
```
- HTTP 400: `VALIDATION_ERROR`, `MISSING_FIELD`, `INVALID_FORMAT`
- HTTP 401: `UNAUTHORIZED`, `TOKEN_EXPIRED`, `TOKEN_INVALID`
- HTTP 403: `FORBIDDEN`, `INSUFFICIENT_PERMISSIONS`
- HTTP 404: `NOT_FOUND`, `RESOURCE_DELETED`
- HTTP 429: `RATE_LIMITED` (include `Retry-After` header)
- HTTP 5xx: `INTERNAL_ERROR` (no internal details leaked)

## Authentication
- **Bearer JWT**: `Authorization: Bearer <token>`
- **API Key** (for server-to-server): `X-API-Key: <key>`
- Rate limit headers: `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`
