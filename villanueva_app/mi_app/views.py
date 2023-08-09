from django.http import HttpResponse
from django.shortcuts import render

from controlador import Controlador

# Create your views here.

def home(request):
    controlador = Controlador()
    return controlador.home(request)

def crearPersona(request):
    controlador = Controlador()
    response = controlador.guardar_persona(request)
    return HttpResponse(response, content_type='application/json')

def borrarPersona(request):
    controlador = Controlador()
    response = controlador.borrar_persona(request)
    return HttpResponse(response, content_type='application/json')

def borrarTodo(request):
    controlador = Controlador()
    response = controlador.borrar_todo(request)
    return HttpResponse(response, content_type='application/json')

def crearPDF(request):
    controlador = Controlador()
    # response = controlador.generar_pdf_personas_tabla(request)
    response = controlador.generar_pdf_personas_listado(request)
    return HttpResponse(response, content_type='application/json')