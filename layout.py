from reportlab.pdfgen import canvas
from reportlab.lib.colors import *
from abc import abstractmethod
from reportlab_qrcode import QRCodeImage
from reportlab.lib.units import mm
from xmlReader import XMLData
from txtReader import TxtData
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import locale



class Strings(XMLData):
    def __init__(self, xml_obj, txt_file):
        super().__init__()
        self.xml_data = self.GetData(xml_obj)
        self.txt = TxtData()
        self.txt_emisor_data = self.txt.GetEmisorData(txt_file)
        self.txt_receptor_data = self.txt.GetReceptorData(txt_file)
        self.txt_empresa_data = self.txt.GetEmpresaData(txt_file)
        self.txt_datosfa_data = self.txt.GetDatosfaData(txt_file)
        self.txt_datostot_data = self.txt.GetTotalesData(txt_file)
        self.txt_datoscom_data = self.txt.GetComprobanteData(txt_file)
        self.txt_detalle_data =  self.txt.GetDetalleData(txt_file)

        fuente_path = "fonts/Courier.ttf"
        self.fuente_nombre = "Times-New"
        pdfmetrics.registerFont(TTFont(self.fuente_nombre, fuente_path))
        fuente_path = "fonts/Courier-Bold.ttf"
        self.fuente_nombre = "Times-New-Bold"
        # Configurar la fuente
        pdfmetrics.registerFont(TTFont(self.fuente_nombre, fuente_path))

class Layout(Strings):
    def __init__(self, xml_obj, txt_file):
        super().__init__(xml_obj, txt_file)

    @classmethod
    def SetStaticLabels(cls, c):

        #Labels Segundo cuadro
        c.setFont('Times-New-Bold', 7)
        c.drawString(361, 753, 'TRANSPORTE ')
        c.drawString(361, 740, 'PEDIDO ')
        c.drawString(467, 740, 'No. De GUIA ')
        c.drawString(361, 727, 'O.E. ')
        c.drawString(467, 727, 'No. De SALIDA ')
        c.drawString(361, 714, 'CONDICIONES DE PAGO ')
        c.drawString(516, 714, 'LISTA  ')
        c.drawString(361, 701, 'AGTE:')
        c.drawString(361, 688, 'ORDEN DE COMPRA ')
        c.drawString(361, 673, 'cfdis Relacionados')

        #Labels Header Bancos
        c.drawString(15, 657, 'BANCO')
        c.drawString(70, 657, 'CUENTA CLABE')
        c.drawString(160, 657, 'CUENTA')
        c.drawString(235, 657, 'REFERENCIA')

    def SetStaticLabels_(self, c):

        #Cuadro a lado info bancos
        c.setFont('Times-New', 7.5)
        aux_y = 657
        c.drawString(293, aux_y, self.txt_empresa_data['ship01'])
        aux_y -= 10
        if self.txt_empresa_data['ship02'] != '':
            c.drawString(293, aux_y, self.txt_empresa_data['ship02'])
            aux_y -= 10
        c.drawString(293, aux_y, self.txt_empresa_data['ship03'])
        aux_y -= 10
        if self.txt_empresa_data['ship04'] != '':
            c.drawString(293, aux_y, self.txt_empresa_data['ship04'])
            aux_y -= 10
        c.drawString(293, aux_y, self.txt_empresa_data['ship05'])
        aux_y -= 10
        if self.txt_empresa_data['ship06'] != '':
            c.drawString(293, aux_y, self.txt_empresa_data['ship06'])
            aux_y -= 10
        if self.txt_empresa_data['ship07'] != '':
            c.drawString(293, aux_y, self.txt_empresa_data['ship07'])
            aux_y -= 10


        #Receptor, primer cuadro etiquetas no estáticas
        c.drawString(12, 752, f"{self.xml_data.receptor['Nombre']}, Domicilio Fiscal: {self.xml_data.receptor['DomicilioFiscalReceptor']}, Regimen Fiscal: {self.xml_data.receptor['RegimenFiscalReceptor']}")
        c.drawString(12, 741, f"{self.txt_receptor_data['calle']} {self.txt_receptor_data['noExterior']} {self.txt_receptor_data['noInterior']}")
        aux_y = 0
        if self.txt_receptor_data['codigoPostal'] == 'NA':
            c.drawString(12, 730, f"{self.txt_receptor_data['codigoPostal']}")
        elif self.txt_receptor_data['codigoPostal'] == '':
            aux_y = 12
        else:
            if self.txt_receptor_data['colonia'] == '':
                c.drawString(12, 730, f"{self.txt_receptor_data['CPPDF']}")
            else:
                c.drawString(12, 730, f"{self.txt_receptor_data['colonia']} {self.txt_receptor_data['CPPDF']}")
        c.drawString(12, 718+aux_y, f"{self.txt_receptor_data['localidad']}")
        if self.txt_receptor_data['municipio'] == '':
            c.drawString(12, 707+aux_y, f"{self.txt_receptor_data['estado']}, {self.txt_receptor_data['pais']}")
        else:
            c.drawString(12, 707+aux_y, f"{self.txt_receptor_data['municipio']} {self.txt_receptor_data['estado']}, {self.txt_receptor_data['pais']}")
        c.drawString(12, 696+aux_y, f"{self.txt_receptor_data['idFiscal']}")
        c.drawString(12, 685+aux_y, f"{self.txt_receptor_data['telefono']}")


        #Labels No estáticos del segundo cuadro DATOS EMPRESA
        c.setFont('Times-New', 7)

        c.drawString(415, 753, self.txt_empresa_data['trans1'])
        c.drawString(395, 740, self.txt_empresa_data['numped'])
        c.drawString(515, 740, self.txt_empresa_data['numGuia'])
        c.drawString(380, 727, self.txt_empresa_data['ordEnt'])
        c.drawString(525, 727, self.txt_empresa_data['ordSal'])
        c.drawString(450, 714, self.xml_data.atributos['CondicionesDePago'])
        c.drawString(540, 714, self.txt_empresa_data['lisPrec'])
        c.drawString(390, 701, self.txt_empresa_data['nomAge1'])
        c.drawString(435, 688, self.txt_empresa_data['ordComp'])


        #DATOS BANCOS DEL VIENEN DEL TXT
        altura_bancos = 647
        _ = self.FitText(c,15,altura_bancos,self.txt_empresa_data['extra03Banco'],14)
        c.drawString(70, altura_bancos, self.txt_empresa_data['extra03Clabe'])
        c.drawString(160, altura_bancos, self.txt_empresa_data['extra03Cuenta'])
        c.drawString(235, altura_bancos, self.txt_empresa_data['extra03Ref'])
        c.drawString(15, altura_bancos-7, f"{self.txt_empresa_data['extra04Banco']}")
        c.drawString(70, altura_bancos-7, self.txt_empresa_data['extra04Clabe'])
        c.drawString(160, altura_bancos-7, self.txt_empresa_data['extra04Cuenta'])
        c.drawString(235, altura_bancos-7, self.txt_empresa_data['extra04Ref'])
        c.drawString(15, altura_bancos-14, f"{self.txt_empresa_data['extra05Banco']}")
        c.drawString(70, altura_bancos-14, self.txt_empresa_data['extra05Clabe'])
        c.drawString(160, altura_bancos-14, self.txt_empresa_data['extra05Cuenta'])
        c.drawString(235, altura_bancos-14, self.txt_empresa_data['extra05Ref'])
        c.drawString(15, altura_bancos-21, f"{self.txt_empresa_data['extra06Banco']}")
        c.drawString(70, altura_bancos-21, self.txt_empresa_data['extra06Clabe'])
        c.drawString(160, altura_bancos-21, self.txt_empresa_data['extra06Cuenta'])
        c.drawString(235, altura_bancos-21, self.txt_empresa_data['extra06Ref'])
        c.drawString(15, altura_bancos-28, f"{self.txt_empresa_data['extra07Banco']}")
        c.drawString(70, altura_bancos-28, self.txt_empresa_data['extra07Clabe'])
        c.drawString(160, altura_bancos-28, self.txt_empresa_data['extra07Cuenta'])
        c.drawString(235, altura_bancos-28, self.txt_empresa_data['extra07Ref'])

        #Bancos etiquetas no estáticas
        c.drawString(30, 610, f"FORMA DE PAGO: {self.xml_data.atributos['FormaPago']}")
        c.drawString(15, 600, f"MONEDA: {self.xml_data.atributos['Moneda']}")
        c.drawString(90, 600, f"TIPO CAMBIO: {self.xml_data.atributos['TipoCambio']}" )
        c.drawString(166,600, f"Exportación: {self.xml_data.atributos['Exportacion']}")
        c.drawString(140, 590, f"FECHA DE VENCIMIENTO: ")
        c.setFont('Times-New-Bold', 7)
        c.drawString(229, 590, f"{self.txt_empresa_data['yearPag']}-{self.txt_empresa_data['mesPag']}-{self.txt_empresa_data['diaPag']}")

    @abstractmethod
    def GetStaticHeaderText(self, c):
        c.setFont('Times-New-Bold', 7.5)
        c.drawString(30, 830, self.xml_data.emisor['Nombre'])
        c.setFont('Times-New-Bold', 7)
        c.drawString(30, 820, f"{self.txt_emisor_data['calle']} No. {self.txt_emisor_data['noExterior']} C.P. {self.txt_emisor_data['codigoPostal']}")
        c.drawString(65, 810, f"Col. {self.txt_emisor_data['PDFcolonia']}")
        c.drawString(20, 800, f"{self.txt_emisor_data['telefono']}")
        c.drawString(40, 790, f"{self.txt_emisor_data['PDFmunicipio']}, {self.txt_emisor_data['PDFestado']}, {self.txt_emisor_data['PDFpais']}")
        c.drawString(20, 780, f"RFC: {self.xml_data.emisor['Rfc']} CURP: {self.txt_emisor_data['curp']}")
        c.setFont('Times-New-Bold', 7)

        # Header superior central
        c.drawString(210, 827, f'Este documento es una representación impresa de un "CFDI" version {self.xml_data.atributos["Version"]}')
        c.setFont('Times-New-Bold', 5)
        c.drawString(220, 815, f"METODO PAGO: {self.xml_data.atributos['MetodoPago']}, {self.txt_datosfa_data['FormaPagoPDF']} USO CFDI: {self.xml_data.receptor['UsoCFDI']}: {self.txt_datosfa_data['UsoCfdi']}")
        c.setFont('Times-New-Bold', 6)
        c.drawString(200, 809, f"REGIMEN FISCAL: {self.xml_data.emisor['RegimenFiscal']}. {self.txt_emisor_data['regimenFiscalPDF']}.")
        c.setFont('Times-New-Bold', 7)
        c.drawString(270, 795, f"TIPO DE COMPROBANTE: {self.xml_data.atributos['TipoDeComprobante']} {self.txt_datosfa_data['TipoComprobante']}")
        c.drawString(220, 785, 'FECHA DE EMISION:')
        c.setFont('Times-New', 6.5)
        c.drawString(223, 775, f"{self.xml_data.atributos['Fecha'].replace('T', ' ')}")
        c.setFont('Times-New-Bold', 7)
        c.drawString(330, 785, 'LUGAR DE EXPEDICION:')
        c.setFont('Times-New', 7)
        c.drawString(360, 775, f"{self.xml_data.atributos['LugarExpedicion']}")
    
    @abstractmethod
    def GetFolios(self, c):
        c.setFillColor(self.purple)
        c.roundRect(500, 805, 80, 30, 4, fill=True)
        c.setFillColor(white)
        c.roundRect(500, 805, 80, 15, 4, fill=True)
        c.setFillColor(white)
        c.setFont('Times-New', 7)
        c.drawString(514, 825, 'FOLIO INTERNO')
        c.setFont('Times-New', 10)
        c.setFillColor(black)
        c.drawString(521, 810, f"{self.xml_data.atributos['Serie']}{self.xml_data.atributos['Folio']}")
        c.setFillColor(self.purple)
        #
        c.roundRect(500, 765, 80, 30, 4, fill=True)
        c.setFillColor(white)
        c.setFont('Times-New', 7)
        c.drawString(516, 785, 'FOLIO FISCAL')
        c.setFillColor(white)
        c.setFont('Times-New', 5)
        c.roundRect(500, 765, 80, 15, 4, fill=True)
        c.setFillColor(black)
        c.drawString(506, 773, self.xml_data.tfd.uuid[0:26])
        c.drawString(527, 768, self.xml_data.tfd.uuid[26:36])
    
    @abstractmethod
    def GetRectangles(self, c):
        #1st Rect
        c.rect(10, 680, 350, 80)
        c.rect(360, 665, 220, 95)

        #Corresponding lines
        c.line(360, 682, 580, 682)
        c.line(360, 695, 580, 695)
        c.line(360, 709, 580, 709)
        c.line(360, 735, 580, 735)
        c.line(360, 722, 580, 722)
        c.line(360, 748, 580, 748)
        c.line(465, 748, 465, 722)
        c.line(515, 722, 515, 709)
        
        self.SetStaticLabels(c)
        self.SetStaticLabels_(c)
        
        #Second Rect
        c.rect(10, 585, 280, 80)
        c.rect(290,585,290,80)

    @abstractmethod
    def GetDetalleHeader(self, c):
        c.setFillColor(self.purple)
        c.roundRect(10, 560, 570, 25, 4, fill=True)
        c.setFillColor(white)
        c.setFont('Times-New', 6)
        c.drawString(20, 575, 'CVE')
        c.drawString(18, 565, 'ARTIC')
        c.line(45, 585, 45, 560)
        c.drawString(53, 575, 'COD SAT')
        c.line(90, 585, 90, 560)
        c.drawString(175, 575, 'DESCRIPCION')
        c.line(305, 585, 305, 560)
        c.drawString(313, 575, 'OBJ.')
        c.drawString(310, 565, 'IMPTO')
        c.line(335, 585, 335, 560)
        c.drawString(340, 575, 'BULTOS')
        c.line(370, 585, 370, 560)
        c.drawString(378, 575, 'U.M. SAT')
        c.line(410, 585, 410, 560)
        c.drawString(420, 575, 'KGS')
        c.line(440, 585, 440, 560)
        c.drawString(453, 575, 'VALOR')
        c.drawString(448, 565, 'UNITARIO')
        c.line(485, 585, 485, 560)
        c.drawString(490, 575, 'DESCUENTO')
        c.line(530, 585, 530, 560)
        c.drawString(542, 575, 'IMPORTE')

    def FitText(self, c, x, y, texto, max_chars, factor=None) -> int:
        lines = [texto[i:i + max_chars] for i in range(0, len(texto), max_chars)]
        for line in lines:
            c.drawString(x,y, line)
            if factor:
                y-=factor
            else:
                y -= 7
        return y

    def Footer(self, c, altura):

        c.setFillColor(HexColor('#e8e8e8'))
        
        #Cuadro bajo el gris con líneas verticales
        #altura + 25 para compensar el recorrido hacia arriba
        altura -= 25
        c.rect(20,altura+1,560,23)
        c.line(370,altura+1,370,altura+24)
        c.line(410,altura+1,410,altura+24)
        c.line(440,altura+1,440,altura+24)
        c.line(485,altura+1,485,altura+24)
        c.line(530,altura+1,530,altura+24)
        
        c.setFillColor(black)
        c.setFont('Times-New-Bold', 6.5)
        c.drawString(22, altura+14, 'RECIBIDA LA MERCANCIA EL CLIENTE CUENTA CON UN PLAZO MÁXIMO DE 10 DIAS PARA')
        c.drawString(22, altura+6, 'INCONFORMARSE POR ESCRITO DE LO CONTRARIO NO SE ACEPTA DEVOLUCIÓN.')
        c.setFont('Times-New', 7)
        c.drawString(337, altura+14, 'TOTAL')
        c.drawString(332, altura+6, 'GENERAL')
        c.drawRightString(407, altura+14, f"{self.txt_empresa_data['sumaBultos']}")
        c.drawRightString(482, altura+14, f"{self.txt_empresa_data['sumaKilos']}")
        locale.setlocale(locale.LC_MONETARY, 'en_US.UTF-8')
        c.drawRightString(577, altura+14, f"{locale.currency(float(self.txt_datostot_data['subtotalSinDescuentosSinIva']), grouping=True)}")
        c.drawRightString(577, altura-8, f"{locale.currency(float(self.txt_datostot_data['subTotal']), grouping=True)}")
        if self.txt_datoscom_data['descuento'] != '':
            c.drawRightString(577, altura-20, f"{locale.currency(float(self.txt_datoscom_data['descuento']), grouping=True)}")
        else:
            c.drawRightString(577, altura-20, '$')
        altura -= 10

        #Subtotal Rects
        c.drawString(22, altura+2, 'CANTIDAD CON LETRA')
        c.setFont('Times-New-Bold', 7)
        c.drawString(110, altura+2, f"{self.txt_datostot_data['cantidadConLetra']}")
        c.drawString(215, altura-7, f"{self.txt_datosfa_data['InfoTit']}")
        c.setFont('Times-New-Bold', 9)
        if self.txt_datosfa_data['InfoCta'][0:2] == 'La':
            _ = self.FitText(c, 22, altura-18,self.txt_datosfa_data['InfoCta'][0:97], 97,9)
            _ = self.FitText(c, 22, altura-28,self.txt_datosfa_data['InfoCta'][98:168], 100,9)
            c.setFont('Times-New-Bold', 8.8)
            _ = self.FitText(c, 22, altura-38,self.txt_datosfa_data['InfoCta'][169:], 110,9)
        elif self.txt_datosfa_data['InfoCta'][0:2] == 'PA':
            _ = self.FitText(c, 22, altura-18,self.txt_datosfa_data['InfoCta'][0:], 70,9)
        elif self.txt_datosfa_data['InfoCta'][0:2] == 'Th':
            _ = self.FitText(c, 22, altura-18,self.txt_datosfa_data['InfoCta'][0:90], 90,9)
            _ = self.FitText(c, 22, altura-28,self.txt_datosfa_data['InfoCta'][90:165], 75,9)
            _ = self.FitText(c, 22, altura-38,self.txt_datosfa_data['InfoCta'][166:], 100,9)
        c.setFillColor(self.purple)
        c.roundRect(20,altura,410,10,1)
        
        altura -= 15
        c.roundRect(20,altura-30,410,45,1)
        c.roundRect(430,altura+15,70,10,1,fill=True)
        c.setFillColor(white)
        c.setFont('Times-New', 7)
        c.drawString(450, altura+18, 'SUB TOTAL')
        c.setFillColor(self.purple)
        c.roundRect(430,altura-40,70,55,1,fill=True)
        c.setFillColor(white)
        c.drawString(446, altura+5, 'DESCUENTO')
        if self.txt_datostot_data['IEPS'] != '0.00':
            altura -=10
            c.drawString(455, altura+3, 'IEPS 8%')
            c.setFillColor(black)
            c.drawRightString(577, altura+3, f"{self.txt_datostot_data['txtIEPS']}")
            c.setFillColor(white)
        c.drawString(446, altura-10, 'IVA')
        c.drawString(456, altura-25, 'TOTAL')
        #cuadro blanco de iva
        c.roundRect(470,altura-13,20,10,0,fill=True, stroke=False)
        #Porcentaje de impuesto
        cadena = self.txt_datosfa_data['ResumenTax']
        inicio = cadena.find("002 Factor:Tasa Tasa o Cuota:0.")
        fin = cadena.find("Base:", inicio)
        inicio += 31
        c.setFillColor(black)
        c.drawString(473, altura-10, f"{cadena[inicio:fin].strip()}%")
        c.drawRightString(577, altura-10, f"{locale.currency(float(self.txt_datostot_data['IVA']), symbol=False, grouping=True)}")
        c.drawRightString(577, altura-25, f"{locale.currency(float(self.txt_datostot_data['total']), grouping=True)}")
        if self.txt_datostot_data['IEPS'] != '0.00':
            altura +=10
        altura -=40
        c.roundRect(500,altura,80,65,1,fill=False)

        #QR
        base_url = 'https://verificacfdi.facturaelectronica.sat.gob.mx/default.aspx'
        qrcode_url = f"{base_url}?&id={self.xml_data.tfd.uuid}&re={self.xml_data.emisor['Rfc']}&rr={self.xml_data.receptor['Rfc']}&tt={self.xml_data.atributos['Total']}&fe={self.xml_data.atributos['Sello'][-8:]}"
        qr = QRCodeImage(qrcode_url, size=37.5*mm, border=False)
        qr.drawOn(c,473,altura-(37.5*mm)-5)

        #Sello Digital
        c.setFillColor(black)
        c.setFont('Times-New-Bold', 7)
        altura -=10
        c.drawString(43,altura,'Sello Digital del CFDI:')
        c.setFont('Times-New', 6)
        altura = self.FitText(c,43,altura-8,self.xml_data.atributos['Sello'],123)
        c.setFont('Times-New-Bold', 7)
        altura-=2
        c.drawString(43,altura,'Sello del SAT:')
        altura-=9
        c.setFont('Times-New', 6)
        altura = self.FitText(c, 43, altura, self.xml_data.tfd.sello_digital_sat, 123)
        altura-=2
        c.setFont('Times-New-Bold', 7)
        c.drawString(43,altura,'Cadena Original del Complemento de Certificación Digital del SAT:')
        altura-=9

        cadena_odecomplemento = f"||{self.xml_data.tfd.version}|{self.xml_data.tfd.uuid}|{self.xml_data.tfd.fecha_timbrado}|{self.xml_data.tfd.proveedor_certificado}|{self.xml_data.atributos['Sello']}|{self.xml_data.tfd.tfd_nodecert}||"
        c.setFont('Times-New', 6)
        altura = self.FitText(c, 43, altura, cadena_odecomplemento, 123)
        c.drawString(118,altura-1, f"{self.txt_datoscom_data['noCertificado']}")
        c.drawString(253,altura-1, f"{self.xml_data.tfd.tfd_nodecert}")
        c.drawString(80,altura-7, f"{self.xml_data.tfd.fecha_timbrado}")
        c.setFont('Times-New-Bold', 6)
        c.drawString(43,altura-1, 'No. de Certificado del CFDI:')
        c.drawString(180,altura-1, '|No. de Certificado del SAT:')
        c.drawString(315,altura-1, '|Fecha y Hora de')
        c.drawString(43,altura-7, 'Certificacion:')
        c.setFont('Times-New-Bold', 7)

        #Stroke
        #altura = altura-(37.5*mm)-5
        altura -=20
        c.setStrokeColor(grey)
        c.setDash([1, 1], 0)
        c.line(20, altura, 580, altura)

        c.setStrokeColor(black)
        c.setDash([1, 0], 0)

        altura -= 10
        c.setFont('Times-New', 6)
        c.drawString(20,altura, 'DEBO Y PAGARE A LA ORDEN DE PABLO IGNACIO MICHEL ONTIVEROS, EN ESTA CIUDAD DE GUADALAJARA, JALISCO EL DIA')
        c.drawString(537,altura, 'LA CANTIDAD')
        c.drawString(410,altura, 'DE')
        c.drawString(470,altura, 'DE')
        c.drawString(20,altura-7, 'DE $')
        c.drawString(72,altura-7, '(')
        c.drawString(577,altura-7, ')')
        c.drawString(20,altura-14, 'VALOR DE MERCANCÍA RECIBIDA A MI ENTERA SATISFACCIÓN A PARTIR DE SU VENCIMIENTO ESTE PAGARÉ CAUSARÁ INTERES A RAZÓN DEL')
        c.drawString(445,altura-14, '%')
        c.drawString(20,altura-21, 'MENSUAL.')
        c.drawString(40,altura-28, 'GUADALAJARA, JAL. A.')
        c.drawString(143,altura-28, 'DE')
        c.drawString(237,altura-28, 'DE')
        c.setFont('Times-New-Bold', 6)
        c.drawString(386,altura, f"{self.txt_empresa_data['diaPag']}")
        c.drawString(427,altura, f"{self.txt_empresa_data['mesPag']}")
        c.drawString(485,altura, f"{self.txt_empresa_data['yearPag']}")
        c.drawCentredString(52,altura-7, f"{locale.currency(float(self.txt_datostot_data['total']), symbol=False, grouping=True)}")
        c.drawString(80,altura-7, f"{self.txt_datostot_data['cantidadConLetra']}")
        c.drawRightString(440,altura-14, f"{self.txt_empresa_data['interesPag']}")
        c.drawString(115,altura-28, f"{self.txt_empresa_data['diaFac']}")
        c.drawString(160,altura-28, f"{self.txt_empresa_data['mesFac']}")
        c.drawString(249,altura-28, f"{self.txt_empresa_data['yearFac']}")

        altura-=48
        #Receptor, primer cuadro etiquetas no estáticas
        c.setFont('Times-New-Bold', 7)
        c.drawString(20, altura, f"{self.xml_data.receptor['Nombre']}")
        altura -= 8
        c.drawString(20, altura, f"{self.txt_receptor_data['calle']} , {self.txt_receptor_data['colonia']} {self.txt_receptor_data['CPLabel']}")
        altura -= 8
        c.drawString(20, altura, f"{self.txt_receptor_data['localidad']}")
        altura -= 8
        c.drawString(20, altura, f"{self.txt_receptor_data['estado']}, {self.txt_receptor_data['pais']}")
        altura -= 8
        c.drawString(20, altura, f"{self.txt_receptor_data['idFiscal']}")
        altura -= 8
        c.drawString(20, altura, f"{self.txt_receptor_data['telefono']}")

        altura += 32

        #Cuadro de factura
        c.setFillColor(self.purple)
        c.roundRect(500, altura, 80, 30, 4, fill=True)
        c.setFillColor(white)
        c.roundRect(500, altura, 80, 15, 4, fill=True)
        c.setFillColor(white)
        c.setFont('Times-New', 8)
        c.drawString(521, altura+20, 'FACTURA')
        c.setFont('Times-New', 10)
        c.setFillColor(black)
        c.drawString(518, altura+5, f"{self.xml_data.atributos['Serie']}{self.xml_data.atributos['Folio']}")
        

        #FIRMA
        altura-=5
        c.setFont('Times-New', 5)
        c.setLineWidth(0.1)
        c.setStrokeColor(grey)
        c.line(330, altura, 415, altura)
        c.drawString(361, altura-10, 'ACEPTO')
        c.drawString(350, altura-15, 'NOMBRE Y FIRMA')
        c.setLineWidth(1)
        altura-=20
        c.drawString(330, altura-15, 'RECIBIDA LA MERCANCÍA EL CLIENTE CUENTA CON UN PLAZO DE MÁXIMO DE 10 DÍAS PARA')
        c.drawString(332, altura-20, 'INCONFORMARSE POR ESCRITO DE LO CONTRARIO SE ACEPTA A SU ENTERA SATISFACCIÓN')

    def UnaPagina(self, c):
        altura = 553
        c.setFont('Times-New-Bold', 6)
        for idx, concepto in enumerate(self.xml_data.conceptos):
            if concepto.atributos['ClaveProdServ'] != '01010101':
                c.drawCentredString(28, altura, concepto.atributos['NoIdentificacion'])
                for art in self.txt_detalle_data:
                    if ((art['Articulo'] == concepto.atributos['NoIdentificacion']) and (art['Bultos'] == concepto.atributos['Cantidad'])):
                        c.drawCentredString(426, altura, str(art['Kgs']))
                        if str(art['Descto']) != '0.00':
                            c.drawRightString(525, altura, str(art['Descto']))
                        break
            else:
                c.drawCentredString(426, altura, '0')
            c.drawString(53, altura, concepto.atributos['ClaveProdServ'])
            c.drawString(315, altura, concepto.atributos['ObjetoImp'])
            c.drawCentredString(352, altura, concepto.atributos['Cantidad'])
            c.drawString(385, altura, concepto.atributos['ClaveUnidad'])
            c.drawRightString(479, altura, concepto.atributos['ValorUnitario'])
            c.drawRightString(580, altura, concepto.atributos['Importe'])
            altura = self.FitText(c, 90, altura, concepto.atributos['Descripcion'], 55, 9)

        # Añadir el número de página
        c.setFont('Times-New', 5.5)
        c.drawRightString(474, 830, f"Pag {self.pagina_actual}/{self.total_paginas}")

        c.setFont('Times-New', 6)
        altura -= 15
        # Cuadro gris
        c.setFillColor(lightgrey)
        if self.txt_empresa_data['obs01'] == '':
            aux_h = 13.5
            aux_y = 6.5
        else:
            aux_h = 20
            aux_y = 0
        if self.txt_empresa_data['obs02'] == '':
            aux_h -= 6.5
            aux_y += 6.5
        c.rect(20, altura+aux_y, 560, aux_h, fill=True, stroke=0)
        c.setFillColor(black)
        c.drawString(25, altura+15, self.txt_datosfa_data['ResumenTax'])
        if self.txt_empresa_data['obs01'] == '':
            aux_alt = 6.5
        else:
            aux_alt = 0
            c.drawString(25, altura+8.5, self.txt_empresa_data['obs01'])
        if self.txt_empresa_data['obs02'] != '':
            c.drawString(25, altura+2+aux_alt, self.txt_empresa_data['obs02'])

        self.Footer(c, altura)

    def MasPags(self, c):
        altura = 553
        conceptos_por_pagina = (altura - 346) // 9
        
        for idx, concepto in enumerate(self.xml_data.conceptos):
            if idx != 0 and idx % conceptos_por_pagina == 0:
                # Página completa, pasa a la siguiente página
                altura -= 15
                c.setFillColor(lightgrey)
                if self.txt_empresa_data['obs01'] == '':
                    aux_h = 13.5
                    aux_y = 6.5
                else:
                    aux_h = 20
                    aux_y = 0
                if self.txt_empresa_data['obs02'] == '':
                    aux_h -= 6.5
                    aux_y += 6.5
                c.rect(20, altura+aux_y, 560, aux_h, fill=True, stroke=0)
                c.setFillColor(black)
                c.drawString(25, altura+15, self.txt_datosfa_data['ResumenTax'])
                if self.txt_empresa_data['obs01'] == '':
                    aux_alt = 6.5
                else:
                    aux_alt = 0
                    c.drawString(25, altura+8.5, self.txt_empresa_data['obs01'])
                if self.txt_empresa_data['obs02'] != '':
                    c.drawString(25, altura+2+aux_alt, self.txt_empresa_data['obs02'])

                # Añadir número de página
                c.setFont('Times-New', 5.5)
                c.drawRightString(474, 830, f"Pag {self.pagina_actual}/{self.total_paginas}")
                
                c.setFont('Times-New', 6)
                c.showPage()  # Nueva página
                self.pagina_actual += 1
                self.GetStaticHeaderText(c)
                self.GetFolios(c)
                self.GetRectangles(c)
                self.GetDetalleHeader(c)
                altura = 553

            # Imprimir el concepto actual
            c.setFont('Times-New-Bold', 6)
            if concepto.atributos['ClaveProdServ'] != '01010101':
                c.drawCentredString(28, altura, concepto.atributos['NoIdentificacion'])
                for art in self.txt_detalle_data:
                    if ((art['Articulo'] == concepto.atributos['NoIdentificacion']) and (art['Bultos'] == concepto.atributos['Cantidad'])):
                        c.drawCentredString(426, altura, str(art['Kgs']))
                        if str(art['Descto']) != '0.00':
                            c.drawRightString(525, altura, str(art['Descto']))
                        break
            else:
                c.drawCentredString(426, altura, '0')
            c.drawString(53, altura, concepto.atributos['ClaveProdServ'])
            c.drawString(315, altura, concepto.atributos['ObjetoImp'])
            c.drawCentredString(352, altura, concepto.atributos['Cantidad'])
            c.drawString(385, altura, concepto.atributos['ClaveUnidad'])
            c.drawRightString(479, altura, concepto.atributos['ValorUnitario'])
            c.drawRightString(580, altura, concepto.atributos['Importe'])
            altura = self.FitText(c, 90, altura, concepto.atributos['Descripcion'], 55, 9)

        # Finalizar última página
        c.setFont('Times-New', 6)
        altura -= 15
        c.setFillColor(lightgrey)
        if self.txt_empresa_data['obs01'] == '':
            aux_h = 13.5
            aux_y = 6.5
        else:
            aux_h = 20
            aux_y = 0
        if self.txt_empresa_data['obs02'] == '':
            aux_h -= 6.5
            aux_y += 6.5
        c.rect(20, altura+aux_y, 560, aux_h, fill=True, stroke=0)
        c.setFillColor(black)
        c.drawString(25, altura+15, self.txt_datosfa_data['ResumenTax'])
        if self.txt_empresa_data['obs01'] == '':
            aux_alt = 6.5
        else:
            aux_alt = 0
            c.drawString(25, altura+8.5, self.txt_empresa_data['obs01'])
        if self.txt_empresa_data['obs02'] != '':
            c.drawString(25, altura+2+aux_alt, self.txt_empresa_data['obs02'])

        # Añadir número de página
        c.setFont('Times-New', 5.5)
        c.drawRightString(474, 830, f"Pag {self.pagina_actual}/{self.total_paginas}")

        c.setFont('Times-New', 6)
        self.Footer(c, altura)

    #Se fija la altura
    @abstractmethod
    def PrintConceptos(self, c):
        altura = 553
        c.setFillColor(black)

        # Calcular el número total de páginas
        num_conceptos = len(self.xml_data.conceptos)
        conceptos_por_pagina = (altura - 346) // 9  # Conceptos que caben en una página

        self.total_paginas = (num_conceptos // conceptos_por_pagina) + (1 if num_conceptos % conceptos_por_pagina > 0 else 0)
        self.pagina_actual = 1

        if self.total_paginas == 1:
            self.UnaPagina(c)  # Solo necesita una página
        else:
            self.MasPags(c)  # Necesita más de una página
