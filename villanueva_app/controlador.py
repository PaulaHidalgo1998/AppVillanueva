from django.http import HttpResponse
from django.shortcuts import render
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from tabulate import tabulate
from mi_app.models import Persona

class Controlador:
    def home(self, request):
        personas_agregadas = self.obtener_personas()
        total_dinero = self.calcular_total_dinero()
        context = {}
        context.update({'personas': personas_agregadas})
        context.update({'total_dinero': total_dinero})
        print('Hola Adri <3')
        return render(request, 'home.html', context)

    def guardar_persona(self, request):
        # Lógica para guardar la persona en la base de datos
        nombre = request.POST['nombre']
        apellidos = request.POST['apellidos']
        dinero_aportado = float(request.POST['dineros'])

        total_personas = Persona.objects.filter().count()
        
        persona = Persona(nombre=nombre, apellidos=apellidos, dinero=dinero_aportado)
        persona.save()
        if dinero_aportado == 40:
            persona.tipo_aportacion = 'adulto'
        elif dinero_aportado == 25:
            persona.tipo_aportacion = 'jubilado'
        elif dinero_aportado == 15:
            persona.tipo_aportacion = 'joven'
        else:
            persona.tipo_aportacion = 'otro'
        
        persona.numero_socio = total_personas + 1
        persona.save()
        print('PERSONA GUARDADA')

        return True

    def borrar_persona(self, request):
        id_persona = request.POST['idPersona']
        persona = Persona.objects.get(pk=id_persona)
        persona.delete()

        return True

    def borrar_todo(self, request):
        Persona.objects.filter().delete()

    def calcular_total_dinero(self):
        personas = Persona.objects.filter()
        total_dinero = personas.filter(tipo_aportacion='joven').count() * 15 + personas.filter(tipo_aportacion='jubilado').count() * 25 + personas.filter(tipo_aportacion='adulto').count() * 40
        otras_personas = personas.filter(tipo_aportacion='otro')
        for otra in otras_personas:
            total_dinero += otra.dinero

        return total_dinero

    def obtener_personas(self):
        return Persona.objects.filter().order_by('apellidos', 'tipo_aportacion')

    # def exportar_pdf(self):
    #     return ''

    def generar_pdf_personas_tabla(self, request):
        doc = SimpleDocTemplate("personas_cuotas_2023.pdf", pagesize=letter)
        elements = []

        # Cabecera de la tabla
        data = [["Número de Socio", "Apellidos", "Nombre", "Tipo de Aportación", "Dinero Aportado"]]

        personas = self.obtener_personas()

        # Llenar la tabla con los datos de las personas
        for persona in personas:
            data.append([
                str(persona.numero_socio),
                persona.apellidos,
                persona.nombre,
                persona.tipo_aportacion,
                str(persona.dinero),
            ])

        # Establecer el estilo de la tabla
        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ])

        # Crear la tabla y aplicar el estilo
        table = Table(data)
        table.setStyle(style)

        # Agregar la tabla al documento
        elements.append(table)

        # Construir el PDF
        doc.build(elements)
        print('PDF CREADO')

    def generar_pdf_personas_listado(self):
        doc = SimpleDocTemplate("personas_cuotas_2023.pdf", pagesize=letter)
        elements = []

        # Estilo de los párrafos
        styles = getSampleStyleSheet()
        style_normal = styles["Normal"]
        style_titulo = styles["Heading1"]

        # Título del listado
        titulo = Paragraph("Listado de Personas", style_titulo)
        elements.append(titulo)

        # Agregar un salto de línea
        elements.append(Spacer(1, 12))

        # Listado de personas
        # for persona in personas:
        #     # Formatear los datos de la persona en un párrafo
        #     datos_persona = "Número de Socio: {}<br/>Apellidos: {}<br/>Nombre: {}<br/>Tipo de Aportación: {}<br/>Dinero Aportado: {}".format(
        #         persona.numero_socio,
        #         persona.apellidos,
        #         persona.nombre,
        #         persona.tipo_aportacion,
        #         persona.dinero_aportado
        #     )
        #     paragraph = Paragraph(datos_persona, style_normal)
        #     elements.append(paragraph)

        #     # Agregar un espacio entre cada persona
        #     elements.append(Spacer(1, 12))

        datos = [
            [1, "Hidalgo", "Paula", "Joven", 40],
            [2, "Gómez", "Carlos", "Adulto", 50],
            [3, "Martínez", "Ana", "Joven", 30],
            [4, "López", "Juan", "Jubilado", 25],
        ]

        # Formatear los datos de la persona en un párrafo
        headers = ["Número de Socio", "Apellidos", "Nombre", "Tipo de Aportación", "Dinero Aportado"]
        tabulated_data = tabulate(datos, headers, tablefmt="plain")
        # Crear los estilos para el contenido
        styles = getSampleStyleSheet()
        style_normal = styles["Normal"]
        style_normal.alignment = 0

        for line in tabulated_data.split("\n"):
            elements.append(Paragraph(line, style_normal))
            elements.append(Spacer(1, 12))


        persona_fila = f"{'3'}\t{'Hidalgo Rodriguez'}\t{'Beatriz'}\t{'Adulto'}\t{'40'}"
        elements.append(Paragraph(persona_fila, styles["Normal"]))     

        # Agregar un espacio entre cada persona
        elements.append(Spacer(1, 12))
        c = canvas.Canvas("reporte.pdf", pagesize=letter)
        c.setFont("Helvetica", 12)

        for dato in datos:
            texto = f"{dato[0]}\t{dato[1]}\t{dato[2]}\t{dato[3]}\t{dato[4]}"
            c.drawString(72, 800, texto)
            c.showPage()

        # Construir el PDF
        doc.build(elements)

        print('PDF LISTO')