from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.db import IntegrityError
from .models import DetalleFactura, DiaEspecial, Oferta, Plato, Encuesta, Factura
from .forms import CustomUserChangeForm, OfertaForm, PlatoForm, EncuestaForm,CustomUserCreationForm, PagoForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required ,user_passes_test
from django.core.exceptions import PermissionDenied
from comercio.carrito import Carrito
import pandas as pd
from datetime import timedelta
from django.utils import timezone
# Creamos verificacion de usuario admin
def es_administrador(user):
    return user.is_staff
    
@login_required
def index(request):
    return render(request, 'index.html')

def registro(request):
    if request.method == 'GET':
        return render(request, 'registro.html', {
            'form': CustomUserCreationForm()  # Usamos el formulario con email
        })
    
    else:
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                login(request, user)
                return redirect('pagina_venta')  # Redirige a la página de inicio u otra ruta
            except IntegrityError:
                return render(request, 'registro.html', {
                    'form': CustomUserCreationForm(),
                    "error": 'El usuario ya existe'
                })
        else:
            return render(request, 'registro.html', {
                'form': CustomUserCreationForm(),
                "error": 'por favor vuelva a ingresar los datos de manera correcta'
            })

    
    
@login_required
def iniciada(request):
    return render(request, 'iniciada.html')


def logout_view(request):
    logout(request)
    return redirect(request.GET.get('next', '/'))


def iniciar_sesion(request):
    if request.method == 'GET':
            return render(request, 'iniciar.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])  

        if user is None:
          return render(request, 'iniciar.html', {
                'form': AuthenticationForm,
                'error': 'usuario o contraseña es incorrecto'
            })
        else:
            login(request, user)
            if user.is_superuser:
                return redirect('iniciada')
            else:
                return redirect('pagina_venta')
        
def lista_de_platos(request):
    platos = Plato.objects.filter(oculto=False)
    return render(request, 'comercio/lista_de_platos.html', {'platos': platos})

# vventas de platos.py

def pagina_venta(request):
    platos = Plato.objects.filter(oculto=False)  # Obtener todos los platos
    carrito = Carrito(request)  # Obtener el carrito
    total_carrito = 0
    for item in carrito:
        if 'total' in item:
            total_carrito += item['total']

    if request.method == 'POST':
        form = EncuestaForm(request.POST)
        if form.is_valid():
            encuesta = form.save(commit=False)
            encuesta.plato = Plato.objects.get(id=request.POST['plato_id'])  # Asocia la encuesta con el plato
            encuesta.save()
            messages.success(request, 'Gracias por tu encuesta!')
            return redirect('pagina_venta')  # Redirige a la misma página
    else:
        form = EncuestaForm()

    return render(request, 'comercio/pagina_venta.html', {'platos': platos, 'form': form, 'carrito': carrito, 'total_carrito': total_carrito})

def encuesta(request):
    platos = Plato.objects.filter(oculto=False)
    if request.method == 'POST':
        form = EncuestaForm(request.POST)
        if form.is_valid():
            encuesta = form.save(commit=False)
            encuesta.plato = Plato.objects.get(id=request.POST['plato_id'])  # Asocia la encuesta con el plato
            encuesta.save()
            messages.success(request, 'Gracias por tu encuesta!')
            return redirect('encuesta')  # Redirige a la misma página
    else:
        form = EncuestaForm()
    return render(request, 'encuestas.html',{'platos': platos, 'form': form,})


def editar_encuesta(request, encuesta_id):
    encuesta = get_object_or_404(Encuesta, id=encuesta_id)
    
    if request.method == "POST":
        form = EncuestaForm(request.POST, instance=encuesta)
        if form.is_valid():
            form.save()
            messages.success(request, 'Encuesta actualizada con éxito.')
            return redirect('pagina_venta')  # Redirige a la página de venta o donde prefieras
    else:
        form = EncuestaForm(instance=encuesta)

    return render(request, 'comercio/encuesta_form.html', {'form': form})

def visualizacion_encuestas(request):
    platos = Plato.objects.filter(oculto=False)
    resultados = []

    for plato in platos:
        encuestas = plato.encuestas.all()  # Obtiene todas las encuestas relacionadas
        if encuestas.exists():
            total_rating = sum(encuesta.rating for encuesta in encuestas)  # Suma las calificaciones
            cantidad_encuestas = encuestas.count()  # Cuenta el número de encuestas
            promedio_rating = total_rating / cantidad_encuestas  # Calcula el promedio
        else:
            total_rating = 0
            promedio_rating = 0
            cantidad_encuestas = 0

        resultados.append({
            'plato': plato,
            'total_rating': total_rating,
            'promedio_rating': promedio_rating,
            'cantidad_encuestas': cantidad_encuestas,
        })

    # Ordenar los resultados por promedio de calificación
    resultados.sort(key=lambda x: x['promedio_rating'], reverse=True)

    return render(request, 'visualizacion_encuestas.html', {'resultados': resultados})

def comprar_plato(request, plato_id):
    plato = get_object_or_404(Plato, id=plato_id)
    carrito = Carrito(request)
    carrito.agregar(plato)
    messages.success(request, f'Has añadido {plato.nombre} al carrito.')
    return redirect('pagina_venta')
#fin de la venta de los platos

@login_required
@permission_required('is_superuser')
def plato_list(request):
    if request.user.is_staff:
        platos = Plato.objects.filter(oculto=False)
        return render(request, 'comercio/plato_list.html', {'platos': platos})
    return redirect('comercio/index')  # Redirigir si no es administrador

# CREAR PLATO:
@user_passes_test(es_administrador)
@login_required
def plato_create(request):
    if request.user.is_staff:
        if request.method == "POST":
            form = PlatoForm(request.POST, request.FILES)  # Asegúrate de incluir request.FILES
            if form.is_valid():
                form.save()
                return redirect('plato_list')
        else:
            form = PlatoForm()
        return render(request, 'comercio/plato_form.html', {'form': form})
    return redirect('index')  # Redirigir si no es administrador
#editar

@login_required
@permission_required('is_superuser')
def plato_update(request, pk):
    plato = get_object_or_404(Plato, pk=pk)
    if request.method == "POST":
        form = PlatoForm(request.POST, instance=plato)
        if form.is_valid():
            form.save()
            return redirect('plato_list')
    else:
        form = PlatoForm(instance=plato)
    return render(request, 'comercio/plato_form.html', {'form': form})
#editar fint

# Borrar plato
@login_required
@permission_required('is_superuser')
def plato_delete(request, pk):
    plato = get_object_or_404(Plato, pk=pk)
    if request.method == "POST":
        plato.delete()
        return redirect('plato_list')
    return render(request, 'comercio/plato_confirm_delete.html', {'plato': plato})

def ver_carrito(request):
    carrito = Carrito(request)
    total_carrito = 0
    for item in carrito:
        if 'total' in item:
            total_carrito += item['total']
    return render(request, 'comercio/ver_carrito.html', {
        'carrito': carrito,
        'total_carrito': total_carrito  # Pasamos el total al contexto
    })

def limpiar_carrito(request):
    carrito = Carrito(request)
    carrito.limpiar()
    return redirect('pagina_venta')

def platos_por_categoria(request, categoria):
    platos = Plato.objects.filter(categoria=categoria, oculto=False)
    carrito = Carrito(request)
    total_carrito = sum(item['total'] for item in carrito if 'total' in item)

    return render(request, 'comercio/pagina_venta.html',{
        'platos': platos,
        'carrito': carrito,
        'total_carrito': total_carrito,
        'categoria': categoria,

    })
@login_required
@login_required
def procesar_compra(request):
    carrito = Carrito(request)
    total_carrito = carrito.obtener_total()  # Ahora puedes llamar a este método

    if total_carrito == 0:
        messages.error(request, 'Debes añadir al menos un producto al carrito antes de proceder al pago.')
        return redirect('pagina_venta')
    
    if request.method == 'POST':
        form = PagoForm(request.POST)
        if form.is_valid():
            # Crear la factura usando el nombre del formulario y asignar el usuario autenticado
            factura = Factura.objects.create(
                usuario=request.user,  # Asignar el usuario autenticado
                nombre=form.cleaned_data['nombre'],  # Usar el nombre ingresado
                direccion=form.cleaned_data['direccion'],
                total=total_carrito,
                metodo_pago=form.cleaned_data['metodo_pago']
            )

            # Guardar los detalles de la factura
            for item in carrito:
                plato = item['plato']  # Obtén el objeto Plato directamente
                cantidad = item['cantidad']
                DetalleFactura.objects.create(factura=factura, plato=plato, cantidad=cantidad)

            # Limpiar el carrito después de la compra
            carrito.limpiar()

            messages.success(request, 'Compra realizada con éxito!')
            return redirect('detalle_compra', factura_id=factura.id)  # Redirige a la página de detalle de compra
    else:
        form = PagoForm()

    return render(request, 'comercio/procesar_compra.html', {'form': form, 'total_carrito': total_carrito})

@login_required
def detalle_compra(request, factura_id):
    factura = get_object_or_404(Factura, id=factura_id, usuario=request.user)
    detalles = factura.detalles.all()  # Obtiene los detalles de la factura
    return render(request, 'comercio/detalle_compra.html', {'factura': factura, 'detalles': detalles})
            
@login_required
@user_passes_test(es_administrador)
def listado_compras(request):
    # Obtiene la fecha actual
    fecha_actual = timezone.now()
    # Calcula la fecha de hace 7 días
    fecha_inicio = fecha_actual - timedelta(days=7)

    # Obtiene las fechas del formulario si están presentes
    fecha_inicio_param = request.GET.get('fecha_inicio')
    fecha_fin_param = request.GET.get('fecha_fin')

    # Filtra las facturas en el rango de fechas
    if fecha_inicio_param and fecha_fin_param:
        facturas = Factura.objects.filter(fecha__range=(fecha_inicio_param, fecha_fin_param)).prefetch_related('detalles')
    else:
        facturas = Factura.objects.filter(fecha__range=(fecha_inicio, fecha_actual)).prefetch_related('detalles')

    return render(request, 'comercio/listado_compras.html', {'facturas': facturas})

@login_required
@user_passes_test(es_administrador)
def descargar_excel(request):
    # Obtiene todas las facturas de todos los usuarios
    facturas = Factura.objects.prefetch_related('detalles').all()

    # Crea una lista para almacenar los datos
    data = []
    
    # Recorre las facturas y agrega los datos a la lista
    for factura in facturas:
        detalles = "; ".join([f"{detalle.cantidad} x {detalle.plato.nombre}" for detalle in factura.detalles.all()])
        data.append({
            "Factura ID": factura.id,
            "Fecha": factura.fecha.replace(tzinfo=None),  # Convertir a timezone-unaware
            "Usuario": factura.usuario.username,
            "Nombre": factura.nombre,
            "Método de Pago": factura.metodo_pago,
            "Detalles del Pedido": detalles,
            "Total": factura.total,
        })

    # Crea un DataFrame de pandas
    df = pd.DataFrame(data)

    # Crea una respuesta HTTP con el archivo Excel
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="compras.xlsx"'

    # Escribe el DataFrame en el archivo Excel
    df.to_excel(response, index=False)

    return response

@login_required
@permission_required('is_superuser')
def plato_ocultar(request, pk):
    plato = get_object_or_404(Plato, pk=pk)
    plato.oculto = not plato.oculto  # Cambia el estado de oculto
    plato.save()
    return redirect('plato_list')

@login_required
def cambiar_usuario_y_contrasena(request):
    if request.method == 'POST':
        user_form = CustomUserChangeForm(request.POST, instance=request.user)
        new_password = request.POST.get('new_password')  # Obtén la nueva contraseña del formulario

        # Validar que la nueva contraseña no sea igual a la anterior
        if new_password and request.user.check_password(new_password):
            messages.error(request, 'La nueva contraseña no puede ser la misma que la anterior.')
            return redirect('cambiar_usuario_y_contrasena')

        if user_form.is_valid():
            user_form.save()
            if new_password:  # Solo cambia la contraseña si se proporciona una nueva
                request.user.set_password(new_password)
                request.user.save()
                update_session_auth_hash(request, request.user)  # Mantiene la sesión activa
                messages.success(request, 'Tu nombre de usuario y contraseña han sido actualizados con éxito.')
            return redirect('pagina_venta')  # Redirige a donde desees
    else:
        user_form = CustomUserChangeForm(instance=request.user)

    return render(request, 'cambiar_usuario_y_contrasena.html', {
        'user_form': user_form,
    })

@login_required
def historial_pedidos(request):
    # Obtiene todas las facturas del usuario autenticado
    facturas = Factura.objects.filter(usuario=request.user).prefetch_related('detalles')

    return render(request, 'comercio/historial_pedidos.html', {'facturas': facturas})

@login_required
@permission_required('is_superuser')
def oferta_list(request):
    ofertas = Oferta.objects.all()
    return render(request, 'comercio/oferta_list.html', {'ofertas': ofertas})

@login_required
@permission_required('is_superuser')
def oferta_create(request):
    if request.method == "POST":
        form = OfertaForm(request.POST)
        if form.is_valid():
            oferta = form.save()
            messages.success(request, 'Oferta creada con éxito.')
            return redirect('oferta_list')
    else:
        form = OfertaForm()
    return render(request, 'comercio/oferta_form.html', {'form': form})

@login_required
@permission_required('is_superuser')
def oferta_update(request, pk):
    oferta = get_object_or_404(Oferta, pk=pk)
    if request.method == "POST":
        form = OfertaForm(request.POST, instance=oferta)
        if form.is_valid():
            form.save()
            messages.success(request, 'Oferta actualizada con éxito.')
            return redirect('oferta_list')
    else:
        form = OfertaForm(instance=oferta)
    return render(request, 'comercio/oferta_form.html', {'form': form})

@login_required
@permission_required('is_superuser')
def oferta_delete(request, pk):
    oferta = get_object_or_404(Oferta, pk=pk)
    if request.method == "POST":
        oferta.delete()
        messages.success(request, 'Oferta eliminada con éxito.')
        return redirect('oferta_list')
    return render(request, 'comercio/oferta_confirm_delete.html', {'oferta': oferta})

@login_required
@permission_required('is_superuser')
def dia_especial_list(request):
    dias_especiales = DiaEspecial.objects.all()
    return render(request, 'comercio/dia_especial_list.html', {'dias_especiales': dias_especiales})

@login_required
@permission_required('is_superuser')
def dia_especial_create(request):
    if request.method == "POST":
        nombre = request.POST.get('nombre')
        fecha = request.POST.get('fecha')
        DiaEspecial.objects.create(nombre=nombre, fecha=fecha)
        messages.success(request, 'Día especial creado con éxito.')
        return redirect('dia_especial_list')
    return render(request, 'comercio/dia_especial_form.html')

@login_required
@permission_required('is_superuser')
def dia_especial_delete(request, pk):
    dia_especial = get_object_or_404(DiaEspecial, pk=pk)
    if request.method == "POST":
        dia_especial.delete()
        messages.success(request, 'Día especial eliminado con éxito.')
        return redirect('dia_especial_list')
    return render(request, 'comercio/dia_especial_confirm_delete.html', {'dia_especial': dia_especial})

@login_required
def oferta_venta(request):
    # Obtener ofertas válidas para hoy
    hoy = timezone.now().date()
    ofertas_hoy = Oferta.objects.filter(dias_especiales__fecha=hoy).distinct()

    return render(request, 'comercio/oferta_venta.html', {
        'ofertas_hoy': ofertas_hoy  # Pasamos las ofertas del día al contexto
    })

@login_required
def agregar_oferta_al_carrito(request, oferta_id):
    oferta = get_object_or_404(Oferta, id=oferta_id)
    carrito = Carrito(request)

    # Agregar cada plato de la oferta al carrito
    for plato in oferta.platos.all():
        carrito.agregar(plato)  # Usa el método agregar de la clase Carrito

    messages.success(request, f'Has añadido la oferta "{oferta.nombre}" al carrito.')
    return redirect('oferta_venta') 