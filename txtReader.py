class TxtData:

    def __init__(self):
        self.emisor_data : dict = {}
        self.receptor_data : dict = {}
        self.empresa_data : dict = {}
        self.datosfa_data : dict = {}

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

