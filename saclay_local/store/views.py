from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.template import loader
from .models import Product, Producer

# Create your views here.

# def index(request):
#     message = "Bienvenue sur le comptoir local de Paris Saclay!"
#     return HttpResponse(message)

def welcome(request):
    return HttpResponse("""
        <h1>Bienvenue !</h1>
        <p>Sur le comptoir local de Paris-Saclay.</p>
        <p><a href="/store/">Accéder au magasin</a></p>
    """)

# def index(request):
#    template = loader.get_template("./store/index.html")
#    return HttpResponse(template.render(request=request))

def index(request):
    products = Product.objects.all().order_by("name")
    context = {
        "products": products,
    }
    return render(request, "store/index.html", context)

def product_detail(request, product_id: int):
    """Ex: /store/2/  → 'Le nom du produit est ... Il a été produit par ...'"""
    product = get_object_or_404(Product, pk=product_id)

    # all producers that have Production rows for this product
    producers = Producer.objects.filter(productions__product=product).distinct()
    producers_list = ", ".join(p.name for p in producers) or "—"

    html = f"Le nom du produit est {product.name}. Il a été produit par {producers_list}"
    return HttpResponse(html)

def search_products_by_producer(request):
    """
    Ex: /store/search/?q=Ferme   → list products whose producer name contains 'Ferme'
    """
    query = request.GET.get("q", "").strip()
    if not query:
        return HttpResponse("<ul></ul>")

    products = (
        Product.objects
        .filter(productions__producer__name__icontains=query)
        .distinct()
        .order_by("name")
    )
    formatted = [f"<li>{p.name}</li>" for p in products]
    html = "<ul>" + "\n".join(formatted) + "</ul>"
    return HttpResponse(html)



# def product_list(request):
#     html = "<ul>"
#     for product in PRODUCTS:
#         name = product['name'].replace('_', ' ')
#         html += f"<li>{name}</li>"
#     html += "</ul>"
#     return HttpResponse(html)

# def informations_producer(request, producer_id):
#     # garantir que o id seja válido
#     if producer_id < 0 or producer_id >= len(PRODUCTS):
#         return HttpResponse("Produit introuvable", status=404)

#     # seleciona o produto
#     product = PRODUCTS[producer_id]
#     product_name = product['name'].replace('_', ' ')
#     producer_name = product['producers'][0]['name'].replace('_', ' ')

#     html = f"Le nom du produit est {product_name}. Il a été produit par {producer_name}"
#     return HttpResponse(html)

# def search_products_by_producer(request):
#     query = request.GET.get('query', '')
#     matching_products = []
#     for product in PRODUCTS:
#         for p in product['producers']:
#             if query == p['name']:
#                 matching_products.append(product['name'].replace('_', ' '))
#     html = "<ul>"
#     for product_name in matching_products:
#         html += f"<li>{product_name}</li>"
#     html += "</ul>"

#     return HttpResponse(html)