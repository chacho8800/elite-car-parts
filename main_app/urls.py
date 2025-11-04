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
    path("parts/make/<str:make>/", views.parts_by_make, name="parts-by-make"),
    path("parts/model/<str:model>/", views.parts_by_model, name="parts-by-model"),
    path('parts/price/', views.parts_by_price, name='parts-by-price'),

    path("parts/category/<str:category>/", views.parts_by_category, name="parts-by-category"),
    path('cart/', views.view_cart, name='view-cart'),
    path("cart/add/<int:part_id>", views.add_to_cart, name="add-to-cart"),
    path('cart/remove/<int:part_id>/', views.CartDelete.as_view(), name='cart-remove'),

    path("accounts/login/", views.Login.as_view(), name="login"),
    path("accounts/signup/", views.signup, name="signup"),
    path("accounts/logout/", LogoutView.as_view(next_page='/'), name="logout"),
    
    path("search/", views.search_part, name="search-part"),
    path("review/<int:part_id>/", views.add_review, name="add-review"),
    path('car/create/', views.CarCreate.as_view(), name='car-create'),
    path('car/<int:pk>/delete', views.CarDelete.as_view(), name='car-delete'),
    path('car/<int:pk>/update', views.CarUpdate.as_view(), name='car-update'),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
