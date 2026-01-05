from django.urls import path
from .views import (
    home, add_to_cart, cart_view,
    increase_qty, decrease_qty, remove_item,
    signup_view, login_view, logout_view
)

app_name = 'store'

urlpatterns = [
    path('', home, name='home'),
    path('add/<int:id>/', add_to_cart, name='add'),
    path('cart/', cart_view, name='cart'),
    path('increase/<int:id>/', increase_qty, name='increase'),
    path('decrease/<int:id>/', decrease_qty, name='decrease'),
    path('remove/<int:id>/', remove_item, name='remove'),

    # AUTH
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]
