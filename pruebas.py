import unittest
from main import CuentaUsuario, Operacion
from datetime import date

class TestBilleteraElectronica(unittest.TestCase):

    def setUp(self):
        # Reiniciar el estado antes de cada prueba
        self.cuenta = {
            "21345" : {"saldo": 200, "contactos": ["123", "456"], "nombre": "Arnaldo"},
            "123" : {"saldo": 400, "contactos": ["456"], "nombre": "Luisa"},
            "456" : {"saldo": 300, "contactos": ["21345"], "nombre": "Andrea"}
        }
        self.operacion = {}

    def test_transferir_exito(self):
        # Caso de éxito: Transferencia válida
        resultado = self.transferir("21345", "123", 50)
        self.assertTrue(resultado, "La transferencia debería ser exitosa")
        self.assertEqual(self.cuenta['21345']['saldo'], 150, "El saldo debería ser 150 después de la transferencia")
        self.assertEqual(self.cuenta['123']['saldo'], 450, "El saldo debería ser 450 después de la transferencia")

    def test_transferir_exito_historial(self):
        # Caso de éxito: Historial de operaciones actualizado
        self.transferir("21345", "123", 50)
        historial = self.get_historial("21345")
        self.assertEqual(len(historial), 1, "Debería haber una operación en el historial")
        operacion = historial[0]
        self.assertEqual(operacion['valor'], 50, "El valor de la operación debería ser 50")
        self.assertEqual(operacion['tipo'], 'enviado', "El tipo de operación debería ser 'enviado'")

    def test_transferir_error_saldo_insuficiente(self):
        # Caso de error: Saldo insuficiente
        resultado = self.transferir("21345", "123", 250)
        self.assertFalse(resultado, "La transferencia debería fallar por saldo insuficiente")
        self.assertEqual(self.cuenta['21345']['saldo'], 200, "El saldo no debería cambiar")
        self.assertEqual(self.cuenta['123']['saldo'], 400, "El saldo no debería cambiar")

    def test_transferir_error_contacto_no_valido(self):
        # Caso de error: Destino no es un contacto válido
        resultado = self.transferir("21345", "789", 50)  # 789 no es un contacto válido
        self.assertFalse(resultado, "La transferencia debería fallar porque el destino no es un contacto")
        self.assertEqual(self.cuenta['21345']['saldo'], 200, "El saldo no debería cambiar")
        self.assertEqual(self.cuenta['123']['saldo'], 400, "El saldo no debería cambiar")

    def test_transferir_error_saldo_y_contacto(self):
        # Caso de error: Saldo insuficiente y destino no válido
        resultado = self.transferir("21345", "789", 250)  # 789 no es un contacto válido, saldo insuficiente
        self.assertFalse(resultado, "La transferencia debería fallar por ambos errores")
        self.assertEqual(self.cuenta['21345']['saldo'], 200, "El saldo no debería cambiar")
        self.assertEqual(self.cuenta['123']['saldo'], 400, "El saldo no debería cambiar")

    # Funciones auxiliares para pruebas
    def transferir(self, minumero, numerodestino, valor):
        if minumero not in self.cuenta or numerodestino not in self.cuenta:
            return False  # Cuenta no existe
        if self.cuenta[minumero]['saldo'] < valor:
            return False  # Saldo insuficiente
        
        # Transfer
        self.cuenta[minumero]['saldo'] -= valor
        self.cuenta[numerodestino]['saldo'] += valor

        # Save sent
        if minumero not in self.operacion:
            self.operacion[minumero] = []
        self.operacion[minumero].append({"tipo": "enviado", "valor": valor, "destino": numerodestino})
        
        # Save received
        if numerodestino not in self.operacion:
            self.operacion[numerodestino] = []
        self.operacion[numerodestino].append({"tipo": "recibido", "valor": valor, "origen": minumero})

        return True

    def get_historial(self, minumero):
        if minumero not in self.operacion:
            return []
        return self.operacion[minumero]

if __name__ == '__main__':
    unittest.main()
