import xml.etree.ElementTree as ET


class Comprobante:

    def __init__(self, root):
        ns = {'cfdi': 'http://www.sat.gob.mx/cfd/4', 'tfd': 'http://www.sat.gob.mx/TimbreFiscalDigital'}
        self.atributos = root.attrib
        self.emisor = root.find(".//cfdi:Emisor", namespaces=ns).attrib
        self.receptor = root.find(".//cfdi:Receptor", namespaces=ns).attrib
        self.conceptos = [Concepto(concepto, ns) for concepto in root.findall(".//cfdi:Concepto", namespaces=ns)]
        self.impuestos = Impuestos(root.find(".//cfdi:Impuestos", namespaces=ns), ns)
        self.tfd = TimbreFiscalDigital(root.find(".//tfd:TimbreFiscalDigital", namespaces=ns))

class Concepto:
    def __init__(self, element, ns):
        self.atributos = element.attrib
        self.traslados = [Traslado(traslado, ns) for traslado in element.findall(".//cfdi:Impuestos/cfdi:Traslados/cfdi:Traslado", namespaces=ns)]

class Traslado:
    def __init__(self, element, ns):
        self.atributos = element.attrib

class Impuestos:
    def __init__(self, element, ns):
        self.atributos = element.attrib
        self.traslados = [Traslado(traslado, ns) for traslado in element.findall(".//cfdi:Traslados/cfdi:Traslado", namespaces=ns)]

class TimbreFiscalDigital():
    def __init__(self, element):
        ns = {'tfd': 'http://www.sat.gob.mx/TimbreFiscalDigital'}
        self.tfd_nodecert = element.get('NoCertificadoSAT')
        self.uuid = element.get("UUID")
        self.fecha_timbrado = element.get("FechaTimbrado")
        self.sello_digital_sat = element.get("SelloSAT")
        self.version = element.get('Version')
        self.proveedor_certificado = element.get('RfcProvCertif')

class XMLData(Comprobante):

    def __init__(self):
        self.purple = '#3333cc'

    def GetData(self, xml_obj):
        tree = ET.parse(xml_obj)
        root = tree.getroot()
        comprobante = Comprobante(root)
        return comprobante

