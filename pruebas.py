import unittest
from main import app, CuentaUsuario, Operacion

class TestBilleteraElectronica(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_transferir_exito(self):
        # Caso de éxito: Transferencia válida
        response = self.app.get('/billetera/pagar', query_string={
            'minumero': '21345',
            'numerodestino': '123',
            'valor': 50
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['status'], 'ok')
        self.assertEqual(CuentaUsuario['21345']['saldo'], 150)
        self.assertEqual(CuentaUsuario['123']['saldo'], 450)

    def test_transferir_exito_historial(self):
        # Caso de éxito: Historial de operaciones actualizado
        self.app.get('/billetera/pagar', query_string={
            'minumero': '21345',
            'numerodestino': '123',
            'valor': 50
        })
        response = self.app.get('/billetera/historial', query_string={
            'minumero': '21345'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 1)
        operacion = response.json[0]
        self.assertEqual(operacion['valor'], '50')
        self.assertEqual(operacion['tipo'], 'enviado')

    def test_transferir_error_saldo_insuficiente(self):
        # Caso de error: Saldo insuficiente
        response = self.app.get('/billetera/pagar', query_string={
            'minumero': '21345',
            'numerodestino': '123',
            'valor': 250
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['status'], 'error')
        self.assertEqual(CuentaUsuario['21345']['saldo'], 200)
        self.assertEqual(CuentaUsuario['123']['saldo'], 400)

    def test_transferir_error_contacto_no_valido(self):
        # Caso de error: Destino no es un contacto válido
        response = self.app.get('/billetera/pagar', query_string={
            'minumero': '21345',
            'numerodestino': '789',  # 789 no es un contacto válido
            'valor': 50
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['status'], 'error')
        self.assertEqual(CuentaUsuario['21345']['saldo'], 200)
        self.assertEqual(CuentaUsuario['123']['saldo'], 400)

    def test_transferir_error_saldo_y_contacto(self):
        # Caso de error: Saldo insuficiente y destino no válido
        response = self.app.get('/billetera/pagar', query_string={
            'minumero': '21345',
            'numerodestino': '789',  # 789 no es un contacto válido
            'valor': 250  # Saldo insuficiente
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['status'], 'error')
        self.assertEqual(CuentaUsuario['21345']['saldo'], 200)
        self.assertEqual(CuentaUsuario['123']['saldo'], 400)

if __name__ == '__main__':
    unittest.main()
