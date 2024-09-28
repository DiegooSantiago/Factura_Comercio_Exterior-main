from reportlab.pdfgen import canvas
from body import Body

"""
TODO
    ***El xml no debe ir en el super de clase en clase
"""

class XmlPdf:
    
    def __init__(self, xml_obj, filenametxt):
        self.body = Body(xml_obj, filenametxt)
        
    def main(self, filenamexml, filenametxt):
        c = canvas.Canvas("test_FP207932.pdf")
        self.body.GetLayout(filenamexml, c, filenametxt)
        c.save()

xml_obj = 'C:/Users/Usuario1/Desktop/Requerimentos/JPrieto/xml_to_pdf_dcruz/pruebas/CFDI_Rel_e_Inf_Global/FP207932.xml'
in_txt = 'C:/Users/Usuario1/Desktop/Requerimentos/JPrieto/xml_to_pdf_dcruz/pruebas/CFDI_Rel_e_Inf_Global/FP207932.txt'

pdf = XmlPdf(xml_obj, in_txt)
pdf.main(xml_obj, in_txt)
