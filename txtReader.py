class TxtData:

    def __init__(self):
        self.emisor_data : dict = {}
        self.receptor_data : dict = {}
        self.empresa_data : dict = {}
        self.datosfa_data : dict = {}
        self.datostot_data : dict = {}
        self.datoscom_data : dict = {}
        self.detalle_data : list = []

    def GetEmisorData(self, filename) -> dict:
        with open(filename, 'r', encoding='latin-1') as file:
            for line in file:
                if line.startswith('em:'):
                    parts = line.strip().split('=')
                    
                    if len(parts) == 2:
                        variable_name = parts[0][3:]
                        variable_value = parts[1]
                        self.emisor_data[variable_name] = variable_value

        return self.emisor_data

    def GetReceptorData(self, filename) -> dict:
        with open(filename, 'r', encoding='latin-1') as file:
            for line in file:
                if line.startswith('re:'):
                    parts = line.strip().split('=')
                    
                    if len(parts) == 2:
                        variable_name = parts[0][3:]
                        variable_receptor_value = parts[1]
                        self.receptor_data[variable_name] = variable_receptor_value

        return self.receptor_data

    def GetEmpresaData(self, filename) -> dict:
        with open(filename, 'r', encoding='latin-1') as file:
            for line in file:
                if line.startswith('emp:'):
                    parts = line.strip().split('=')
                    
                    if len(parts) == 2:
                        variable_name = parts[0][4:]
                        variable_receptor_value = parts[1]
                        self.empresa_data[variable_name] = variable_receptor_value

        return self.empresa_data

    def GetDatosfaData(self, filename) -> dict:
        with open(filename, 'r', encoding='latin-1') as file:
            for line in file:
                if line.startswith('FA:'):
                    parts = line.strip().split('=')
                    if len(parts) == 2:
                        variable_name = parts[0][3:]
                        variable_datosfa_value = parts[1]
                        self.datosfa_data[variable_name] = variable_datosfa_value
        return self.datosfa_data

    def GetTotalesData(self, filename) -> dict:
        with open(filename, 'r', encoding='latin-1') as file:
            for line in file:
                if line.startswith('tot:'):
                    parts = line.strip().split('=')
                    if len(parts) == 2:
                        variable_name = parts[0][4:]
                        variable_datostot_value = parts[1]
                        self.datostot_data[variable_name] = variable_datostot_value
        return self.datostot_data

    def GetComprobanteData(self, filename) -> dict:
        with open(filename, 'r', encoding='latin-1') as file:
            for line in file:
                if line.startswith('com:'):
                    parts = line.strip().split('=')
                    if len(parts) == 2:
                        variable_name = parts[0][4:]
                        variable_datoscom_value = parts[1]
                        self.datoscom_data[variable_name] = variable_datoscom_value
        return self.datoscom_data

    def GetDetalleData(self, filename):
        with open(filename, 'r', encoding='latin-1') as file:
            contenido = file.read()
            inicio = contenido.find("#InicioDetalle") + len("#InicioDetalle")
            fin = contenido.find("#FinDetalle")
            detalle = contenido[inicio:fin].strip()
            lineas = detalle.splitlines()
            columnas = lineas[0].strip().split('|')
            for linea in lineas[1:]:
                valores = linea.split('|')
                if (len(valores)-1 == len(columnas)) or (len(valores) == len(columnas)):
                    diccionario_det = {}
                    for i in range(len(columnas)):
                        if columnas[i] != '':
                            diccionario_det[columnas[i]] = valores[i]
                    self.detalle_data.append(diccionario_det)
        return self.detalle_data
