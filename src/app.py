from cmath import e
from flask import Flask,jsonify, request
from config import config
from flaskext.mysql import MySQL


app = Flask(__name__)
conexion = MySQL(app)

@app.route('/bandejapaisa')
def listar_bandejapaisa():
    try:
        bandejapaisa=conexion.connection.bandejapaisa()
        sql = "SELECT frijol, arroz, chicharron  FROM bandejapaisa"
        bandejapaisa.execute(sql)
        datos = bandejapaisa.fetchall()
        bandejapaisa=[]
        for fila in datos:
            bandejapaisa = {'frijol': fila[0], 'arroz': fila[1], 'chicharron': fila[2]}
            bandejapaisa.append(bandejapaisa)
        return jsonify({'bandejapaisa': bandejapaisa, 'mensaje': "Estos son los ingredientes de la bandeja paisa."})
    except Exception as e: 
        return jsonify({'mensaje': "Error al listar."})

@app.route('/bandejapaisa/<frijol>')
def leer_bandejapaisa(frijol):
    try:
        bandejapaisa=conexion.connection.bandejapaisa()
        sql="SELECT frijol, arroz, chicharron FROM bandejapaisa WHERE frijol = '{0}'".format(frijol)
        bandejapaisa.execute(sql)
        datos=bandejapaisa.fetchone()
        if datos!= None:
            bandejapaisa = {'frijol':datos[0], 'arroz':datos[1], 'chicharron':datos[2]}
            return jsonify({'bandejapaisa':bandejapaisa,'mensaje':"bandejapaisa Encontrado."})
        else:
            return jsonify({'mensaje':"bandejapaisa no encontrado."})
    except Exception as e:
        return jsonify({'mensaje':"Error"})


@app.route('/bandejapaisa')#Este es el metodo POST
def registrar_bandejapaisa():
    try:
        bandejapaisa=conexion.connection.bandejapaisa()
        sql="""INSERT INTO  curso (frijol, arroz, chicharron)
         VALUES ('{0}','{1}','{2}')""".format(request.json['frijol'], request.json['arroz'], request.json['chicharron'])
        bandejapaisa.execute(sql)
        conexion.connection.commit()
        return({'mensaje':"bandejapaisa registrado."})
    except Exception as e:
        return jsonify({'mensaje':"Error"})


@app.route('/bandejapaisa/<frijol>')#Este es el metodo PUT
def modificar_bandejapaisa(frijol):
    try:
        bandejapaisa=conexion.connection.bandejapaisa()
        sql="UPDATE bandejapaisa SET arroz = '{0}', chicharron = '{1}' WHERE frijol = '{2}'".format(request.json['arroz'], request.json['chicharron'], frijol)
        bandejapaisa.execute(sql)
        conexion.connection.commit()
        return({'mensaje':"Curso actualizado."})
    except Exception as e:
        return jsonify({'mensaje':"Error"})


@app.route('/bandejapaisa/<frijol>')#Este es el metodo DELETE
def eliminar_bandejapaisa(frijol):
    try:
        bandejapaisa=conexion.connection.bandejapaisa()
        sql=" DELETE FROM bandejapaisa WHERE frijol = '{0}'".format(frijol)
        bandejapaisa.execute(sql)
        conexion.connection.commit()
        return({'mensaje':"bandejapaisa eliminado."})
    except Exception as e:
        return jsonify({'mensaje':"Error"})

def pag_no_encontrada(error):
    return "<h1>La página que buscas no existe</h1>",404 #Mensaje de eror

if __name__=='__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(404, pag_no_encontrada)
    app.run()

