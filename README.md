# Dynamic Pricing System

This project is a dynamic pricing system that calculates product prices based on various pricing rules and applies discounts, including tiered discounts. It is built using Django and Django REST Framework (DRF) to expose functionality via a RESTful API.

## Features

- **Product Management**: Handles different types of products, each with its own pricing rules (Seasonal, Bulk, Premium).
- **Discount Management**: Supports different discount types including percentage-based, fixed amount, and tiered discounts.
- **Order Management**: Allows you to manage orders, apply multiple discounts, and calculate the total price.
- **RESTful API**: Provides endpoints to interact with products, orders, and discounts.

## Technologies Used

- **Django**: A high-level Python web framework.
- **Django REST Framework (DRF)**: Toolkit for building Web APIs in Django.
- **MySQL**: Database to store product, order, and discount data.

## Setup Instructions

### Prerequisites

- Python 3.x
- MySQL (or another relational database)
- Git

**API Usage**

**Products Endpoints**
-POST /products/: Create a new product.
-GET /products/: Retrieve all products.
-GET /products/{id}/: Retrieve a product by its ID.
-PUT /products/{id}/: Update an existing product.
-DELETE /products/{id}/: Delete a product.

**Orders Endpoints**
-POST /orders/: Create a new order with products and discounts.
-GET /orders/{id}/: Retrieve an order by its ID.
-GET /orders/: Retrieve all orders.
-POST /orders/{id}/calculate_total/: Calculate and get the total order price after applying all discounts.

**Discounts Endpoints**
-POST /discounts/: Create a new discount.
-GET /discounts/: Retrieve all discounts.
-GET /discounts/{id}/: Retrieve a discount by its ID.
-PUT /discounts/{id}/: Update an existing discount.
-DELETE /discounts/{id}/: Delete a discount.
