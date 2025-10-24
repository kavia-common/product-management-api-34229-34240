from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers.products import router as products_router

openapi_tags = [
    {
        "name": "Health",
        "description": "Service health endpoints",
    },
    {
        "name": "Products",
        "description": "CRUD operations for product resources",
    },
]

app = FastAPI(
    title="Product Management API",
    description=(
        "A simple FastAPI service providing CRUD endpoints for products.\n\n"
        "Example curl commands:\n"
        "1) List products:\n"
        "   curl -s http://localhost:3001/products | jq\n\n"
        "2) Create product:\n"
        "   curl -X POST http://localhost:3001/products \\\n"
        "     -H 'Content-Type: application/json' \\\n"
        "     -d '{\"id\":1, \"name\":\"Keyboard\", \"price\":49.99, \"quantity\":10}'\n\n"
        "3) Get product:\n"
        "   curl -s http://localhost:3001/products/1 | jq\n\n"
        "4) Update product:\n"
        "   curl -X PUT http://localhost:3001/products/1 \\\n"
        "     -H 'Content-Type: application/json' \\\n"
        "     -d '{\"name\":\"Keyboard Pro\", \"price\":59.99, \"quantity\":8}'\n\n"
        "5) Delete product:\n"
        "   curl -X DELETE http://localhost:3001/products/1 -i\n"
    ),
    version="0.1.0",
    openapi_tags=openapi_tags,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Health"], summary="Health Check")
def health_check():
    """
    Health check endpoint.
    Returns 200 OK with a simple payload to indicate service health.
    """
    return {"message": "Healthy"}


# Register routers
app.include_router(products_router)
