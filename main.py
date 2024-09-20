from reportlab.pdfgen import canvas
from body import Body

"""
TODO
    ***El xml no debe ir en el super de clase en clase
"""

class XmlPdf:
    
    def __init__(self, xml_obj):
        self.body = Body(xml_obj)
        
    def main(self, filenamexml, filenametxt):
        c = canvas.Canvas("test.pdf")
        self.body.GetLayout(filenamexml, c, filenametxt)
        c.save()

#xml_obj = 'archivos_de_prueba/FP204233-copia.xml'
xml_obj = 'archivos_de_prueba/FP204233.xml'
in_txt = 'archivos_de_prueba/FP204233.txt'

pdf = XmlPdf(xml_obj)
pdf.main(xml_obj, in_txt)
