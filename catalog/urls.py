from django.urls import path
from catalog.views import show_catalog
from . import views

app_name = 'catalog'

urlpatterns = [
    path('', show_catalog, name='show_catalog'),
    path('store/add/', views.create_store, name='create_store'),
    path('store/edit/<uuid:store_id>/', views.edit_store, name='edit_store'),
    path('store/delete/<uuid:store_id>/', views.delete_store, name='delete_store'),
    path('store/<uuid:store_id>/', views.store_detail, name='store_detail'),
    path('store/<uuid:store_id>/add_product_to_store/', views.add_product_to_store, name='add_product_to_store'),
    path('product/<uuid:product_id>/edit/', views.edit_product, name='edit_product'),
    path('product/<uuid:product_id>/delete/', views.delete_product, name='delete_product'),
    path('xml/', views.show_xml, name='show_xml'),
    path('json/', views.show_json, name='show_json'),
    path('xml/<str:id>/', views.show_xml_by_id, name='show_xml_by_id'),
    path('json/<str:id>/', views.show_json_by_id, name='show_json_by_id'),
    path('products/json/', views.product_list_json, name='product_list_json'),
    path('store/<uuid:store_id>/products/json/', views.product_list_store_json, name='product_list_store_json'),
    path('products/json/<str:id>/', views.show_json_by_id_product, name='show_json_by_id_product'),
    path('create-product-flutter/', views.create_product_flutter, name='create_product_flutter'),
    path('create-store-flutter/', views.create_store_flutter, name='create_store_flutter'),
    path('update-store/<uuid:pk>/', views.update_store_flutter, name='update-store'),
    path('update-product-flutter/<uuid:product_id>/', views.update_product_flutter, name='update-product'),
    path('delete-store/<uuid:store_id>/', views.delete_store_flutter, name='delete-store'),
    path('delete-product/<uuid:product_id>/', views.delete_product_flutter, name='delete-product'),

]