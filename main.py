from reportlab.pdfgen import canvas
from body import Body

folio = 'FP201203'
carpeta = '46'

class XmlPdf:
    
    def __init__(self, xml_obj, filenametxt):
        self.body = Body(xml_obj, filenametxt)
        
    def main(self, filenamexml, filenametxt):
        c = canvas.Canvas("C:/Users/Usuario1/Desktop/Requerimentos/JPrieto/xml_to_pdf_dcruz/tipos_factura/" + carpeta + "/test_" + folio + ".pdf")
        self.body.GetLayout(filenamexml, c, filenametxt)
        c.save()

xml_obj = 'C:/Users/Usuario1/Desktop/Requerimentos/JPrieto/xml_to_pdf_dcruz/tipos_factura/' + carpeta + '/' + folio + '.xml'
in_txt = 'C:/Users/Usuario1/Desktop/Requerimentos/JPrieto/xml_to_pdf_dcruz/pruebas/TXTs/' + folio + '.txt'

pdf = XmlPdf(xml_obj, in_txt)
pdf.main(xml_obj, in_txt)
