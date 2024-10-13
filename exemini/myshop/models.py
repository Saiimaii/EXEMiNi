from django.db import models
from django.contrib.auth.models import User


class DatashopManager(models.Manager):
    def create_datashop(self, user, datesend, num_order, order, product, quantity, totalPrece, address, message):
        datashop = self.create(
            user=user,
            datesend=datesend,
            num_order=num_order,
            order=order,
            product=product,
            quantity=quantity,
            totalPrece=totalPrece,
            address=address,
            message=message,
        )
        return datashop
    
class Datashop(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    datesend = models.DateField()
    num_order = models.CharField(max_length=20)
    order = models.TextField()
    product = models.CharField(max_length=100)
    quantity = models.IntegerField()
    totalPrece = models.DecimalField(max_digits=10, decimal_places=2)
    address = models.TextField()
    message = models.TextField(null=True, blank=True)
    payments_status = models.CharField(
        "การชำระเงิน",
        max_length=50,
        choices=[
            ('รอร้านตรวจสอบ', 'Checked'),
            ('รอการชำระเงิน', 'Pending'),
            ('ชำระเงินเรียบร้อยแล้ว', 'Paid')
        ],
        default='รอร้านตรวจสอบ'
    )
    products_status = models.CharField(
        "สถานะสินค้า",
        max_length=50,
        choices=[
            ('รอกดรับสินค้า', 'Received'),
            ('กำลังทำสินค้า', 'Processing'),
            ('จัดส่งเรียบร้อยแล้ว', 'Shipped')
        ],
        default='รอกดรับสินค้า'
    )

    def __str__(self):
        return self.order

