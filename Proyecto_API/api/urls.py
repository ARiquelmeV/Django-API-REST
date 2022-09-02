## Archivo creado, guardara las urls que se creen en la aplicacion api

from django.urls import path

# Se importa la vista
from .views import ProductoView, home, GestiondeProductos, EliminarProducto, EditarProducto, RegistrarProducto

urlpatterns = [
    path('productos/', ProductoView.as_view(), name='productos_list'),
    path('productos/<int:id>', ProductoView.as_view(), name='productos_process'),
    path('', home),
    path('registrarproducto/', RegistrarProducto),
    path('gestion/', GestiondeProductos),
    path('gestion/eliminarproducto/<int:id>', EliminarProducto),
    path('gestion/editarproducto/<int:id>', EditarProducto),
]