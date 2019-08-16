from flask import Flask, render_template,  redirect, url_for, escape, request
import mysql.connector
import json
import datetime
#import conn


def run_query(query=''):
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="controlPagos"
    )

    mycursor = mydb.cursor()

    mycursor.execute(query)
    
    if query.upper().startswith('SELECT'): 
        data = mycursor.fetchall() 
    else: 
        mydb.commit()               
        data = None 

    mycursor.close()    
    mydb.close()
    return data


app = Flask(__name__)

@app.route("/clientes")
def clientes():
    return render_template("clientes.html")

@app.route("/ingreso_pagos")
def ingreso_pagos():
    return render_template("ingreso_pagos.html")

@app.route("/consulta_pagos")
def consulta_pagos():
    return render_template("consulta_pagos.html")

@app.route("/consulta_pagos_i2")
def consulta_pagos_i2():
    return render_template("consulta_pagos_i2.html")

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/getClientes",methods=['POST'])
def getClientes():
    sql = "SELECT * FROM cliente"
    data = run_query(sql)
    clientes = [] 
    for cl in data: 
        cliente = { 'id' : cl[0] , 'nit' : cl[1] , 'nombre': cl[2] }
        clientes.append(cliente)
    return json.dumps({'status':'OK','clientes':json.dumps(clientes)})


@app.route("/ingresoCliente",methods=['POST'])
def ingresoclientes(): 
    nit = request.form['nit']
    usuario = request.form['username']
    monto = request.form['monto']
    direccion = request.form['direccion']
    telefono = request.form['telefono']
    email = request.form['email']
    regimen = request.form['regimen']
    saldo = request.form['saldo']
    sql = "INSERT INTO cliente (NIT,NOMBRE,MENSUAL,DIRECCION,TELEFONO,EMAIL,REGIMEN,SALDO) VALUES(%i,'%s',%f,'%s','%s','%s','%s',%f)" % (int(nit),usuario,float(monto),direccion,telefono,email,regimen,float(saldo))
    run_query(sql)
    return  redirect(url_for('clientes'))


@app.route("/nuevoPago",methods=['POST'])
def nuevoPago(): 
    identificador = request.form['id']
    tipo = request.form['tipo']
    monto = request.form['monto']
    descripcion = request.form['descripcion']
    fecha = request.form['fecha']
    #hoy = datetime.datetime.now()
    #hoystr = str(hoy.strftime("%Y-%m-%d"))
    sql = "INSERT INTO  pago (idCliente,fechaPago,monto,descripcion,tipo) VALUES(%i,'%s',%f,'%s','%s')" % (int(identificador),fecha,float(monto),descripcion,tipo)
    run_query(sql)
    return  redirect(url_for('ingreso_pagos'))

@app.route("/getPagos",methods=['POST'])
def getPagos():
    sql = "SELECT NIT,NOMBRE,fechaPago,pago.monto FROM cliente , pago WHERE cliente.idCliente = pago.idCliente"
    data = run_query(sql)
    clientes = [] 
    for cl in data: 
        cliente = { 'nit' : cl[0] , 'nombre' : cl[1] , 'fechaInicio': str(cl[2]),'fin': str(cl[3]) ,'fechaPago': str(cl[4]) , 'monto': str(cl[5]) }
        clientes.append(cliente) 
    return json.dumps(clientes)       


@app.route("/consultaPagos",methods=['POST'])
def consultaPagos():
    sql = "SELECT  NOMBRE,pago.monto FROM cliente , pago WHERE fechaPago >= '%s' AND fechaPago <= '%s'  AND cliente.idCliente = pago.idCliente" % (request.form['fechainicio'], request.form['fechaFin'])
    data = run_query(sql)
    clientes = [] 
    for cl in data: 
        cliente = { 'nombre' : cl[0] , 'monto' : str(cl[1]) }
        clientes.append(cliente) 

    print(clientes)    
    return json.dumps(clientes)  

if __name__ == "__main__":
    app.run(debug=True)


