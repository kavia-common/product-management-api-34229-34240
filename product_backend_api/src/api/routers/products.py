from typing import List
from fastapi import APIRouter, HTTPException, status
from ..schemas.product import Product, ProductCreate, ProductUpdate
from ..repositories.product_repository import product_repository

router = APIRouter(
    prefix="/products",
    tags=["Products"],
)


@router.get(
    "",
    response_model=List[Product],
    summary="List products",
    description="Retrieve all products.",
    responses={
        200: {"description": "List of products returned successfully."}
    },
)
# PUBLIC_INTERFACE
def list_products() -> List[Product]:
    """Return all products."""
    return [Product(**p) for p in product_repository.list_products()]


@router.post(
    "",
    response_model=Product,
    status_code=status.HTTP_201_CREATED,
    summary="Create product",
    description="""
Create a new product.

Example:
curl -X POST http://localhost:3001/products \\
  -H 'Content-Type: application/json' \\
  -d '{ "id": 1, "name": "Keyboard", "price": 49.99, "quantity": 10 }'
""",
    responses={
        201: {"description": "Product created successfully."},
        400: {"description": "Validation error or duplicate id."},
    },
)
# PUBLIC_INTERFACE
def create_product(payload: ProductCreate) -> Product:
    """Create a product; id must be unique, name non-empty, price>=0, quantity>=0."""
    # Additional validation not covered by type constraints
    if not payload.name.strip():
        raise HTTPException(status_code=400, detail="name must be non-empty")

    if product_repository.exists(payload.id):
        raise HTTPException(status_code=400, detail="id must be unique")

    product_dict = payload.model_dump()
    product_repository.create_product(product_dict)
    return Product(**product_dict)


@router.get(
    "/{product_id}",
    response_model=Product,
    summary="Get product by id",
    description="Retrieve a product by its id.",
    responses={
        200: {"description": "Product found."},
        404: {"description": "Product not found."},
    },
)
# PUBLIC_INTERFACE
def get_product(product_id: int) -> Product:
    """Get a single product by id or 404 if not found."""
    prod = product_repository.get_product(product_id)
    if not prod:
        raise HTTPException(status_code=404, detail="Product not found")
    return Product(**prod)


@router.put(
    "/{product_id}",
    response_model=Product,
    summary="Update product",
    description="""
Update a product by id.

Example:
curl -X PUT http://localhost:3001/products/1 \\
  -H 'Content-Type: application/json' \\
  -d '{ "name": "Keyboard Pro", "price": 59.99, "quantity": 8 }'
""",
    responses={
        200: {"description": "Product updated."},
        400: {"description": "Validation error."},
        404: {"description": "Product not found."},
    },
)
# PUBLIC_INTERFACE
def update_product(product_id: int, payload: ProductUpdate) -> Product:
    """Update a product's fields; requires existing product."""
    if not payload.name.strip():
        raise HTTPException(status_code=400, detail="name must be non-empty")

    if not product_repository.exists(product_id):
        raise HTTPException(status_code=404, detail="Product not found")

    product_dict = {"id": product_id, **payload.model_dump()}
    product_repository.update_product(product_id, product_dict)
    return Product(**product_dict)


@router.delete(
    "/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete product",
    description="""
Delete a product by id.

Example:
curl -X DELETE http://localhost:3001/products/1
""",
    responses={
        204: {"description": "Product deleted."},
        404: {"description": "Product not found."},
    },
)
# PUBLIC_INTERFACE
def delete_product(product_id: int) -> None:
    """Delete a product; 404 if it does not exist."""
    if not product_repository.exists(product_id):
        raise HTTPException(status_code=404, detail="Product not found")
    product_repository.delete_product(product_id)
    return None
