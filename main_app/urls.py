from django.urls import path 
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('', views.home, name='home'),
    path("about/", views.about, name="about"),
    path("account/", views.account, name='account'),

    path("parts/", views.part_index, name="part-index"),
    path("parts/<int:part_id>", views.part_detail, name="part-detail"),
    path('cart/', views.view_cart, name='view-cart'),
    path("cart/add/<int:part_id>", views.add_to_cart, name="add-to-cart"),
    path('cart/remove/<int:part_id>/', views.CartDelete.as_view(), name='cart-remove'),

    path("accounts/login/", views.Login.as_view(), name="login"),
    path("accounts/signup/", views.signup, name="signup"),
    path("accounts/logout/", LogoutView.as_view(next_page='/'), name="logout"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
