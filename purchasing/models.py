from django.db import models
from suppliers.models import Supplier
from warehouses.models import Warehouse, ProductBatch
from products.models import Product
from django.conf import settings
from django.core.exceptions import ValidationError


###############################
# PURCHASE ORDERS
###############################

class PurchaseOrder(models.Model):
    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("submitted", "Submitted"),
        ("received", "Received"),
        ("cancelled", "Cancelled"),
    ]

    ALLOWED_STATUS_TRANSITIONS = {
        "draft": {"submitted", "cancelled"},
        "submitted": {"received", "cancelled"},
        "received": set(),      # no transitions from here
        "cancelled": set(),     # locked
    }

    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT)
    ordered_at = models.DateTimeField()
    expected_at = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft")
    reference = models.CharField(max_length=100, blank=True)

    @property
    def number(self):
        return f"PO{self.id:06d}"
    
    def __str__(self):
        return f"PO{self.id:06d}"
    
    def clean(self):
        if not self.pk:
            return  # new PO, no checks yet

        old = PurchaseOrder.objects.get(pk=self.pk)

        # Status change?
        if old.status != self.status:
            allowed = self.ALLOWED_STATUS_TRANSITIONS[old.status]

            if self.status not in allowed:
                raise ValidationError(
                    f"Cannot change status from '{old.status}' to '{self.status}'. "
                    f"Allowed: {', '.join(allowed) or 'None'}."
                )

        # Prevent editing fields when not draft
        if old.status != "draft":
            changed_fields = []
            for field in ["supplier_id", "warehouse_id", "ordered_at", "expected_at", "reference"]:
                if getattr(self, field) != getattr(old, field):
                    changed_fields.append(field)

            if changed_fields:
                raise ValidationError("Cannot modify purchase order details unless in Draft.")
            
    def save(self, *args, **kwargs):
        self.full_clean()  # calls clean()
        super().save(*args, **kwargs)

    def is_fully_received(self):
        """
        A PO is fully received if all PO lines have zero outstanding_for_po_closure().
        Uses Closed GRVs only.
        """
        return all(
            line.outstanding_for_po_closure() <= 0
            for line in self.lines.all()
        )



class PurchaseOrderLine(models.Model):
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, related_name="lines")
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
    
    def clean(self):
        if self.purchase_order.status != "draft":
            raise ValidationError("Cannot modify line items unless the purchase order is in Draft")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    
    def received_quantity_with_status(self, statuses):
        """
        Sum quantities for GRV lines where the parent GRV
        has a status within the provided list.
        Always excludes cancelled GRVs.
        """
        return sum(
            line.quantity
            for line in self.receipts.filter(goods_receipt__status__in=statuses)
        )
    
    def outstanding_for_grv(self):
        return self.quantity - self.received_quantity_with_status(["draft", "closed"])
    
    def outstanding_for_po_closure(self):
        return self.quantity - self.received_quantity_with_status(["closed"])




###############################
# GOODS RECEIPT (GRV)
###############################

class GoodsReceipt(models.Model):
    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("closed", "Closed"),
        ("cancelled", "Cancelled"),
    ]

    ALLOWED_STATUS_TRANSITIONS = {
        "draft": {"closed"},
        "closed": set(),      # no transitions from here
    }

    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.SET_NULL, null=True, blank=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT)
    received_at = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft")
    reference = models.CharField(max_length=100, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    @property
    def number(self):
        return f"GRV{self.id:06d}"
    
    def __str__(self):
        return f"GRV{self.id:06d}"
    
    def clean(self):
        if not self.pk:
            return  # new GRV, no checks yet

        old = GoodsReceipt.objects.get(pk=self.pk)

        # Status change?
        if old.status != self.status:
            allowed = self.ALLOWED_STATUS_TRANSITIONS[old.status]

            if self.status not in allowed:
                raise ValidationError(
                    f"Cannot change status from '{old.status}' to '{self.status}'. "
                    f"Allowed: {', '.join(allowed) or 'None'}."
                )

        # Prevent editing fields when not draft
        if old.status != "draft":
            changed_fields = []
            for field in ["purchase_order_id", "supplier_id", "warehouse_id", "received_at", "reference", "created_by_id"]:
                if getattr(self, field) != getattr(old, field):
                    changed_fields.append(field)

            if changed_fields:
                raise ValidationError("Cannot modify GRV details unless in Draft.")
        
        # Prevent closing if expiry dates missing
        if self.status == "closed":
            if self.lines.filter(expiry_date__isnull=True).exists():
                raise ValidationError("All GRV line items must have an expiry date before closing.")

            
    def save(self, *args, **kwargs):
        self.full_clean()  # calls clean()
        is_new = self.pk is None
        old_status = None

        if not is_new:
            old_status = GoodsReceipt.objects.get(pk=self.pk).status

        super().save(*args, **kwargs)

        # After saving → detect if we transitioned to CLOSED
        if old_status != "closed" and self.status == "closed":
            self.handle_closure()

    def handle_closure(self):
        """
        Perform necessary actions when a GRV is closed:
        1. Create inventory ProductBatch entries.
        2. Check if linked PO can be closed.
        """

        # 1. CREATE PRODUCT BATCHES FROM GRV LINE ITEMS
        for line in self.lines.select_related("product"):
            ProductBatch.objects.create(
                goods_receipt_line=line,
                product=line.product,
                warehouse=self.warehouse,
                quantity=line.quantity,
                expiry_date=line.expiry_date,
            )

        # 2. IF GRV LINKED TO A PO → SEE IF PO CAN BE CLOSED
        if self.purchase_order:
            po = self.purchase_order

            if po.is_fully_received():
                po.status = "received"
                po.save()



class GoodsReceiptLine(models.Model):
    goods_receipt = models.ForeignKey(GoodsReceipt, on_delete=models.CASCADE, related_name="lines")
    purchase_order_line = models.ForeignKey(PurchaseOrderLine, on_delete=models.PROTECT, related_name="receipts", null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    expiry_date = models.DateField(null=True, blank=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def number(self):
        return f"LINE{self.id:06d}"
    
    def __str__(self):
        return f"{self.goods_receipt.number}, {self.number}"
    
    def clean(self):
        if self.goods_receipt.status != "draft":
            raise ValidationError("Cannot modify line items unless the GRV is in Draft")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

