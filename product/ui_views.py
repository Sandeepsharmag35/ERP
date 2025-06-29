from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.db.models import Q
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.urls import reverse
from .models import Product, Uom, ProductUom
from .forms import ProductForm, UomForm, ProductUomForm


def product_list(request):
    """List/search products with HTMX support"""
    search_query = request.GET.get("search", "")
    products = Product.objects.select_related("base_uom").all()

    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) | Q(product_code__icontains=search_query)
        )

    # Handle HTMX requests
    if request.headers.get("HX-Request"):
        return render(
            request,
            "product/partials/product_table.html",
            {"products": products, "search_query": search_query},
        )

    # Handle JSON API requests
    if request.headers.get("Accept") == "application/json":
        products_data = [
            {
                "id": p.id,
                "product_code": p.product_code,
                "name": p.name,
                "base_uom": str(p.base_uom),
                "costing_method": p.get_costing_method_display(),
                "tracking_method": p.get_tracking_method_display(),
                "is_active": p.is_active,
            }
            for p in products
        ]
        return JsonResponse({"products": products_data})

    return render(
        request,
        "product/product_list.html",
        {"products": products, "search_query": search_query},
    )


@require_http_methods(["GET", "POST"])
def product_create(request):
    """Create new product"""
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.save()

            messages.success(request, f'Product "{product.name}" created successfully!')

            # Handle HTMX redirect
            if request.headers.get("HX-Request"):
                response = HttpResponse()
                response["HX-Redirect"] = reverse("product-list")
                return response

            return redirect("product-list")
        else:
            # Handle HTMX form errors
            if request.headers.get("HX-Request"):
                return render(
                    request,
                    "product/partials/product_form.html",
                    {
                        "form": form,
                        "action_url": reverse("product-create"),
                        "submit_text": "Create Product",
                    },
                )
    else:
        form = ProductForm()

    if request.headers.get("HX-Request"):
        return render(
            request,
            "product/partials/product_form.html",
            {
                "form": form,
                "action_url": reverse("product-create"),
                "submit_text": "Create Product",
            },
        )

    return render(
        request,
        "product/partials/product_form.html",
        {
            "form": form,
            "title": "Create Product",
            "action_url": reverse("product-create"),
            "submit_text": "Create Product",
        },
    )


def product_detail(request, pk):
    """Product detail view"""
    product = get_object_or_404(Product, pk=pk)
    product_uoms = ProductUom.objects.filter(product=product).select_related("uom")

    return render(
        request,
        "product/product_detail.html",
        {"product": product, "product_uoms": product_uoms},
    )


def uom_list(request):
    """List UoMs with HTMX support"""
    search_query = request.GET.get("search", "")
    uoms = Uom.objects.all()

    if search_query:
        uoms = uoms.filter(
            Q(name__icontains=search_query)
            | Q(code__icontains=search_query)
            | Q(category__icontains=search_query)
        )

    # Handle HTMX requests
    if request.headers.get("HX-Request"):
        return render(
            request,
            "product/partials/uom_table.html",
            {"uoms": uoms, "search_query": search_query},
        )

    # Handle JSON API requests
    if request.headers.get("Accept") == "application/json":
        uoms_data = [
            {
                "id": u.id,
                "code": u.code,
                "name": u.name,
                "category": u.category,
                "conversion_to_si": str(u.conversion_to_si),
            }
            for u in uoms
        ]
        return JsonResponse({"uoms": uoms_data})

    return render(
        request, "product/uom_list.html", {"uoms": uoms, "search_query": search_query}
    )


@require_http_methods(["GET", "POST"])
def uom_create(request):
    """Create new UoM"""
    if request.method == "POST":
        form = UomForm(request.POST)
        if form.is_valid():
            uom = form.save()
            messages.success(request, f'UoM "{uom.name}" created successfully!')

            # Handle HTMX redirect
            if request.headers.get("HX-Request"):
                response = HttpResponse()
                response["HX-Redirect"] = reverse("uom-list")
                return response

            return redirect("uom-list")
        else:
            # Handle HTMX form errors
            if request.headers.get("HX-Request"):
                return render(
                    request,
                    "product/partials/uom_form.html",
                    {
                        "form": form,
                        "action_url": reverse("uom-create"),
                        "submit_text": "Create UoM",
                    },
                )
    else:
        form = UomForm()

    if request.headers.get("HX-Request"):
        return render(
            request,
            "product/partials/uom_form.html",
            {
                "form": form,
                "action_url": reverse("uom-create"),
                "submit_text": "Create UoM",
            },
        )

    return render(
        request,
        "product/partials/uom_form.html",
        {
            "form": form,
            "title": "Create UoM",
            "action_url": reverse("uom-create"),
            "submit_text": "Create UoM",
        },
    )


@require_http_methods(["GET", "POST"])
def product_uom_create(request, product_pk):
    """Add UoM to product"""
    product = get_object_or_404(Product, pk=product_pk)

    if request.method == "POST":
        form = ProductUomForm(request.POST)
        if form.is_valid():
            product_uom = form.save(commit=False)
            product_uom.product = product
            product_uom.save()

            messages.success(request, f"UoM added to product successfully!")
            return redirect("product-detail", pk=product.pk)

    return redirect("product-detail", pk=product.pk)
