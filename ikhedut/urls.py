from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from ikhedut import views
from django.contrib.auth import login

urlpatterns = [
    path("",views.index,name="ikhedut"),
    path("agricultureguidance/",views.agricultureguidance,name="agricultureguidance"),
    path("sellcrops/",views.sellcrops,name="sellcrops"),
    path("tractor/",views.tractor,name="tractor"),
    path("tillage/",views.tillage,name="tillage"),
    path("ox/",views.ox,name="ox"),
    path("agrochemicals/",views.agrochemicals,name="agrochemicals"),
    path("fertilizer/",views.fertilizer,name="fertilizer"),
    path("contact/",views.contact,name="contact"),
    path("signup/",views.signup,name="signup"),
    path("logout/",views.logout,name="logout"),
    path("login/",views.user_login,name="login"),
    path("userprofile/",views.userprofile,name="userprofile"),    
    path("buycrops/", views.buy_crops, name="buycrops"),
    path("cart/",views.cart,name="cart"),
    path("postadvertisement/",views.postadvertisement,name="postadvertisement"),
    path("postedadvertisement/",views.postedadvertisement,name="postedadvertisement"),
    path("remove-cart/<int:item_id>/", views.remove_from_cart, name="remove_from_cart"),
    path("checkout/", views.checkout, name="checkout"),
    path("order_success/", views.order_success, name="order_success"),
    path("spraypump/", views.spraypump, name="spraypump"),
    path("order/cancel/<int:order_id>/", views.cancel_order, name="cancel_order"),
    path("order/request-cancel/<int:order_id>/",views.request_cancel_order,name="request_cancel_order"),
    # path("city-weather/", views.city_weather, name="city_weather"), 
    ]

# if settings.DEBUG:
#     urlpatterns += static(
#         settings.MEDIA_URL,
#         document_root=settings.MEDIA_ROOT
#     )


