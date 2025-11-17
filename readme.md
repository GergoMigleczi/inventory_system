# Inventory Management System

A modular, extensible **Django-based inventory management system** designed for real-world operational workflows:

- Product catalogue  
- Supplier management  
- Purchase Orders (POs)  
- Goods Receiving (GRVs)  
- Warehouse stock + batches  
- Generic reusable UI framework  

The system is structured for maintainability, scalability, and clarity, using Django 4, class-based views, a custom user model, and a clean domain-driven architecture.

---

## 📦 Features

### 🔑 Core System
- Custom user model with email authentication  
- Modular Django apps (`products`, `suppliers`, `warehouses`, `purchasing`, `accounts`)  
- Reusable shared UI templates  
- Standardised CRUD structure across all apps  

### 🏭 Inventory
- Warehouse model  
- Product batches with:
  - quantity  
  - expiry date  
  - lot numbers  
  - link to GRV line  
- Real-time batch-level stock visibility  

### 📄 Purchase Orders
- Create, edit, delete purchase orders  
- PO line items  
- Business rules enforced:
  - Only Draft POs can be edited  
  - Only Draft POs can add or remove line items  
- Configurable status flow (Draft → Submitted → Received/Closed)

### 📥 Goods Receipts (GRVs)
- Create GRV manually or from a PO (`?po=<id>`)  
- Auto-population of GRV header and line items  
- GRV line items represent quantities being received  
- GRV status flow (Draft → Closed → Cancelled)  
- On GRV closure:
  - Creates inventory batches  
  - Updates linked PO outstanding quantities  
  - Auto-closes PO if fully received by **closed** GRVs  

### 📊 Reusable UI Framework

One of the major architectural decisions in this project is the **generic, reusable UI system**, consisting of:

#### `list_base.html`
- Single template for all list views  
- Dynamic columns  
- Dynamic actions  
- Dropdown for extra actions  
- Uses `UrlBuilder` for constructing parameters dynamically  

#### `form_base.html`
- Shared form template  
- Uniform buttons  
- Compatible with all Django ModelForms  

#### `table.html`
- Shared dynamic table component  
- Driven entirely by `columns` + `rows` from each view  

#### `RecordHeader`
A structured helper used by list and nested list views:

- Displays the “top-level” record  
- Displays the immediate parent record  
- Provides contextual navigation when navigating down multiple layers  
- Prevents the user from feeling lost deep in nested data (e.g. PO → PO Lines → GRV → GRV Lines)

This greatly improves clarity when navigating layered business objects.

---

## 🏛 Architecture Overview

### 1. Modular Django Apps

products/
suppliers/
warehouses/
purchasing/
accounts/

Each app encapsulates its own domain logic and UI.

---

### 2. Business Logic Lives in Models

The system follows a **fat-model, thin-view** architecture.

Views remain clean and predictable because:

- Validation lives in `model.clean()`  
- Status transition logic lives inside the model  
- Save-time logic (e.g., generating batches, auto-closing POs) lives inside the model  

Examples:
- PO line items cannot be modified unless PO is in Draft  
- GRV cannot be edited unless Draft  
- GRV closure creates inventory batches + checks PO closure  
- PO cannot move backward in status  

---

### 3. Generic UI Implementation

#### `UrlBuilder`
A powerful abstraction for generating URLs dynamically.

It supports:
- row fields  
- kwargs from the current URL  
- static fields  
- callables  
- optional query strings  

Used in `list_base.html` to keep table actions generic.

#### `getattr_dynamic`
A custom template filter to dynamically read attributes based on column definitions.

#### Unified CRUD Views

Every CRUD screen follows the same pattern:

ListView → list_base.html
CreateView → form_base.html
UpdateView → form_base.html
DeleteView → confirm_delete.html


This allows you to scale to 50+ models without duplicating UI code.

---

## 🧠 Domain Model Summary

### Products & Suppliers
- Products belong to multiple suppliers through `SupplierProduct`
- Validation ensures each supplier-product pair is unique

### Warehouses & Inventory
- Batches represent real physical stock  
- Batches created from GRV line items  
- Each batch includes:
  - product  
  - warehouse  
  - quantity  
  - expiry date  
  - lot number  
  - link to its GRV line  

### Purchase Orders

PurchaseOrder
PurchaseOrderLine


Rules:
- Only Draft POs are editable  
- Only Draft POs can add/remove line items  
- No backwards status transitions  
- Outstanding logic considers:
  - Draft GRVs + Closed GRVs → auto-population  
  - Closed GRVs only → PO closure  
  - Cancelled GRVs → ignored  

### Goods Receipts

GoodsReceipt
GoodsReceiptLine


Behaviours:
- Can be created from a PO (`/goods_receipts/new/?po=ID`)  
- Auto-populates line items based on outstanding quantities  
- Closing a GRV:
  - Creates product batches  
  - Updates PO outstanding quantities  
  - If PO is now fully received → auto-close PO  
- Cannot be edited unless in Draft  
- Cancelled GRVs do not affect outstanding calculations  

---

## 🚀 Installation

### 1. Clone the repository
git clone <repo-url>
cd inventory_system

### 2. Create virtual environment
python -m venv venv
source venv/bin/activate

### 3. Install dependencies
pip install -r requirements.txt

### 4. Apply database migrations
python manage.py migrate

### 5. Create a superuser
python manage.py createsuperuser

### 6. Run the server
python manage.py runserver
