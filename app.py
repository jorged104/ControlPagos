from flask import Flask, render_template,  redirect, url_for, escape, request
import mysql.connector
import json
import datetime
#import conn


def run_query(query=''):
    try:
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
            if  query.upper().startswith('INSERT'):
                data = mycursor.lastrowid            
              

        mycursor.close()    
        mydb.close()
        return data
    except expression as identifier: 
        print("Error en DB")
    return None    


def run_proc(name='', tupla = () ):
    try:
        mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database="controlPagos"
        )
        mycursor = mydb.cursor()
        mycursor.callproc(name,tupla)

        data = mycursor.stored_results()  
        return data       
    except expression as identifier:
        print("Error en DB")
    return None    

app = Flask(__name__)

@app.route("/clientes")
def clientes():
    return render_template("clientes.html")

@app.route("/ingreso_pagos")
def ingreso_pagos():
    return render_template("ingreso_pagos.html")

@app.route("/ingreso_Cobros")
def ingreso_cobros():
    return render_template("ingreso_cobros.html")    


@app.route("/consulta_pagos")
def consulta_pagos():
    return render_template("consulta_pagos.html")

@app.route("/consulta_pagos_i2")
def consulta_pagos_i2():
    return render_template("consulta_pagos_i2.html")

@app.route("/consulta_cliente")
def consulta_cliente():
    return render_template("consulta_cliente.html")

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
    cobros = request.form['cobros']

    sql = "INSERT INTO  pago (idCliente,fechaPago,monto,descripcion,tipo) VALUES(%i,'%s',%f,'%s','%s')" % (int(identificador),fecha,float(monto),descripcion,tipo)   
    respuesta = run_query(sql)
    run_proc("ingreso_pago" , ( int(identificador) , float(monto) ) )
    if (cobros != '' ):
        listacobros = cobros.split(",")  
        for c in listacobros:
            run_proc("setCobro", ( int(c) , int(respuesta) ) )
    return  redirect(url_for('ingreso_pagos'))

@app.route("/nuevoCobro",methods=['POST'])
def nuevoCobro(): 
    identificador = request.form['id']
    monto = request.form['monto']
    descripcion = request.form['descripcion']
    fecha = request.form['fecha']
    sql = "INSERT INTO  cobros (idusuario,fechaCobro,monto,descripcion) VALUES(%i,'%s',%f,'%s')" % (int(identificador),fecha,float(monto),descripcion)
    run_query(sql)
    run_proc("ingreso_cobro" , ( int(identificador) , float(monto) ) )
    return  redirect(url_for('ingreso_cobros'))

@app.route("/getPagos",methods=['POST'])
def getPagos():
    sql = "SELECT NIT,NOMBRE,fechaPago,pago.monto,descripcion FROM cliente , pago WHERE cliente.idCliente = pago.idCliente ORDER BY pago.idPago DESC LIMIT 50 "
    data = run_query(sql)
    clientes = [] 
    for cl in data: 
        cliente = { 'nit' : cl[0] , 'nombre' : cl[1] , 'fechaPago': str(cl[2]),'monto': str(cl[3]) , 'descripcion': str(cl[4]) }
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


@app.route("/getCobros",methods=['POST'])
def getCobros():
    sql = "SELECT  fechaCobro,monto,descripcion FROM cobros  WHERE idusuario == '%i' " % (request.form['id'])
    data = run_query(sql)
    clientes = [] 
    for cl in data: 
        cliente = { 'fecha' : cl[0] , 'monto' : str(cl[1]) , 'descripcion' : cl[2] }
        clientes.append(cliente) 

    print(clientes)    
    return json.dumps(clientes) 

@app.route("/getcobrospendientes",methods=['POST'])
def getcobrospendientes():
    sql = "SELECT  idcobro,descripcion , monto , fechaCobro  FROM cobros  WHERE idusuario = %i AND idpago IS NULL   " % (int(request.form['id']))
    print(sql)
    data = run_query(sql)
    clientes = [] 
    for cl in data: 
        cliente = { 'id' : cl[0] ,'desc': str(cl[1]) ,'monto' : str(cl[2]) , 'fecha' : str(cl[3]) }
        clientes.append(cliente) 
    #print(clientes)    
    return json.dumps(clientes)      


if __name__ == "__main__":
    app.run(debug=True)


