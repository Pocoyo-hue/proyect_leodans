import pymysql
import bcrypt
import jwt
from flask import Flask, make_response, render_template, request, jsonify
from flask_jwt import JWT, jwt_required, current_identity
from datetime import date
from datetime import datetime, timedelta


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

    #funciones tbl_rol

    def select_rol_all(self):
        sql='select * from tbl_rol'
        try:
            self.cursor.execute(sql)
            columns = [column[0] for column in self.cursor.description]
            results = []
            for row in self.cursor.fetchall():
                results.append(dict(zip(columns, row)))
            return results
        except Exception as e:
            raise

    #funciones tbl_user
    def select_user(self,id):
        sql='select user_rol from tbl_users where id={}'.format(id)
        try:
            self.cursor.execute(sql)
            columns = [column[0] for column in self.cursor.description]
            results = []
            for row in self.cursor.fetchall():
                results.append(dict(zip(columns, row)))
            return results

        except Exception as e:
            raise
    def authenticate(self,username):
        sql="select id,user_password,estado,id_rol from tbl_users where user_name='{}'".format(username)
        try:
            self.cursor.execute(sql)
            columns = [column[0] for column in self.cursor.description]
            results = []
            for row in self.cursor.fetchall():
                results.append(dict(zip(columns, row)))
            return results

        except Exception as e:
            raise

    def insert_user(self, username, password, rol,nombre,apellido):
        sql="insert into tbl_users (user_name,user_password,id_rol,estado,nombre,apellido) values(%s,%s,%s,%s,%s,%s);"
        try:
            self.cursor.execute(sql,(username,password,rol,True))
            self.connection.commit()
            user=self.cursor.lastrowid
            return user
        except Exception as e:
            raise
    #funciones para consultas y insert en la tabla 'tbl_ropa'
    def select_browser(self,text):
        sql='select tbl_ropa.id as id, tbl_talla.talla as talla, nombre_ropa from tbl_ropa inner join tbl_talla on tbl_ropa.id_talla = tbl_talla.id where nombre_ropa like "%{}%"'.format(text)
        try:
            self.cursor.execute(sql)
            columns = [column[0] for column in self.cursor.description]
            results = []
            for row in self.cursor.fetchall():
                results.append(dict(zip(columns, row)))
            return results
        except Exception as e:
            raise

    def select_ropa(self,id):

        sql= 'select tbl_ropa.id,nombre_ropa,tbl_talla.talla as talla from tbl_ropa inner join tbl_talla on tbl_ropa.id_talla = tbl_talla.id where tbl_ropa.id={}'.format(id) #hace un select con el id

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

        sql= 'select tbl_ropa.id,nombre_ropa,tbl_talla.talla as talla from tbl_ropa inner join tbl_talla on tbl_ropa.id_talla = tbl_talla.id'
        
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
        sql= "update tbl_ropa set cantidad=cantidad-{} where tbl_ropa.id={}".format(cantidad,id)

        try:
            self.cursor.execute(sql)
            self.connection.commit()
        except Exception as e:
            raise

    def insert_ropa(self,nombre,cantidad,talla):
        sql="insert into tbl_ropa (nombre_ropa,cantidad,id_talla) values('{}',{},{});".format(nombre,cantidad,talla)
        try:
            self.cursor.execute(sql)
            self.connection.commit()
            ropa=self.cursor.lastrowid
            return ropa
        except Exception as e:
            raise
    #select y insert en la tabla 'tbl_venta'
    def insert_venta(self,fecha,hora,total,u,u_c):
        sql="insert into tbl_venta (fecha,hora,total,id_user,id_user_caja) values('{}','{}',{},{},{})".format(fecha,hora,total,u,u_c)
        try:
            self.cursor.execute(sql)
            self.connection.commit()
            venta=self.cursor.lastrowid
            return venta
        except Exception as e:
            raise
    
    def select_venta(self,id):
        sql="select id,date_format(fecha, '%d-%m-%Y') as fecha,date_format(hora, '%H:%i:%s') as hora, total, tbl_user.nombre, tbl_user.apellido from tbl_venta inner join tbl_user on tbl_venta.id_user = tbl_user.id where id={}".format(id)

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
        sql="select id,date_format(fecha, '%d-%m-%Y') as fecha,date_format(hora, '%H:%i:%s') as hora, total, tbl_user.nombre, tbl_user.apellido from tbl_venta inner join tbl_user on tbl_venta.id_user = tbl_user.id"
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
        sql="select id,date_format(fecha, '%d-%m-%Y') as fecha,date_format(hora, '%H:%i:%s') as hora, total, tbl_user.nombre, tbl_user.apellido from tbl_venta inner join tbl_user on tbl_venta.id_user = tbl_user.id where tbl_venta.fecha between '{}' and '{}'".format(f1,f2)
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
        sql="select id,date_format(fecha, '%d-%m-%Y') as fecha,date_format(hora, '%H:%i:%s') as hora, total, tbl_user.nombre, tbl_user.apellido from tbl_venta inner join tbl_user on tbl_venta.id_user = tbl_user.id where tbl_venta.fecha = '{}' and tbl_venta.hora between '{}' and '{}'".format(f1,h1,h2)
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
#creo mi JWT
app.config['SECRET_KEY']='2101d85b8bc14fd39f80c2a1211699f4'

@app.route("/")
def home():
    #return render_template('index.html')
    return "<p>Bienbenido</p>"

def auth_in():
    token=request.headers['Authorization']
    if not token:
        return False
    try:
        token=token.replace("Bearer ","")
        payload=jwt.decode(token,app.config['SECRET_KEY'],algorithms=["HS256"])
        if datetime.strptime(payload['expiration'], '%Y-%m-%d %H:%M:%S.%f')<datetime.now():
            return False
        else:
            return True
    except:
        return jsonify({'Alert':'Invalid Token'})

#rutas de la tabla users
@app.route('/auth', methods=['POST'])
def auth():
    token=request.headers['Authorization']
    if not token:
        return jsonify({'Alert!':'Token is missing!'})
    try:
        token=token.replace("Bearer ","")
        payload=jwt.decode(token,app.config['SECRET_KEY'],algorithms=["HS256"])
        return jsonify(payload)
    except:
        return jsonify({'Alert':'Invalid Token'})

@app.route("/login", methods=['POST'])
def login_user():
    name=request.form['username']
    password=request.form['password'].encode('utf-8')
    data=mydata.authenticate(name)
    if data!=[]:
        hashed=data[0]['user_password']
        hashed=hashed.encode('utf-8')
        token='no auth'
        if bcrypt.checkpw(password,hashed) and data[0]['estado']==True:
            token=jwt.encode({
                'user':data[0]['id'],
                'rol':data[0]['id_rol'],
                'expiration':str(datetime.now()+timedelta(minutes=120))
            },
            app.config['SECRET_KEY'])
        else:
            token='Basic realm: "Authentication Failed!!"'
        return jsonify({'token':token})
    else:
        return make_response('unable to verify', 403, {'WWW-Authentication':'Basic realm: "Authentication Failed!!"'})

@app.route("/list_user",methods=['POST'])
def select_u():
    id=request.form['id_user']
    data=mydata.select_user(id)
    return jsonify(data)
@app.route("/new_user",methods=['POST'])
def insert_u():
    name=request.form['username']
    password=request.form['password']
    rol=request.form['user_rol']
    nombre=request.form['nombre']
    apellido=request.form['apellido']
    password=password.encode('utf-8')
    hashed=bcrypt.hashpw(password,bcrypt.gensalt())
    data=mydata.insert_user(name,hashed,rol,nombre,apellido)
    return jsonify(data)
#rutas de la tabla ropa
@app.route("/list")
def listar():
    a=auth_in()
    if a==True:
        data=mydata.select_ropa_all()
        return jsonify(data)
    else:
        return jsonify({'Alert':'Invalid Token'})

@app.route("/browser_ropa",methods=['POST'])
def browser_name():
    a=auth_in()
    if a==True:
        t=request.form['texto']
        if t=='':
            return jsonify({'err':'invalid format'})
        else:
            data=mydata.select_browser(t)
            return data
    else:
        return jsonify({'Alert':'Invalid Token'})

@app.route("/newropa", methods=['POST'])
def insert():
    a=auth_in()
    if a==True:
        name=request.form['nombre']
        cant=request.form['cantidad']
        talla=request.form['talla']

        data=mydata.insert_ropa(name,cant,talla)
        
        data=mydata.select_ropa(data)

        return jsonify(data)
    else:
        return jsonify({'Alert':'Invalid Token'})

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
    a=auth_in()
    if a==True:
        total=request.form['total']
        fecha=date.today()
        hora=datetime.now()
        data=mydata.insert_venta(fecha,hora.time(),total)
        data=mydata.select_venta(data)

        return jsonify(data)
    else:
        return jsonify({'Alert':'Invalid Token'})

@app.route("/list_fecha", methods=['POST'])
def select_venta_fechas():
    a=auth_in()
    if a==True:
        fecha1=request.form['fecha1']
        fecha2=request.form['fecha2']
        data=mydata.select_venta_fechas(fecha1,fecha2)

        return jsonify(data)
    else:
        return jsonify({'Alert':'Invalid Token'})
@app.route("/list_hora", methods=['POST'])
def select_venta_hora():
    a=auth_in()
    if a==True:
        fecha1=request.form['fecha1']
        hora1=request.form['hora1']
        hora2=request.form['hora2']
        data=mydata.select_venta_hora(fecha1,hora1,hora2)

        return jsonify(data)
    else:
        return jsonify({'Alert':'Invalid Token'})
@app.route("/list_venta")
def select_venta():
    data=mydata.select_venta(1)

    return jsonify(data)

#rutas del tabla tbl_venta_ropa
@app.route("/newproduct", methods=['POST'])
def insert_product_venta():
    a=auth_in()
    if a==True:
        id_v=request.form['id_venta']
        id_r=request.form['id_ropa']
        cantidad=request.form['cantidad']
        monto=request.form['monto']
        user=request.form['user']
        user_caja=request.form['user_caja']
        data=mydata.insert_producto_venta(id_v,id_r,cantidad,monto,user,user_caja)
        data=mydata.select_venta_ropa(data)

        return jsonify(data)
    else:
        return jsonify({'Alert':'Invalid Token'})

@app.route("/list_product")
def select_product_venta():
    data=mydata.select_venta_ropa(1)
    
    return jsonify(data)

@app.route("/list_product_fecha", methods=['POST'])
def select_product_fecha():
    a=auth_in()
    if a==True:
        fecha1=request.form['fecha1']
        fecha2=request.form['fecha2']
        data=mydata.select_venta_ropa_fecha(fecha1,fecha2)

        return jsonify(data)
    else:
        return jsonify({'Alert':'Invalid Token'})
        
app.run()


