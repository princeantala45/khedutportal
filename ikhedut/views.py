from django.shortcuts import render,redirect
from .models import Cart,Cartitems,Contact,Signup,Ad,CropSale,Order,OrderItem

from django.db import transaction
from django.contrib import messages

# this is for login and logout built in feauters of Django
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import authenticate, login as auth_login


from django.utils import timezone
from datetime import timedelta
from django.shortcuts import get_object_or_404
# import requests
# from django.http import JsonResponse

# Create your views here.
def index(request):
    crops = CropSale.objects.filter(is_approved=True)
    return render(request, "index.html", {"crops": crops})

def crops(request):
    return render(request,"crops.html")

def agricultureguidance(request):
    return render(request,"agricultureguidance.html")

@login_required(login_url="/login")
def sellcrops(request):
    if request.method == "POST":
        try:
            CropSale.objects.create(
                seller=request.user,
                crop=request.POST.get("crop"),
                quantity=request.POST.get("quantity"),
                price=request.POST.get("price"),
                image=request.FILES.get("image"),
                is_approved=False
            )
            messages.success(request, "Crop submitted successfully. Waiting for admin approval.")
        except Exception:
            messages.error(request, "Something went wrong. Please try again.")

        return redirect("sellcrops")

    return render(request, "sellcrops.html")

@login_required(login_url="/login")
def buy_crops(request):
    sales = CropSale.objects.filter(is_approved=True)

    crops_dict = {}

    for sale in sales:
        crop_name = sale.crop

        if crop_name not in crops_dict:
            crops_dict[crop_name] = {
                "crop": crop_name,
                "product_id": sale.id,
                "total_quantity": sale.quantity,
                "price": sale.price,
                "image": sale.image,  # first image
            }
        else:
            crops_dict[crop_name]["total_quantity"] += sale.quantity            
            crops_dict[crop_name]["price"] = min(
                crops_dict[crop_name]["price"], sale.price
            )

    crops = crops_dict.values()

    return render(request, "buycrops.html", {"crops": crops})

def tractor(request):
    return render(request,"tractor.html")

def tillage(request):
    return render(request,"tillage.html")

def ox(request):
    return render(request,"ox.html")

def agrochemicals(request):
    return render(request,"agrochemicals.html")

def fertilizer(request):
    return render(request,"fertilizer.html")

@login_required(login_url="login")
def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        message = request.POST.get('message')
        Contact.objects.create(
            name=name,
                email=email,
            mobile=mobile,
            message=message
        )
        messages.success(request, "Your message has been sent successfully.")
        return redirect('contact')
    return render(request,'contact.html')


def signup(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        mobile = request.POST.get("mobile", "").strip()
        password = request.POST.get("password")
        repassword = request.POST.get("repassword")
        image=request.FILES.get("image")

        if not all([username, email, mobile, password, repassword]):
            messages.error(request, "All fields are required")
            return render(request, "signup.html")

        if password != repassword:
            messages.error(request, "Passwords do not match")
            return render(request, "signup.html")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return render(request, "signup.html")

        # CREATE USER (this MUST be outside the if)
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        # CREATE PROFILE
        Signup.objects.create(
            user=user,
            mobile=mobile,
            image=image
        )

        messages.success(request, "Registration successful")
        return redirect("login")

    return render(request, "signup.html")


def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            return redirect("/")
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "login.html")

def logout(request):
    if request.method == "POST":
        auth_logout(request)
    return redirect("/")
 
@login_required(login_url="login")
def cart(request):
    if request.method == "POST":
        crop_id = request.POST.get("crop_id")
        quantity = int(request.POST.get("quantity", 20))

        product = CropSale.objects.get(id=crop_id)

        cart, created = Cart.objects.get_or_create(
            user=request.user,
            is_paid=False
        )

        cart_item, created = Cartitems.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={"quantity": quantity}
        )

        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        messages.success(request, "Item added to cart")
        return redirect("cart")

    cart = Cart.objects.filter(user=request.user, is_paid=False).first()

    if not cart:
        return render(request, "cart.html", {
            "items": [],
            "total": 0
        })

    items = cart.items.select_related("product")
    total = sum(item.subtotal for item in items)

    return render(request, "cart.html", {
        "items": items,
        "total": round(total, 2)
    })

@login_required(login_url="/login")
def postedadvertisement(request):
    ads = Ad.objects.filter(is_approved=True)
    return render(request, "postedadvertisement.html", {"ads": ads})

@login_required(login_url="login")
def postadvertisement(request):
    if request.method == "POST":
        Ad.objects.create(
        user=request.user,   # IMPORTANT
        fullname=request.POST.get("fullname"),
        mobile=request.POST.get("mobile"),
        city=request.POST.get("city"),
        productname=request.POST.get("productname"),
        description=request.POST.get("description"),
        price=request.POST.get("price"),
        image=request.FILES.get("image"),
        )

        messages.success(request, "Advertisement submitted for approval to admin.")
    return render(request,'postadvertisement.html')
   
@login_required(login_url="login")
def remove_from_cart(request, item_id):
    item = Cartitems.objects.get(id=item_id)
    item.delete()
    messages.success(request, "Item removed from cart")
    return redirect("cart")

@login_required(login_url="/login")
def checkout(request):
    cart = Cart.objects.filter(user=request.user, is_paid=False).first()

    if not cart or not cart.items.exists():
        return redirect("cart")

    items = cart.items.select_related("product")
    total = sum(item.subtotal for item in items)

    if request.method == "POST":
        with transaction.atomic():

            # stock validation FIRST
            for item in items:
                product = item.product
                if not product or product.quantity < item.quantity:
                    messages.error(
                        request,
                        f"Not enough stock for {product.crop if product else 'a product'}"
                    )
                    return redirect("cart")

            payment_method = request.POST.get("payment_method")

            card_number = card_expiry = card_cvv = upi_id = None

            if payment_method == "CARD":
                card_number = request.POST.get("cardnumber")
                card_expiry = request.POST.get("expiry")
                card_cvv = request.POST.get("cvv")
            elif payment_method == "UPI":
                upi_id = request.POST.get("upi_id")

            order = Order.objects.create(
                user=request.user,
                fullname=request.POST.get("fullname"),
                mobile=request.POST.get("mobile"),
                city=request.POST.get("city"),
                pincode=request.POST.get("pincode"),
                address=request.POST.get("address"),
                payment_method=payment_method,
                card_number=card_number,
                card_expiry=card_expiry,
                card_cvv=card_cvv,
                upi_id=upi_id,
                total_amount=total,
            )

            for item in items:
                product = item.product

                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=item.quantity,
                    price=item.subtotal
                )

                product.quantity -= item.quantity
                product.save()

            cart.is_paid = True
            cart.save()

        return redirect("order_success")

    return render(request, "checkout.html", {
        "items": items,
        "total": total,
    })

def order_success(request):
    return render(request, "order_success.html")

def spraypump(request):
    return render(request,'spraypump.html')


# def city_weather(request):
#     city = request.GET.get("city")

#     if not city:
#         return JsonResponse({"error": "City required"})

#     api_key = "6628d7a8b1f449a3aab95433252312"
#     url = "https://api.weatherapi.com/v1/current.json"

#     params = {
#         "key": api_key,
#         "q": city,
#     }

#     try:
#         res = requests.get(url, params=params, timeout=10).json()

#         # API error handling
#         if "error" in res:
#             return JsonResponse({"error": res["error"]["message"]})

#         data = {
#             "city": res["location"]["name"],
#             "region": res["location"]["region"],
#             "temp": res["current"]["temp_c"],
#             "condition": res["current"]["condition"]["text"],
#             "icon": res["current"]["condition"]["icon"],
#             "humidity": res["current"]["humidity"],
#             "wind": res["current"]["wind_kph"],
#         }

#         return JsonResponse(data)

#     except Exception as e:
#         return JsonResponse({"error": "Server error"})


@login_required(login_url="/login")
def userprofile(request):
    user = request.user

    # extra signup info (FIXED)
    profile = Signup.objects.filter(user=user).first()

    # user orders
    orders = Order.objects.filter(user=user).order_by("-created_at")

    # user ads
    ads = Ad.objects.filter(user=user).order_by("-id")

    return render(request, "userprofile.html", {
        "user": user,
        "profile": profile,
        "orders": orders,
        "ads": ads,
    })

@login_required(login_url="/login")
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    if not order.can_cancel():
        messages.error(request, "Order can no longer be cancelled.")
        return redirect("userprofile")

    order.status = "cancelled"
    order.save()

    messages.success(request, "Order cancelled successfully.")
    return redirect("userprofile")

@login_required(login_url="/login")
def request_cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    if not order.can_cancel():
        messages.error(request, "Cancellation time expired.")
        return redirect("userprofile")

    order.status = "cancel_requested"
    order.cancel_requested_at = timezone.now()
    order.save()

    messages.success(
        request,
        "Cancellation request sent to admin."
    )
    return redirect("userprofile")
