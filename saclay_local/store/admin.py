from django.contrib import admin
from .models import Product, Producer, Consumer, Production, Consumption


# ---- Inlines para editar produção/consumo a partir do Product ----

class ProductionInline(admin.TabularInline):
    model = Production
    extra = 1          # quantas linhas vazias aparecem
    autocomplete_fields = ["producer"]


class ConsumptionInline(admin.TabularInline):
    model = Consumption
    extra = 1
    autocomplete_fields = ["consumer"]


# ---- Product ----

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "quantity_available",
    )
    search_fields = ("name",)
    inlines = [ProductionInline, ConsumptionInline]


# ---- Producer ----

@admin.register(Producer)
class ProducerAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


# ---- Consumer ----

@admin.register(Consumer)
class ConsumerAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


# ---- Production ----

@admin.register(Production)
class ProductionAdmin(admin.ModelAdmin):
    list_display = (
        "product",
        "producer",
        "quantity_produced",
        "created_at",
    )
    list_filter = ("producer", "product", "created_at")
    search_fields = ("product__name", "producer__name")
    autocomplete_fields = ["product", "producer"]
    date_hierarchy = "created_at"


# ---- Consumption ----

@admin.register(Consumption)
class ConsumptionAdmin(admin.ModelAdmin):
    list_display = (
        "product",
        "consumer",
        "quantity_consumed",
        "created_at",
    )
    list_filter = ("consumer", "product", "created_at")
    search_fields = ("product__name", "consumer__name")
    autocomplete_fields = ["product", "consumer"]
    date_hierarchy = "created_at"
