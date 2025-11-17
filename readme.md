
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
bash
Copy code
git clone <repo-url>
cd inventory_system
2. Create virtual environment
bash
Copy code
python -m venv venv
source venv/bin/activate
3. Install dependencies
bash
Copy code
pip install -r requirements.txt
4. Apply database migrations
bash
Copy code
python manage.py migrate
5. Create a superuser
bash
Copy code
python manage.py createsuperuser
6. Run the server
bash
Copy code
python manage.py runserver
