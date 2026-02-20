"""Pydantic schemas for Order/Checkout request/response validation.

Schemas:
- CheckoutLineItem / CheckoutRequest: incoming checkout request from frontend
- CheckoutResponse: returns the Stripe checkout URL
- OrderItemResponse / OrderResponse: order data for API responses
"""

import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.order import OrderStatus


class CheckoutLineItem(BaseModel):
    """A single item in a checkout request. Only product_id — price comes from DB."""

    product_id: uuid.UUID


class CheckoutRequest(BaseModel):
    """Request body for POST /checkout/create-session."""

    items: list[CheckoutLineItem] = Field(min_length=1)


class CheckoutResponse(BaseModel):
    """Response from checkout session creation."""

    checkout_url: str
    session_id: str


class OrderItemResponse(BaseModel):
    """An order line item in API responses."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    order_id: uuid.UUID
    product_id: uuid.UUID | None
    product_name: str
    price_cents: int
    quantity: int


class OrderResponse(BaseModel):
    """Full order in API responses."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    customer_email: str
    customer_name: str
    stripe_checkout_session_id: str
    stripe_payment_intent_id: str | None
    status: OrderStatus
    total_cents: int
    shipping_address_json: dict
    items: list[OrderItemResponse]
    created_at: datetime
    updated_at: datetime
