#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, request
from flask_cors import CORS
from datetime import date


CuentaUsuario = {
    "21345" : {"saldo": 200, "contactos": ["123", "456"], "nombre": "Arnaldo"},
    "123" : {"saldo": 400, "contactos": ["456"], "nombre": "Luisa"},
    "456" : {"saldo": 300, "contactos": ["21345"], "nombre": "Andrea"}
}

Operacion = {}

app = Flask(__name__)

CORS(app, origins='*')

@app.route('/billetera/contactos', methods=['GET'])
def get_contactos():
    minumero = request.args.get('minumero')
    if minumero not in CuentaUsuario:
        return ("Cuenta no existe")
    
    returnValue = ""
    for contacto in CuentaUsuario[minumero]['contactos']:
        returnValue += contacto + " : " + CuentaUsuario[contacto]['nombre'] + "\n"
    return returnValue

@app.route('/billetera/historial', methods=['GET'])
def get_historial():
    minumero = request.args.get('minumero')
    if minumero not in CuentaUsuario:
        return ("Cuenta no existe")
    if minumero not in Operacion:
        return ("")
    
    returnValue = ""
    for operacion in Operacion[minumero]:
        if operacion['tipo'] == "enviado":
            returnValue += "Pago realizado de " + operacion['valor'] + " a " + CuentaUsuario[operacion['destino']]["nombre"] + "\n"
        else:
            returnValue += "Pago recibido de " + operacion['valor'] + " de " + CuentaUsuario[operacion['origen']]["nombre"] + "\n"
    return (returnValue)

@app.route('/billetera/pagar', methods=['GET'])
def pagar():
    # Data
    minumero = request.args.get('minumero')
    numerodestino = request.args.get('numerodestino')
    valor = request.args.get('valor')

    # Accounts exist
    if minumero not in CuentaUsuario or numerodestino not in CuentaUsuario:
        return ("Cuenta no existe")
    if CuentaUsuario[minumero]['saldo'] < int(valor):
        return ("Saldo insuficiente")
    
    # Transfer
    CuentaUsuario[minumero]['saldo'] -= int(valor)
    CuentaUsuario[numerodestino]['saldo'] += int(valor)

    # Save sent
    if minumero not in Operacion:
        Operacion[minumero] = []
    Operacion[minumero].append({"tipo": "enviado", "valor": valor, "destino": numerodestino})
    
    # Save received
    if numerodestino not in Operacion:
        Operacion[numerodestino] = []
    Operacion[numerodestino].append({"tipo": "recibido", "valor": valor, "origen": minumero})

    date_ = date.today()
    return "Realizado el " + date_.strftime("%d/%m/%Y")

if __name__ == '__main__':
    app.run(port=5000, host='0.0.0.0')