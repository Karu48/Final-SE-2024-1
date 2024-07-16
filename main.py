#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from dataclasses import dataclass
from flask import Flask, jsonify, request
from flask_cors import CORS


CuentaUsuario = {
    "21345" : {"saldo": 200, "contactos": ["123", "456"]},
    "123" : {"saldo": 400, "contactos": ["456"]},
    "456" : {"saldo": 300, "contactos": ["21345"]}
}

Operacion = {}

app = Flask(__name__)

CORS(app, origins='*')

@app.route('/billetera/contactos', methods=['GET'])
def get_contactos():
    minumero = request.args.get('minumero')
    if minumero not in CuentaUsuario:
        return jsonify({"status": "error"})
    return jsonify(CuentaUsuario[minumero]['contactos'])

@app.route('/billetera/historial', methods=['GET'])
def get_historial():
    minumero = request.args.get('minumero')
    if minumero not in CuentaUsuario:
        return jsonify({"status": "error"})
    if minumero not in Operacion:
        return jsonify([])
    return jsonify(Operacion[minumero])

@app.route('/billetera/pagar', methods=['GET'])
def pagar():
    # Data
    minumero = request.args.get('minumero')
    numerodestino = request.args.get('numerodestino')
    valor = request.args.get('valor')

    # Accounts exist
    if minumero not in CuentaUsuario or numerodestino not in CuentaUsuario:
        return jsonify({"status": "error"})
    if CuentaUsuario[minumero]['saldo'] < int(valor):
        return jsonify({"status": "error"})
    
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

    return jsonify({"status": "ok"})

if __name__ == '__main__':
    app.run(port=5000, host='0.0.0.0')