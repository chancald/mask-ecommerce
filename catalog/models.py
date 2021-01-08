from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import User


CATEGORY_CHOICES = (
    ('C', 'Casual'),
    ('F', 'Formal'),
)
LABEL_CHOICES = (
    ('S', 'secondary'),
    ('P', 'primary'),
    ('D', 'danger'),
)
STATE_CHOICES = (
    ('SA', 'Santo Domingo'),
    ('SE', 'Santo Domingo Este'),
    ('SO', 'Santo Domingo Oeste'),
    ('SN', 'Santo Domingo Norte'),
)
PAYMENT_CHOICES = (
    ('EF', 'Efectivo'),
)

class Item(models.Model):
    title = models.CharField(max_length=40)
    price = models.IntegerField()
    discount_price = models.IntegerField(blank=True, null=True)
    slug = models.SlugField()
    status = models.name = models.CharField(max_length=200)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    label = models.CharField(choices=LABEL_CHOICES, max_length=2)
    description = models.TextField()
    image = models.ImageField(default='default.jpg', upload_to='static/images')

    def __str__(self):
        return self.title
    
    def get_add_to_cart_url(self):
        return reverse('add_to_cart', kwargs={'slug':self.slug})

    def get_remove_from_cart_url(self):
        return reverse('remove_from_cart', kwargs={'slug':self.slug})
    
    def get_add_item_quantity_url(self):
        return reverse('add_item_quantity', kwargs={'slug':self.slug})

    def get_remove_item_quantity_url(self):
        return reverse('remove_item_quantity', kwargs={'slug':self.slug})

    def get_remove_from_cart_summary_url(self):
        return reverse('remove_from_cart_summary', kwargs={'slug':self.slug})

class OrderItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    quantity = models.IntegerField(default=1)

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total_item_dicount_price(self):
        return self.quantity * self.item.discount_price

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_item_dicount_price()
        else:
            return self.get_total_item_price()

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_final_price()

class Promo(models.Model):
    promo_discount = models.FloatField()
    title = models.CharField(max_length=40)
    slug = models.SlugField()

    def __str__(self):
        return self.title

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    promo = models.ManyToManyField(Promo)
    address = models.ForeignKey("Address", on_delete=models.SET_NULL, blank=True, null=True)
    ordered = models.BooleanField(default=False)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()


    def __str__(self):
        return self.user.username
    
    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        if self.promo:
            for promo in self.promo.all():
                total *= (1 - promo.promo_discount)
        return round(total, 2)
    
    def get_promo_discount(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        for promo in self.promo.all():
            promo_discount = promo.promo_discount
        return total * promo_discount
    
class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=40)
    email = models.CharField(max_length=40)
    phone = models.CharField(max_length=40)
    street_address = models.CharField(max_length=200)
    street_address_2 = models.CharField(max_length=200)
    save_info = models.BooleanField(default=False)
    default = models.BooleanField(default=False)
    use_default = models.BooleanField(default=False)
    state_option = models.CharField(choices=STATE_CHOICES, max_length=2)
    payment_option = models.CharField(choices=PAYMENT_CHOICES, max_length=2)

    class Meta:
        verbose_name_plural = "Addresses"

    def __str__(self):
        return self.user.username
