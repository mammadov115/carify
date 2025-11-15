from django.views import View
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponseBadRequest, JsonResponse
from cars.models import Car
from spareparts.models import SparePart
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.shortcuts import redirect
from .models import Order, OrderItem
import json



class CreateOrderView(View):
    """
    Handles the creation of an order based on the provided product type and ID.
    Accepts POST requests and assigns the product (Car or SparePart) to the
    correct field within the Order model.
    """

    valid_types = ('car', 'sparepart')

    def get(self, request, *args, **kwargs):
        product_type = kwargs.get('product_type')
        product_id = kwargs.get('product_id')

        if product_type not in self.valid_types:
            return HttpResponseBadRequest("Invalid product type.")

        # order = Order(user=request.user, quantity=1)

        if product_type == 'car':
            product = Car.objects.get(id=product_id)
        else:
            product = Car.objects.get(id=product_id)

        # order.save()

        # Initialize cart if empty
        order_items = request.session.get("order_items", [])

        # Check if the same product already exists
        exists = any(
            item["type"] == product_type and item["id"] == product.id
            for item in order_items
        )


            # Append new item
        if not exists:
            order_items.append({
                "type": product_type,
                "id": product.id,
                "quantity": 1,
            })

        # Save back to session
        request.session["order_items"] = order_items
        request.session.modified = True
        return redirect('order-list')


class OrderListView(LoginRequiredMixin, View):
    """
    Fetches all order items from session and retrieves the corresponding
    Car or SparePart objects to display in template.
    """

    template_name = "order_list.html"

    def get(self, request):
        session_items = request.session.get("order_items", [])
        products = []
        quantity = 0
        total = 0

        for item in session_items:
            product_type = item.get("type")
            product_id = item.get("id")
            
            if product_type == "car":
                product = get_object_or_404(Car, id=product_id)
            elif product_type == "sparepart":
                product = get_object_or_404(SparePart, id=product_id)
            else:
                continue  # invalid type, skip

            # add quantity and price from session
            product.quantity = item.get("quantity", 1)
            product.session_price = item.get("price")
            product.type = product_type

            products.append(product)
            quantity += item.get("quantity", 1)
            total += product.price


        return render(request, self.template_name, {"orders": products, "total_quantity":quantity, "total": total})


class RemoveOrderItemView(LoginRequiredMixin, View):
    """
    Removes a product from session-based order list by type and id.
    """

    def get(self, request, product_type, product_id):
        order_items = request.session.get("order_items", [])

        # Filter out the product to remove
        order_items = [
            item for item in order_items
            if not (item["type"] == product_type and item["id"] == int(product_id))
        ]

        # Save back to session
        request.session["order_items"] = order_items
        request.session.modified = True

        return redirect("order-list")


class CreateOrderFromProductsView(LoginRequiredMixin, View):
    """
    Handles creating an Order with multiple products (Cars and SpareParts)
    from a POST request containing a products list, buyer_number, and notes.
    """

    def post(self, request, *args, **kwargs):
        try:
            # Parse JSON body
            data = json.loads(request.body)
            products = data.get("products", [])
            buyer_number = data.get("buyer_number", "")
            notes = data.get("notes", "")
        except json.JSONDecodeError:
            return HttpResponseBadRequest("Invalid JSON.")

        if not products or not buyer_number:
            return HttpResponseBadRequest("Products list and buyer_number are required.")

        # Create the main Order object
        order = Order.objects.create(
            user=request.user,
            buyer_number=buyer_number,
            notes=notes
        )

        # Loop through products and create OrderItem for each
        for item in products:
            product_type = item.get("type")
            product_id = item.get("id")
            quantity = item.get("quantity", 1)
            price = item.get("price", None)

            if product_type == "car":
                product_obj = Car.objects.filter(id=product_id).first()
            elif product_type == "sparepart":
                product_obj = SparePart.objects.filter(id=product_id).first()
            else:
                continue  # skip invalid type

            if not product_obj:
                continue  # skip if product not found

            # Create OrderItem
            OrderItem.objects.create(
                order=order,
                product_type=product_type,
                car=product_obj if product_type == "car" else None,
                spare_part=product_obj if product_type == "sparepart" else None,
                quantity=quantity,
                price=price
            )

        # Optionally, return JSON response or redirect
        return JsonResponse({"success": True, "order_id": order.id})
