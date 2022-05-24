import os
import json
from flask import Flask, jsonify, request
from flask_migrate import Migrate
from models import db, Usuario
from models import ClienteContabilidad, PagosContabilidad, NotaContabilidad
from flask_cors import CORS
from flask_jwt_extended import create_access_token, JWTManager
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqlconnector://admin:curso2021@database-1.clcxl18xumje.us-east-1.rds.amazonaws.com/basedatos"
''' os.environ.get('DB_CONNECTION_STRING') mysql+mysqlconnector://admin:curso2021@database-1.clcxl18xumje.us-east-1.rds.amazonaws.com/basedatos '''
db.init_app(app)
Migrate(app, db)
app.config["JWT_SECRET_KEY"] = os.environ.get('JWT_SECRET_KEY')
jwt = JWTManager(app)

# Main html

@app.route('/login', methods=['POST'])
def login_usuario():
    request_body = request.data
    decoded_object = json.loads(request_body)
    correo = decoded_object["correo"]
    clave = decoded_object["clave"]
    usuario = Usuario.query.filter_by(correo=correo).first()
    if usuario is not None:
        if check_password_hash(str(usuario.clave), clave) == True:
            token = create_access_token(identity=clave)
            return jsonify(usuario.serialize(), token), 200
    else:
        return jsonify({"Error": "Clave o Usuario incorrecto"}), 401

@app.route('/usuario', methods=['GET', 'POST'])
@app.route('/usuario/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def usuarios(id=None):
    if (request.method == 'GET'):
        if(id is not None):
            usuario = Usuario.query.get(id)
            return jsonify(usuario.serialize()), 200
        usuarios = Usuario.query.all()
        usuarios = list(map(lambda usuario: usuario.serialize(), usuarios))
        return jsonify(usuarios), 200

    if (request.method == 'POST'):
        request_body = request.data
        decoded_object = json.loads(request_body)
        nombre = decoded_object['nombre']
        apellido = decoded_object['apellido']
        correo = decoded_object['correo']
        clave = decoded_object['clave']
        tipo = decoded_object['tipo']

        usuario = Usuario()
        usuario.nombre = nombre
        usuario.apellido = apellido
        usuario.correo = correo
        usuario.clave = generate_password_hash(clave)
        usuario.tipo = tipo
        usuario.save()

        return jsonify(usuario.serialize())

    if (request.method == 'PUT'):
        request_body = request.data
        decoded_object = json.loads(request_body)
        nombre = decoded_object['nombre']
        apellido = decoded_object['apellido']
        correo = decoded_object['correo']
        clave = decoded_object['clave']
        tipo = decoded_object['tipo']

        usuario = Usuario.query.get(id)

        if nombre != None:
            usuario.nombre = nombre
        if apellido != None:
            usuario.apellido = apellido
        if correo != None:
            usuario.correo = correo
        if clave != None:
            usuario.clave = generate_password_hash(clave)
        if tipo != None:
            usuario.tipo = tipo

        usuario.update()

        return jsonify(usuario.serialize())

    if (request.method == 'DELETE'):
        usuario = Usuario.query.get(id)
        usuario.delete()
        return jsonify({"success": "User deleted"}), 200

''' CONTABILIDAD '''

''' Esta es la ruta que genera los clientes en la Vista Ampliada de Contabilidad '''
@app.route('/xContabilidad/<int:page_num>', methods=['GET'])
def xContabilidad(page_num=None):
    if (request.method == 'GET'):
        clientesContabilidad= ClienteContabilidad.query.paginate(per_page=50, page=page_num, error_out=True)
        paginas = clientesContabilidad.pages
        pagina = clientesContabilidad.page
        clientesContabilidad= clientesContabilidad.items
        clientesContabilidad = list(
            map(lambda clienteContabilidad: clienteContabilidad.serialize(), clientesContabilidad))
        return jsonify(clientesContabilidad, paginas, pagina), 200

''' Esta es la ruta de Busqueda para la Barra de Busqueda. '''
@app.route('/busquedaContabilidad', methods=['POST'])  
def busquedaContabilidad():
    request_body = request.data
    decoded_object = json.loads(request_body)
    busqueda = decoded_object["busqueda"]
    busqueda = "%{}%".format(busqueda)
    clientesContabilidad = ClienteContabilidad.query.filter((ClienteContabilidad.razon.like(busqueda)) | (ClienteContabilidad.rut.like(busqueda)) | (ClienteContabilidad.correo.like(busqueda)) | (ClienteContabilidad.correoSecundario.like(busqueda)) | (ClienteContabilidad.correoTerciario.like(busqueda)) | (ClienteContabilidad.fono.like(busqueda)) | (ClienteContabilidad.id.like(busqueda)) | (ClienteContabilidad.libre.like(busqueda))).all()
    paginas = 1
    pagina = 1
    if clientesContabilidad is not None:
        clientesContabilidad = list(
            map(lambda clienteContabilidad: clienteContabilidad.serialize(), clientesContabilidad))
        return jsonify(clientesContabilidad, paginas, pagina), 200
    else:
        return jsonify({"Error": "Tu busqueda no ha Arrojado Resultados"}), 401

''' Esta es la Ruta para hacer Filtros en Vista Ampliada '''
@app.route('/filtroContabilidad', methods=['POST'])  
def filtroContabilidad():
    request_body = request.data
    decoded_object = json.loads(request_body)
    vigente = decoded_object['vigente']
    whatsapp = decoded_object['whatsapp']
    erpyme = decoded_object['erpyme']
    dicom = decoded_object['dicom']
    repetido = decoded_object['repetido']

    if vigente != None:
        clientesContabilidad = ClienteContabilidad.query.filter(ClienteContabilidad.vigente.like(vigente)).all()
    if whatsapp != None:
        clientesContabilidad = ClienteContabilidad.query.filter(ClienteContabilidad.whatsapp.like(whatsapp)).all()
    if erpyme != None:
        clientesContabilidad = ClienteContabilidad.query.filter(ClienteContabilidad.erpyme.like(erpyme)).all()
    if dicom != None:
        clientesContabilidad = ClienteContabilidad.query.filter(ClienteContabilidad.dicom.like(dicom)).all()
    if repetido != None:
        clientesContabilidad = ClienteContabilidad.query.filter(ClienteContabilidad.repetido.like(repetido)).all()

    paginas = 1
    pagina = 1
    if clientesContabilidad is not None:
        clientesContabilidad = list(
            map(lambda clienteDt: clienteDt.serialize(), clientesContabilidad))
        return jsonify(clientesContabilidad, paginas, pagina), 200
    else:
        return jsonify({"Error": "Tu filtrado no ha Arrojado Resultados"}), 401

@app.route('/clienteContabilidad', methods=['POST'])
@app.route('/clienteContabilidad/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def clientesContabilidad(id=None):
    if (request.method == 'GET'):
        if(id is not None):
            clienteContabilidad = ClienteContabilidad.query.get(id)
            return jsonify(clienteContabilidad.serialize()), 200

    if (request.method == 'POST'):
        request_body = request.data
        decoded_object = json.loads(request_body)
        razon = decoded_object['razon']
        rut = decoded_object['rut']
        vigente = decoded_object['vigente']
        correo = decoded_object['correo']
        correoSecundario = decoded_object['correoSecundario']
        correoTerciario = decoded_object['correoTerciario']
        fono = decoded_object['fono']
        whatsapp = decoded_object['whatsapp']
        erpyme = decoded_object['erpyme']
        dicom = decoded_object['dicom']
        repetido = decoded_object['repetido']
        libre = decoded_object['libre']

        clienteContabilidad = ClienteContabilidad()
        clienteContabilidad.razon = razon
        clienteContabilidad.rut = rut
        clienteContabilidad.vigente = vigente
        clienteContabilidad.correo = correo
        clienteContabilidad.correoSecundario = correoSecundario
        clienteContabilidad.correoTerciario = correoTerciario
        clienteContabilidad.fono = fono
        clienteContabilidad.whatsapp = whatsapp
        clienteContabilidad.erpyme = erpyme
        clienteContabilidad.dicom = dicom
        clienteContabilidad.repetido = repetido
        clienteContabilidad.libre = libre

        clienteContabilidad.save()

        return jsonify(clienteContabilidad.serialize()), 201

    if (request.method == 'PUT'):
        request_body = request.data
        decoded_object = json.loads(request_body)
        razon = decoded_object['razon']
        rut = decoded_object['rut']
        vigente = decoded_object['vigente']
        correo = decoded_object['correo']
        correoSecundario = decoded_object['correoSecundario']
        correoTerciario = decoded_object['correoTerciario']
        fono = decoded_object['fono']
        whatsapp = decoded_object['whatsapp']
        erpyme = decoded_object['erpyme']
        dicom = decoded_object['dicom']
        repetido = decoded_object['repetido']
        libre = decoded_object['libre']

        clienteContabilidad = ClienteContabilidad.query.get(id)
        if razon != None:
            clienteContabilidad.razon = razon
        if rut != None:
            clienteContabilidad.rut = rut
        if vigente != None:
            clienteContabilidad.vigente = vigente
        if correo != None:
            clienteContabilidad.correo = correo
        if correoSecundario != None:
            clienteContabilidad.correoSecundario = correoSecundario
        if correoTerciario != None:
            clienteContabilidad.correoTerciario = correoTerciario
        if fono != None:
            clienteContabilidad.fono = fono
        if whatsapp != None:
            clienteContabilidad.whatsapp = whatsapp
        if erpyme != None:
            clienteContabilidad.erpyme = erpyme
        if dicom != None:
            clienteContabilidad.dicom = dicom
        if repetido != None:
            clienteContabilidad.repetido = repetido
        if libre != None:
            clienteContabilidad.libre = libre

        clienteContabilidad.update()

        return jsonify(clienteContabilidad.serialize()), 201

    if (request.method == 'DELETE'):
        clienteContabilidad = ClienteContabilidad.query.get(id)
        clienteContabilidad.delete()
        return jsonify({"success": "Deal deleted"}), 200


@app.route('/pagosContabilidad', methods=['GET', 'POST'])
@app.route('/pagosContabilidad/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def pagosContabilidad(id=None):
    if (request.method == 'GET'):
        if(id is not None):
            detallesPago = PagosContabilidad.query.filter_by(clienteContabilidadid=id).all()
            detallesPago = list(
                map(lambda detallePago: detallePago.serialize(), detallesPago))
            return jsonify(detallesPago), 200
        detallesPago = PagosContabilidad.query.all()
        detallesPago = list(
            map(lambda detallePago: detallePago.serialize(), detallesPago))
        return jsonify(detallesPago), 200

    if (request.method == 'POST'):
        request_body = request.data
        decoded_object = json.loads(request_body)
        year = decoded_object['year']
        mes = decoded_object['mes']
        numeroTransferencia = decoded_object['numeroTransferencia']
        montoPagado = decoded_object['montoPagado']
        montoCobrado = decoded_object['montoCobrado']
        facturaNumero = decoded_object['facturaNumero']
        comentario = decoded_object['comentario']
        clienteContabilidadid = decoded_object['clienteContabilidadid']

        pagoContabilidad = PagosContabilidad()
        pagoContabilidad.year = year
        pagoContabilidad.mes = mes
        pagoContabilidad.numeroTransferencia = numeroTransferencia
        pagoContabilidad.montoPagado = montoPagado
        pagoContabilidad.montoCobrado = montoCobrado
        pagoContabilidad.facturaNumero = facturaNumero
        pagoContabilidad.comentario = comentario
        pagoContabilidad.clienteContabilidadid = clienteContabilidadid

        pagoContabilidad.save()

        return jsonify(pagoContabilidad.serialize()), 201

    if (request.method == 'PUT'):
        request_body = request.data
        decoded_object = json.loads(request_body)
        year = decoded_object['year']
        mes = decoded_object['mes']
        numeroTransferencia = decoded_object['numeroTransferencia']
        montoPagado = decoded_object['montoPagado']
        montoCobrado = decoded_object['montoCobrado']
        facturaNumero = decoded_object['facturaNumero']
        comentario = decoded_object['comentario']

        pagoContabilidad = PagosContabilidad.query.get(id)

        if year != None:
            pagoContabilidad.year = year
        if mes != None:
            pagoContabilidad.mes = mes
        if numeroTransferencia != None:
            pagoContabilidad.numeroTransferencia = numeroTransferencia
        if montoPagado != None:
            pagoContabilidad.montoPagado = montoPagado
        if montoCobrado != None:
            pagoContabilidad.montoCobrado = montoCobrado
        if comentario != None:
            pagoContabilidad.comentario = comentario
        if facturaNumero != None:
            pagoContabilidad.facturaNumero = facturaNumero

        pagoContabilidad.update()

        return jsonify(pagoContabilidad.serialize()), 201

    if (request.method == 'DELETE'):
        pagoContabilidad = PagosContabilidad.query.get(id)
        pagoContabilidad.delete()
        return jsonify({"success": "Deal deleted"}), 200

@app.route('/notaContabilidad', methods=['GET', 'POST'])
@app.route('/notaContabilidad/<int:id>', methods=['GET'])
def NotasContabilidad(id=None):
    if (request.method == 'GET'):
        if(id is not None):
            notas = NotaContabilidad.query.filter_by(clienteContabilidadid=id).all()
            notas = list(
                map(lambda nota: nota.serialize(), notas))
            return jsonify(notas), 200
        notas = NotaContabilidad.query.all()
        notas = list(
            map(lambda nota: nota.serialize(), notas))
        return jsonify(notas), 200

    if (request.method == 'POST'):
        request_body = request.data
        decoded_object = json.loads(request_body)
        comentario = decoded_object['comentario']
        fechaComentario = decoded_object['fechaComentario']
        clienteContabilidadid = decoded_object['clienteContabilidadid']

        nota = NotaContabilidad()
        nota.comentario = comentario
        nota.fechaComentario = fechaComentario
        nota.clienteContabilidadid = clienteContabilidadid

        nota.save()

        return jsonify(nota.serialize()), 201

if __name__ == '__main__':
    app.run(debug=True)
