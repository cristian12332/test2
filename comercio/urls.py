from django.urls import path
from . import views
from .views import (
    agregar_oferta_al_carrito,
    cambiar_usuario_y_contrasena,
    descargar_excel,
    dia_especial_create,
    dia_especial_delete,
    dia_especial_list,
    encuesta,
    historial_pedidos,
    listado_compras,
    oferta_create,
    oferta_delete,
    oferta_list,
    oferta_update,
    oferta_venta,
    plato_list,
    plato_create,
    plato_ocultar,
    plato_update,
    plato_delete,
    pagina_venta,
    comprar_plato,
    editar_encuesta,
    visualizacion_encuestas,
    procesar_compra,
)

urlpatterns = [
    path('iniciar_sesion/', views.iniciar_sesion, name='iniciar_sesion'),
    path('plato_list/', plato_list, name='plato_list'),  # Ruta principal para listar platos
    path('nuevo/', plato_create, name='plato_create'),  # Ruta para crear un nuevo plato
    path('editar/<int:pk>/', plato_update, name='plato_update'),  # Ruta para editar un plato
    path('eliminar/<int:pk>/', plato_delete, name='plato_delete'),  # Ruta para eliminar un plato
    path('', pagina_venta, name='pagina_venta'),  # Ruta para la página de venta
    path('comprar/<int:plato_id>/', comprar_plato, name='comprar_plato'),  # Ruta para comprar un plato
    path('plato/listar/', plato_list, name='plato_list'),  # Ruta adicional para listar platos
    path('encuesta/', encuesta, name='encuesta'),
    path('editar_encuesta/<int:encuesta_id>/', editar_encuesta, name='editar_encuesta'),  # Ruta para editar encuestas
    path('visualizar-encuestas/', visualizacion_encuestas, name='visualizar_encuestas'),
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('limpiar_carrito/', views.limpiar_carrito, name='limpiar_carrito'),
    path('platos/<str:categoria>/', views.platos_por_categoria, name='platos_por_categoria'),
    path('procesar_compra/', procesar_compra, name='procesar_compra'),
    path('detalle_compra/<int:factura_id>/', views.detalle_compra, name='detalle_compra'),
    path('listado_compras/', listado_compras, name='listado_compras'),
    path('descargar_excel/', descargar_excel, name='descargar_excel'), 
    path('plato/ocultar/<int:pk>/', plato_ocultar, name='plato_ocultar'),
    path('cambiar-usuario-y-contrasena/', cambiar_usuario_y_contrasena, name='cambiar_usuario_y_contrasena'),
    path('historial_pedidos/', historial_pedidos, name='historial_pedidos'),
    path('dias-especiales/', dia_especial_list, name='dia_especial_list'),
    path('dias-especiales/nuevo/', dia_especial_create, name='dia_especial_create'),
    path('dias-especiales/eliminar/<int:pk>/', dia_especial_delete, name='dia_especial_delete'),
    path('ofertas/', oferta_list, name='oferta_list'),
    path('ofertas/nueva/', oferta_create, name='oferta_create'),
    path('ofertas/editar/<int:pk>/', oferta_update, name='oferta_update'),
    path('ofertas/eliminar/<int:pk>/', oferta_delete, name='oferta_delete'),
    path('ofertas_venta/', oferta_venta, name='oferta_venta'),
    path('ofertas/agregar/<int:oferta_id>/', agregar_oferta_al_carrito, name='agregar_oferta_al_carrito'),
]