from django.db import models

#Consts and Choices:
choices_type_of_person = [
    ("1", "Person"),
    ("2", "Company"),
]

choices_type_of_product = [
    ("1", "Product"),
    ("2", "Service"),
]

choices_type_of_payment = [
    ("1", "Cash"),
    ("2", "Credit Card"),
    ("3", "Mobile payments"),
    ("4", "Bank Transfer"),
]

class Client(models.Model):
    name = models.CharField("Name", max_length=64)
    doc = models.CharField("Doc", max_length=14, blank=True, null=True)
    phone = models.CharField("Phone", max_length=13, blank=True, null=True)
    address = models.TextField("Address", blank=True, null=True)
    type_person = models.CharField(
        "Type of Person",
        choices=choices_type_of_person,
        default="1",
        max_length=1,
    )

    class Meta:
        ordering = ['id']
    
    @property
    def get_sales(self):
        return SaleOrder.objects.filter(client=self)
    
    @property
    def get_sales_spent(self):
        return sum([order.total_value_order for order in SaleOrder.objects.filter(client=self)])

class Product(models.Model):
    name = models.CharField("Produto", max_length=64)
    price = models.FloatField("Price")
    weight = models.FloatField("Weight", blank=True, null=True)
    type_product = models.CharField(
        "Type of Product",
        choices=choices_type_of_product,
        default="1",
        max_length=1,
    )

    class Meta:
        ordering = ['id']

class SaleOrder(models.Model):
    client = models.ForeignKey("Client", verbose_name="Client", on_delete=models.SET_NULL, blank=True, null=True)
    date_order = models.DateField("Order Date", auto_now_add=True)
    total_value = models.FloatField("Total Value", blank=True, null=True)
    type_of_payment = models.CharField(
        "Type of Payment",
        choices=choices_type_of_payment,
        default="1",
        max_length=1,
    )

    class Meta:
        ordering = ['id']

    @property
    def lines(self):
        lines = SaleOrderLine.objects.filter(order=self.id)        
        return [{
            "product": line.product.name or "Produto",
            "quantity": line.quantity,
            "discount": line.discount,
            "total_value": line.calculated_total,
        } for line in lines]

    @property
    def total_value_order(self):
        # If the total value was not submitted, calculate using the lines...
        if self.total_value:
            return self.total_value
        else:
            lines = SaleOrderLine.objects.filter(order=self.id)
            return sum([line.calculated_total for line in lines])
            
class SaleOrderLine(models.Model):
    order = models.ForeignKey("SaleOrder", verbose_name="Order", on_delete=models.CASCADE, blank=True, null=True)
    product = models.ForeignKey("Product", verbose_name="Product", on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.FloatField("Quantity", default=1)
    discount = models.FloatField("Discount", default=0.0)
    total_value = models.FloatField("Total Value", blank=True, null=True)
    
    class Meta:
        ordering = ['id']

    @property
    def calculated_total(self):
        return (self.product.price * self.quantity) - self.discount

