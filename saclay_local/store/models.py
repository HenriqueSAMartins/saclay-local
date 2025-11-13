from django.db import models
from django.core.validators import MinValueValidator


# Create your models here.

# PRODUCERS = {
#   'ferme_viltain': {'name': 'Ferme_de_Viltain'},
#   'ferme_Henrique': {'name': 'Ferme_de_Henrique'},
# }

# PRODUCTS = [
#   {'name': 'yaourth_vanille', 'producers': [PRODUCERS['ferme_viltain']]},
#   {'name': 'yaourth_marron', 'producers': [PRODUCERS['ferme_viltain']]},
#   {'name': 'jus_de_pomme', 'producers': [PRODUCERS['ferme_viltain']]},
#   {'name': 'fromage_blanc', 'producers': [PRODUCERS['ferme_Henrique']]}
# ]

class Product(models.Model):
    name = models.CharField(max_length=120, unique=True)
    quantity_available = models.PositiveIntegerField(
        default=0, validators=[MinValueValidator(0)]
    )
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} (disp.: {self.quantity_available})"


class Producer(models.Model):
    name = models.CharField(max_length=120, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Consumer(models.Model):
    name = models.CharField(max_length=120, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Production(models.Model):
    """Relation Product–Producer + quantity produced."""
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="productions"
    )
    producer = models.ForeignKey(
        Producer, on_delete=models.CASCADE, related_name="productions"
    )
    quantity_produced = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (("product", "producer"),)
        indexes = [
            models.Index(fields=["product", "producer"]),
        ]

    def __str__(self):
        return f"{self.producer} → {self.product} ({self.quantity_produced})"


class Consumption(models.Model):
    """Relation Product–Consumer + quantity consumed."""
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="consumptions"
    )
    consumer = models.ForeignKey(
        Consumer, on_delete=models.CASCADE, related_name="consumptions"
    )
    quantity_consumed = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["product", "consumer"]),
        ]

    def __str__(self):
        return f"{self.consumer} ← {self.product} ({self.quantity_consumed})"
