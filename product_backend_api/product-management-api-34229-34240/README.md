# Product Management API

FastAPI backend providing CRUD endpoints for products.

- Runs in container product_backend_api on port 3001
- OpenAPI docs: http://localhost:3001/docs
- Endpoints:
  - GET /products
  - POST /products
  - GET /products/{id}
  - PUT /products/{id}
  - DELETE /products/{id}
  - GET /products/balance

## Product Model

```
{
  "id": int,          // unique
  "name": string,     // non-empty
  "price": float,     // >= 0
  "quantity": int     // >= 0
}
```

## Example cURL

List products:
```
curl -s http://localhost:3001/products | jq
```

Create product:
```
curl -X POST http://localhost:3001/products \
  -H 'Content-Type: application/json' \
  -d '{ "id": 1, "name": "Keyboard", "price": 49.99, "quantity": 10 }'
```

Get product:
```
curl -s http://localhost:3001/products/1 | jq
```

Update product:
```
curl -X PUT http://localhost:3001/products/1 \
  -H 'Content-Type: application/json' \
  -d '{ "name": "Keyboard Pro", "price": 59.99, "quantity": 8 }'
```

Delete product:
```
curl -X DELETE http://localhost:3001/products/1 -i
```

Get total balance (sum of price * quantity across all products):
```
curl -s http://localhost:3001/products/balance | jq
```

## Notes

- In-memory storage is used and will reset on container restart.
- Validation errors return HTTP 400; not found returns 404; create returns 201.
- Code is organized for easy swap to a real persistence layer later.
