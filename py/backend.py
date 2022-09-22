import pymysql
import bcrypt
from flask import Flask, render_template, request, jsonify
from datetime import date
from datetime import datetime

class database:
    #coenxion la base de datos
    def __init__(self):
        self.connection = pymysql.connect(

            host='localhost',
            user='balduino',
            password='123',
            db='leodans'
        )
        self.cursor = self.connection.cursor()

        print("Conexion establecida exitosamente!!!")
    #funciones para consultas y insert en la tabla 'tbl_ropa'
    def select_ropa(self,id):

        sql= 'select * from tbl_ropa where id={}'.format(id) #hace un select con el id

        try:
            self.cursor.execute(sql)
            columns = [column[0] for column in self.cursor.description]
            results = []
            for row in self.cursor.fetchall():
                results.append(dict(zip(columns, row)))
            return results

        except Exception as e:
            raise
    
    def select_ropa_all(self):

        sql= 'select * from tbl_ropa'
        
        try:
            self.cursor.execute(sql)
            columns = [column[0] for column in self.cursor.description]
            results = []
            for row in self.cursor.fetchall():
                results.append(dict(zip(columns, row)))
            return results
        except Exception as e:
            raise
    
    def update_ropa(self,id,cantidad):
        sql= "update tbl_ropa set cantidad=cantidad-{} where id={}".format(cantidad,id)

        try:
            self.cursor.execute(sql)
            self.connection.commit()
        except Exception as e:
            raise

    def insert_ropa(self,nombre,cantidad):
        sql="insert into tbl_ropa (nombre_ropa,cantidad) values('{}',{});".format(nombre,cantidad)
        try:
            self.cursor.execute(sql)
            self.connection.commit()
            ropa=self.cursor.lastrowid
            return ropa
        except Exception as e:
            raise
    #select y insert en la tabla 'tbl_venta'
    def insert_venta(self,fecha,hora,total):
        sql="insert into tbl_venta (fecha,hora,total) values('{}','{}',{})".format(fecha,hora,total)
        try:
            self.cursor.execute(sql)
            self.connection.commit()
            venta=self.cursor.lastrowid
            return venta
        except Exception as e:
            raise
    
    def select_venta(self,id):
        sql="select id,date_format(fecha, '%d-%m-%Y') as fecha,date_format(hora, '%H:%i:%s') as hora from tbl_venta where id={}".format(id)

        try:
            self.cursor.execute(sql)
            columns = [column[0] for column in self.cursor.description]
            results = []
            for row in self.cursor.fetchall():
                results.append(dict(zip(columns, row)))
            return results
        except Exception as e:
            raise
    
    def select_venta_all(self):
        sql="select id,date_format(fecha, '%d-%m-%Y') as fecha,date_format(hora, '%H:%i:%s') as hora from tbl_venta"
        try:
            self.cursor.execute(sql)
            columns = [column[0] for column in self.cursor.description]
            results = []
            for row in self.cursor.fetchall():
                results.append(dict(zip(columns, row)))
            return results
        except Exception as e:
            raise

    def select_venta_fechas(self,f1,f2):
        sql="select id,date_format(fecha, '%d-%m-%Y') as fecha,date_format(hora, '%H:%i:%s') as hora, total from tbl_venta where tbl_venta.fecha between '{}' and '{}'".format(f1,f2)
        try:
            self.cursor.execute(sql)
            columns = [column[0] for column in self.cursor.description]
            results = []
            for row in self.cursor.fetchall():
                results.append(dict(zip(columns, row)))
            return results
        except Exception as e:
            raise

    def select_venta_hora(self,f1,h1,h2):
        sql="select id,date_format(fecha, '%d-%m-%Y') as fecha,date_format(hora, '%H:%i:%s') as hora from tbl_venta where tbl_venta.fecha = '{}' and tbl_venta.hora between '{}' and '{}'".format(f1,h1,h2)
        try:
            self.cursor.execute(sql)
            columns = [column[0] for column in self.cursor.description]
            results = []
            for row in self.cursor.fetchall():
                results.append(dict(zip(columns, row)))
            return results
        except Exception as e:
            raise   
    #funciones sobre select y insert venta_ropa
    def insert_producto_venta(self,id_venta,id_ropa,cantidad,monto):
        sql="insert into tbl_producto_venta (id_venta,id_ropa,cantidad,monto) values({},{},{},{})".format(id_venta,id_ropa,cantidad,monto)
        try:
            self.cursor.execute(sql)
            self.connection.commit()
            producto_venta=self.cursor.lastrowid
            return producto_venta
        except Exception as e:
            raise

    def select_venta_ropa_all(self):
        sql="select * from tbl_producto_venta"
        try:
            self.cursor.execute(sql)
            columns = [column[0] for column in self.cursor.description]
            results = []
            for row in self.cursor.fetchall():
                results.append(dict(zip(columns, row)))
            return results
        except Exception as e:
            raise

    def select_venta_ropa(self,id):
        sql="select * from tbl_producto_venta where id={}".format(id)
        try:
            self.cursor.execute(sql)
            columns = [column[0] for column in self.cursor.description]
            results = []
            for row in self.cursor.fetchall():
                results.append(dict(zip(columns, row)))
            return results
        except Exception as e:
            raise 
    
    def select_venta_ropa_fecha(self,f1,f2):
        sql="select date_format(tbl_venta.fecha, '%d-%m-%Y') as fecha,tbl_ropa.nombre_ropa,date_format(tbl_venta.hora,'%H:%i:%s') as hora from tbl_producto_venta inner join tbl_venta on tbl_producto_venta.id_venta = tbl_venta.id inner join tbl_ropa on tbl_producto_venta.id_ropa = tbl_ropa.id where tbl_venta.fecha BETWEEN '{}' and '{}'".format(f1,f2)
        try:
            self.cursor.execute(sql)
            columns = [column[0] for column in self.cursor.description]
            results = []
            for row in self.cursor.fetchall():
                results.append(dict(zip(columns, row)))
            return results
        except Exception as e:
            raise

    #cierra la conexion con la base de datos
    def close(self):
        self.connection.close()
#creo objeto de la clase database
mydata = database()
#creo mi objeto de flask
app = Flask(__name__)

@app.route("/")
def home():
    #return render_template('index.html')
    return "<p>puerco</p>"

#rutas de la tabla ropa
@app.route("/list")
def listar():
    data=mydata.select_ropa_all()
    return jsonify(data)

@app.route("/newropa", methods=['POST'])
def insert():
    name=request.form['nombre']
    cant=request.form['cantidad']

    data=mydata.insert_ropa(name,cant)
    
    data=mydata.select_ropa(data)

    return jsonify(data)

@app.route("/update_ropa", methods=['PUT'])
def update_ropa():
    id=request.form['id_ropa']
    cantidad=request.form['cantidad']
    mydata.update_ropa(id,cantidad)
    data=mydata.select_ropa(id)

    return jsonify(data)

#rutas de la tabla venta
@app.route("/newvent", methods=['POST'])
def insert_venta():
    total=request.form['total']
    fecha=date.today()
    hora=datetime.now()
    data=mydata.insert_venta(fecha,hora.time(),total)
    data=mydata.select_venta(data)

    return jsonify(data)

@app.route("/list_fecha", methods=['POST'])
def select_venta_fechas():
    fecha1=request.form['fecha1']
    fecha2=request.form['fecha2']
    data=mydata.select_venta_fechas(fecha1,fecha2)

    return jsonify(data)

@app.route("/list_hora", methods=['POST'])
def select_venta_hora():
    fecha1=request.form['fecha1']
    hora1=request.form['hora1']
    hora2=request.form['hora2']
    data=mydata.select_venta_hora(fecha1,hora1,hora2)

    return jsonify(data)

@app.route("/list_venta")
def select_venta():
    data=mydata.select_venta(1)

    return jsonify(data)

#rutas del tabla tbl_venta_ropa
@app.route("/newproduct", methods=['POST'])
def insert_product_venta():
    id_v=request.form['id_venta']
    id_r=request.form['id_ropa']
    cantidad=request.form['cantidad']
    monto=request.form['monto']
    data=mydata.insert_producto_venta(id_v,id_r,cantidad,monto)
    data=mydata.select_venta_ropa(data)

    return jsonify(data)

@app.route("/list_product")
def select_product_venta():
    data=mydata.select_venta_ropa(1)
    
    return jsonify(data)

@app.route("/list_product_fecha", methods=['POST'])
def select_product_fecha():
    fecha1=request.form['fecha1']
    fecha2=request.form['fecha2']
    data=mydata.select_venta_ropa_fecha(fecha1,fecha2)

    return jsonify(data)

app.run()

