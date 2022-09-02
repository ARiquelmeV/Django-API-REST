from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .models import Producto
import requests
import json


# Clase que se convertira en una vista que sea capaz de procesar las respuestas
# Esto corresponde al backend de la applicacion

class ProductoView(View):

     # Se ejecutara cada vez que se envie una respuesta, para poder realizar peticiones de post | alternativa la csrf token
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    # Listar producto/s
    def get(self, request ,id=0):
        
        # Filtrar si se requiere mostrar solo un producto
        if (id > 0):
            # lista de productos, para saber si existen productos
            productos= list(Producto.objects.filter(id=id).values())
            # Si la lista no es vacia, se muestra la totalidad de los productos
            if len(productos) > 0:
                producto = productos[0]
                datos={'message': "Success", 'productos':producto}
            else:
                datos={'message': "Productos no encontrados..."}

            return JsonResponse(datos)  
        else:        
            # Se ocupa .values y se castea a lista, ya que al retornar .all(tipo queryset) como JsonResponse, da error
            productos = list(Producto.objects.values())
            if len(productos)>0:
                datos={'message': "Success", 'productos':productos}

            else:
                datos={'message': "Productos no encontrados..."}

            return JsonResponse(datos)        

    # Agregar productos
    def post(self, request):
        # Variable jd (jason data) que captura los datos (en un diccionario) para poder insertarlos en la base de datos
        jd = json.loads(request.body)
        Producto.objects.create(
            nombre=jd['nombre'],
            precio=jd['precio'],
            stock=jd['stock'],
            medidas=jd['medidas'],
            colores=jd['colores'],
            foto=jd['foto'],
        )

        datos={'message': "Success"}
        return JsonResponse(datos)     

    # Seleccionar un producto para modificarlo
    def put(self, request, id):
        # Variable jd (jason data) que captura los datos (en un diccionario) para poder insertarlos en la base de datos
        jd = json.loads(request.body)
        # lista de productos, para saber si el objeto en particular existe
        productos= list(Producto.objects.filter(id=id).values())
        # Al no ser vacia la lista, se procede a acceder al producto para cambiar algun atributo
        if len(productos)> 0:
            producto = Producto.objects.get(id=id)
            producto.nombre=jd['nombre']
            producto.precio=jd['precio']
            producto.stock=jd['stock']
            producto.medidas=jd['medidas']
            producto.colores=jd['colores']
            producto.foto=jd['foto']
            producto.save()
            datos={'message': "Success"}

        else:
            datos={'message': "Productos no encontrados..."}

        return JsonResponse(datos)              
        

    # Seleccionar un elemento para borrarlo
    def delete(self, request ,id):
        productos= list(Producto.objects.filter(id=id).values())
        if len(productos)> 0:
            Producto.objects.filter(id=id).delete()
            datos={'message': "Success"}
        else:
            datos={'message': "Productos no encontrados..."}

        return JsonResponse(datos)              
        
## Esto sera el front de la aplicacion

# Vista de inicio, donde se puede obtener los datos
def home(request):

    # Se deben obtener los datos de la API con el metodo request
    url = 'http://127.0.0.1:8000/api/productos/'
    
    # Luego convertimos la request en un objeto json
    productos = requests.get(url).json()

    # Y con render, mandamos el objeto jason al html que corresponda
    return render(request, "Catalogo.html", {'productos': productos})

# Tambien en la pagina de inicio sera posible registrar un producto, esto sera a traves del ORM de Django mas que con los metodos de API
def RegistrarProducto(request):
    nombre= str(request.POST['pnombre'])
    precio= int(request.POST['pprecio'])
    stock= int(request.POST['pstock'])
    colores= str(request.POST['pcolores'])
    medidas= str(request.POST['pmedidas'])
    foto= str(request.POST['pfoto'])
    Producto.objects.create( nombre=nombre, precio=precio, stock = stock, colores = colores, 
    medidas = medidas, foto = foto)
    return redirect('http://127.0.0.1:8000/api/')       

# Vista gestion de productos, para esta vista, capturamos el tipo de dato id para poder obtener el producto con el metodo request
# Gracias a esto, sabemos cual es el producto que se desea editar/eliminar
#  
def GestiondeProductos(request):
    # Se captura este elemento cuando se pide seleccionar el id del producto con el metodo POST
    id = request.POST['numProducto']

    # Luego se obtienen los datos del producto
    url = 'http://127.0.0.1:8000/api/productos/'+id

    # Y se convierten en un tipo de dato json para mandarlo al hmtl gestiondeproductos
    productos = requests.get(url).json()
    return render(request, "Gestiondeproductos.html", {'productos': productos})

# Se encuentra en la lista gestion de productos, necesita el id del producto a eliminar
def EliminarProducto(request, id):
    producto = list(Producto.objects.filter(id=id).values())
    # Pregunta si existe el elemento
    if len(producto)> 0:
        # Y lo borra de la base de datos
        Producto.objects.filter(id=id).delete()
        return redirect('http://127.0.0.1:8000/api/')
    else:
        return redirect('http://127.0.0.1:8000/api/')

# Se encuentra en la lista gestion de productos, el id ya lo sabemos cuando estamos en esta vista, por lo usamos directamente.
def EditarProducto(request, id):
    producto = Producto.objects.get(id=id)
    #print(id)
    #print(request.POST['pnombre'])
    # Con el metodo POST obtenemos lo que el usuario cambie en los input, y guardamos en la base de datos.
    producto.nombre= str(request.POST['pnombre'])
    #print(request.POST['pprecio'])
    producto.precio= int(request.POST['pprecio'])
    #print(request.POST['pstock'])
    producto.stock= int(request.POST['pstock'])
    producto.save()
    return redirect('http://127.0.0.1:8000/api/')

