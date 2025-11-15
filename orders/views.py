from django.views import View
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponseBadRequest, JsonResponse
from cars.models import Car
from spareparts.models import SparePart
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.shortcuts import redirect
from .models import Order, OrderItem
from django.contrib import messages


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
                "price": float(product.price)
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
            print(total, product.price)
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
    Creates an Order using:
    - Product list from session
    - buyer_number, notes, total from POST form
    """

    def post(self, request, *args, **kwargs):
        # 1. Get products from session
        cart = request.session.get("order_items", {})

        if not cart:
            return HttpResponseBadRequest("Cart is empty.")

        # 2. Get form data
        buyer_number = request.POST.get("phone")
        notes = request.POST.get("notes", "")

        if not buyer_number:
            messages.error(request, "Number is required." )
            return redirect("orders")




        # 3. Create Order
        order = Order.objects.create(
            user=request.user,
            buyer_number=buyer_number,
            notes=notes,
        )

        # 4. Loop through cart items
        total = 0
        for item in cart:
            product_type = item.get("type")
            product_id = item.get("id")
            quantity = item.get("quantity", 1)
            price = item.get("price")
            total += price

            if product_type == "car":
                product_obj = Car.objects.filter(id=product_id).first()
            elif product_type == "sparepart":
                product_obj = SparePart.objects.filter(id=product_id).first()
            else:
                continue

            if not product_obj:
                continue
            
            order.total = total
            order.save()


            OrderItem.objects.create(
                order=order,
                product_type=product_type,
                car=product_obj if product_type == "car" else None,
                spare_part=product_obj if product_type == "sparepart" else None,
                quantity=quantity,
                price=product_obj.price
            )

        # Clear cart after successful order
        # if "order_items" in request.session:
        #     del request.session["order_items"]

        return render(request, "order_list.html")