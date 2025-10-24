from pydantic import BaseModel, Field, ConfigDict


# PUBLIC_INTERFACE
class ProductBase(BaseModel):
    """Shared product attributes for create/update operations."""
    name: str = Field(..., description="Product name (non-empty)")
    price: float = Field(..., ge=0, description="Unit price, must be >= 0")
    quantity: int = Field(..., ge=0, description="Available quantity, must be >= 0")

    model_config = ConfigDict(from_attributes=True)


# PUBLIC_INTERFACE
class ProductCreate(ProductBase):
    """Payload for creating a product with an explicit unique id."""
    id: int = Field(..., description="Unique product identifier (int, unique)")


# PUBLIC_INTERFACE
class ProductUpdate(ProductBase):
    """Payload for updating a product; id is taken from the path parameter."""
    pass


# PUBLIC_INTERFACE
class Product(ProductBase):
    """Response schema for a product resource."""
    id: int = Field(..., description="Unique product identifier")
