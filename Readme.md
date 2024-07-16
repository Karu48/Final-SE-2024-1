# Integrantes:

### -  Rodrigo Gabriel Amaya Mory
### - Rodrigo Lauz Nakasone

# Pregunta 3:
#### En este caso se podria agregar un atributo a la clase CuentaUsuario que será totalSumado, este atributo acumulará los gastos del usuario del día y para que el uuario no pueda seguir transferiendo cuando totalSumado sobrepase los 200, usaremos un metodo LimiteTransferencia tipo bool que retornara True en caso sobrepase los 200 y false en caso siga estando menor que 200.

### **Casos de pruebas necesarios**
1. **Transferencia Exitosamente Dentro del Límite Diario**
   - **Descripción**: Transferir un monto dentro del límite diario acumulado de 200 soles.
2. **Transferencia Excediendo el Límite Diario**
   - **Descripción**: Intentar transferir un monto que cause que el total diario exceda 200 soles.
   - **Caso de Prueba**:
3. **Reseteo del Límite Diario**
   - **Descripción**: Realizar transferencias en un día hasta alcanzar el límite. Verificar que las transferencias el día siguiente se procesan correctamente con el límite reiniciado.      

### **Los casos de prueba existentes garantizan que no se introduzcan errores en la funcionalidad existente**
1. **Transferencia Exitosamente**
   - **Descripción**: Transferir un monto válido.
   - **Caso de Prueba**:
     ```python
     def test_transferir_exito(self):
         resultado = self.cuenta.transferir("987654321", 100)
         self.assertTrue(resultado, "La transferencia debería ser exitosa")
         self.assertEqual(self.cuenta.saldo, 900, "El saldo debería ser 900 después de la transferencia")
     ```

2. **Historial de Operaciones Actualizado**
   - **Descripción**: Verificar que el historial de operaciones se actualiza correctamente.
   - **Caso de Prueba**:
     ```python
     def test_transferir_exito_historial(self):
         self.cuenta.transferir("987654321", 100)
         self.assertEqual(len(self.cuenta.historial_operaciones), 1, "Debería haber una operación en el historial")
         operacion = self.cuenta.historial_operaciones[0]
         self.assertEqual(operacion.valor, 100, "El valor de la operación debería ser 100")
     ```

3. **Saldo Insuficiente**
   - **Descripción**: Intentar transferir un monto mayor al saldo disponible.
   - **Caso de Prueba**:
     ```python
     def test_transferir_error_saldo_insuficiente(self):
         resultado = self.cuenta.transferir("987654321", 1100)
         self.assertFalse(resultado, "La transferencia debería fallar por saldo insuficiente")
         self.assertEqual(self.cuenta.saldo, 1000, "El saldo no debería cambiar")
     ```
4. **Error de Saldo y Contacto**
   - **Descripción**: Intentar transferir un monto mayor al saldo disponible a un número que no es un contacto válido.
   - **Caso de Prueba**:
     ```python
     def test_transferir_error_saldo_y_contacto(self):
         resultado = self.cuenta.transferir("123123123", 1100)
         self.assertFalse(resultado, "La transferencia debería fallar por ambos errores")
         self.assertEqual(self.cuenta.saldo, 1000, "El saldo no debería cambiar")
     ```        