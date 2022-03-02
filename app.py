import os
import json
from flask import Flask, jsonify, request
from flask_migrate import Migrate
from models import db, Usuario, ClienteDt, Nota, Dt2019, Dt2020, Dt2021, Dt2022, Dt2023, Dt2024
from flask_cors import CORS
from flask_jwt_extended import create_access_token, JWTManager
from werkzeug.security import check_password_hash, generate_password_hash
from flask import render_template

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqlconnector://admin:curso2021@database-1.clcxl18xumje.us-east-1.rds.amazonaws.com/basedatos"
''' os.environ.get('DB_CONNECTION_STRING') mysql+mysqlconnector://admin:curso2021@database-1.clcxl18xumje.us-east-1.rds.amazonaws.com/basedatos '''
db.init_app(app)
Migrate(app, db)
app.config["JWT_SECRET_KEY"] = "@alfa123@254alfacentaurizxcKKvbnm@123456789ASDFGHJKL"
'''os.environ.get('JWT_SECRET_KEY') @alfa123@254alfacentaurizxcKKvbnm@123456789ASDFGHJKL'''
jwt = JWTManager(app)

# Main html


@app.route('/')
def main():
    return render_template('index.html')


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

''' Esta es la ruta que genera los clientes en la Vista Ampliada de Direccion Tributaria '''
@app.route('/xDt/<int:page_num>', methods=['GET'])
def xDt(page_num=None):
    if (request.method == 'GET'):
        clientesDt= ClienteDt.query.paginate(per_page=1000, page=page_num, error_out=True)
        paginas = clientesDt.pages
        pagina = clientesDt.page
        clientesDt= clientesDt.items
        clientesDt = list(
            map(lambda clienteDt: clienteDt.serializeX(), clientesDt))
        return jsonify(clientesDt, paginas, pagina), 200

''' Esta es la ruta de Busqueda para la Barra de Busqueda. '''
@app.route('/busquedaDt', methods=['POST'])  
def busquedaDt():
    request_body = request.data
    decoded_object = json.loads(request_body)
    busqueda = decoded_object["busqueda"]
    busqueda = "%{}%".format(busqueda)
    clientesDt = ClienteDt.query.filter((ClienteDt.razon.like(busqueda)) | (ClienteDt.rut.like(busqueda)) | (ClienteDt.correo.like(busqueda)) | (ClienteDt.correoSecundario.like(busqueda)) | (ClienteDt.correoTerciario.like(busqueda)) | (ClienteDt.fono.like(busqueda)) | (ClienteDt.representante.like(busqueda)) | (ClienteDt.rutRepresentante.like(busqueda)) | (ClienteDt.id.like(busqueda)) | (ClienteDt.libre.like(busqueda))).all()
    paginas = 1
    pagina = 1
    if clientesDt is not None:
        clientesDt = list(
            map(lambda clienteDt: clienteDt.serializeX(), clientesDt))
        return jsonify(clientesDt, paginas, pagina), 200
    else:
        return jsonify({"Error": "Tu busqueda no ha Arrojado Resultados"}), 401

''' Esta es la Ruta para hacer Filtros en Vista Ampliada '''
@app.route('/filtroDt', methods=['POST'])  
def filtroDt():
    request_body = request.data
    decoded_object = json.loads(request_body)
    vigente = decoded_object['vigente']
    whatsapp = decoded_object['whatsapp']
    erpyme = decoded_object['erpyme']
    p = decoded_object['p']
    sacar = decoded_object['sacar']
    dicom = decoded_object['dicom']
    repetido = decoded_object['repetido']
    tipoPago = decoded_object['tipoPago']

    if vigente != None:
        clientesDt = ClienteDt.query.filter(ClienteDt.vigente.like(vigente)).all()
    if whatsapp != None:
        clientesDt = ClienteDt.query.filter(ClienteDt.whatsapp.like(whatsapp)).all()
    if erpyme != None:
        clientesDt = ClienteDt.query.filter(ClienteDt.erpyme.like(erpyme)).all()
    if p != None:
        clientesDt = ClienteDt.query.filter(ClienteDt.p.like(p)).all()
    if sacar != None:
        clientesDt = ClienteDt.query.filter(ClienteDt.sacar.like(sacar)).all()
    if dicom != None:
        clientesDt = ClienteDt.query.filter(ClienteDt.dicom.like(dicom)).all()
    if repetido != None:
        clientesDt = ClienteDt.query.filter(ClienteDt.repetido.like(repetido)).all()
    if tipoPago != None:
        clientesDt = ClienteDt.query.filter(ClienteDt.tipoPago.like(tipoPago)).all()

    ''' print(filtrado) '''
    ''' filtrado = "%{}%".format(filtrado) '''
    ''' clientesDt = ClienteDt.query.filter(ClienteDt.vigente.like(filtrado)).all() '''
    paginas = 1
    pagina = 1
    if clientesDt is not None:
        clientesDt = list(
            map(lambda clienteDt: clienteDt.serializeInfo(), clientesDt))
        return jsonify(clientesDt, paginas, pagina), 200
    else:
        return jsonify({"Error": "Tu filtrado no ha Arrojado Resultados"}), 401

@app.route('/clienteDt', methods=['POST'])
@app.route('/clienteDt/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def ClientesDt(id=None):
    if (request.method == 'GET'):
        if(id is not None):
            clienteDt = ClienteDt.query.get(id)
            return jsonify(clienteDt.serializeInfo()), 200

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
        representante = decoded_object['representante']
        rutRepresentante = decoded_object['rutRepresentante']
        fechaContratacion = decoded_object['fechaContratacion']
        erpyme = decoded_object['erpyme']
        p = decoded_object['p']
        sacar = decoded_object['sacar']
        dicom = decoded_object['dicom']
        repetido = decoded_object['repetido']
        libre = decoded_object['libre']
        mesesPagados = decoded_object['mesesPagados']
        tipoPago = decoded_object['tipoPago']

        clienteDt = ClienteDt()
        clienteDt.razon = razon
        clienteDt.rut = rut
        clienteDt.vigente = vigente
        clienteDt.correo = correo
        clienteDt.correoSecundario = correoSecundario
        clienteDt.correoTerciario = correoTerciario
        clienteDt.fono = fono
        clienteDt.whatsapp = whatsapp
        clienteDt.representante = representante
        clienteDt.rutRepresentante = rutRepresentante
        clienteDt.fechaContratacion = fechaContratacion
        clienteDt.erpyme = erpyme
        clienteDt.p = p
        clienteDt.sacar = sacar
        clienteDt.dicom = dicom
        clienteDt.repetido = repetido
        clienteDt.libre = libre
        clienteDt.mesesPagados = mesesPagados
        clienteDt.tipoPago = tipoPago

        clienteDt.save()

        return jsonify(clienteDt.serialize()), 201

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
        representante = decoded_object['representante']
        rutRepresentante = decoded_object['rutRepresentante']
        fechaContratacion = decoded_object['fechaContratacion']
        erpyme = decoded_object['erpyme']
        p = decoded_object['p']
        sacar = decoded_object['sacar']
        dicom = decoded_object['dicom']
        repetido = decoded_object['repetido']
        libre = decoded_object['libre']
        mesesPagados = decoded_object['mesesPagados']
        tipoPago = decoded_object['tipoPago']

        clienteDt = ClienteDt.query.get(id)
        if razon != None:
            clienteDt.razon = razon
        if rut != None:
            clienteDt.rut = rut
        if vigente != None:
            clienteDt.vigente = vigente
        if correo != None:
            clienteDt.correo = correo
        if correoSecundario != None:
            clienteDt.correoSecundario = correoSecundario
        if correoTerciario != None:
            clienteDt.correoTerciario = correoTerciario
        if fono != None:
            clienteDt.fono = fono
        if whatsapp != None:
            clienteDt.whatsapp = whatsapp
        if representante != None:
            clienteDt.representante = representante
        if rutRepresentante != None:
            clienteDt.rutRepresentante = rutRepresentante
        if fechaContratacion != None:
            clienteDt.fechaContratacion = fechaContratacion
        if erpyme != None:
            clienteDt.erpyme = erpyme
        if p != None:
            clienteDt.p = p
        if sacar != None:
            clienteDt.sacar = sacar
        if dicom != None:
            clienteDt.dicom = dicom
        if repetido != None:
            clienteDt.repetido = repetido
        if libre != None:
            clienteDt.libre = libre
        if mesesPagados != None:
            clienteDt.mesesPagados = mesesPagados
        if tipoPago != None:
            clienteDt.tipoPago = tipoPago

        clienteDt.update()

        return jsonify(clienteDt.serialize()), 201

    if (request.method == 'DELETE'):
        clienteDt = ClienteDt.query.get(id)
        clienteDt.delete()
        return jsonify({"success": "Deal deleted"}), 200


@app.route('/dt2019', methods=['GET', 'POST'])
@app.route('/dt2019/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def Dt2019s(id=None):
    if (request.method == 'GET'):
        if(id is not None):
            detallesPago = Dt2019.query.filter_by(clienteDtid=id).all()
            detallesPago = list(
                map(lambda detallePago: detallePago.serialize(), detallesPago))
            return jsonify(detallesPago), 200
        detallesPago = Dt2019.query.all()
        detallesPago = list(
            map(lambda detallePago: detallePago.serialize(), detallesPago))
        return jsonify(detallesPago), 200

    if (request.method == 'POST'):
        request_body = request.data
        decoded_object = json.loads(request_body)
        mes = decoded_object['mes']
        numeroTransferencia = decoded_object['numeroTransferencia']
        montoPagado = decoded_object['montoPagado']
        montoCobrado = decoded_object['montoCobrado']
        mesesPagados = decoded_object['mesesPagados']
        facturaNumero = decoded_object['facturaNumero']
        comentario = decoded_object['comentario']
        fechaIngresoPago = decoded_object['fechaIngresoPago']
        clienteDtid = decoded_object['clienteDtid']

        dtPago2019 = Dt2019()
        dtPago2019.mes = mes
        dtPago2019.numeroTransferencia = numeroTransferencia
        dtPago2019.montoPagado = montoPagado
        dtPago2019.montoCobrado = montoCobrado
        dtPago2019.mesesPagados = mesesPagados
        dtPago2019.facturaNumero = facturaNumero
        dtPago2019.comentario = comentario
        dtPago2019.fechaIngresoPago = fechaIngresoPago
        dtPago2019.clienteDtid = clienteDtid

        dtPago2019.save()

        return jsonify(dtPago2019.serialize()), 201

    if (request.method == 'PUT'):
        request_body = request.data
        decoded_object = json.loads(request_body)
        mes = decoded_object['mes']
        numeroTransferencia = decoded_object['numeroTransferencia']
        montoPagado = decoded_object['montoPagado']
        montoCobrado = decoded_object['montoCobrado']
        mesesPagados = decoded_object['mesesPagados']
        facturaNumero = decoded_object['facturaNumero']
        comentario = decoded_object['comentario']

        dtPago2019 = Dt2019.query.get(id)

        if mes != None:
            dtPago2019.mes = mes
        if numeroTransferencia != None:
            dtPago2019.numeroTransferencia = numeroTransferencia
        if montoPagado != None:
            dtPago2019.montoPagado = montoPagado
        if montoCobrado != None:
            dtPago2019.montoCobrado = montoCobrado
        if comentario != None:
            dtPago2019.comentario = comentario
        if facturaNumero != None:
            dtPago2019.facturaNumero = facturaNumero
        if mesesPagados != None:
            dtPago2019.mesesPagados = mesesPagados

        dtPago2019.update()

        return jsonify(dtPago2019.serialize()), 201

    if (request.method == 'DELETE'):
        dtPago2019 = Dt2019.query.get(id)
        dtPago2019.delete()
        return jsonify({"success": "Deal deleted"}), 200


@app.route('/dt2020', methods=['GET', 'POST'])
@app.route('/dt2020/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def Dt2020s(id=None):
    if (request.method == 'GET'):
        if(id is not None):
            detallesPago = Dt2020.query.filter_by(clienteDtid=id).all()
            detallesPago = list(
                map(lambda detallePago: detallePago.serialize(), detallesPago))
            return jsonify(detallesPago), 200
        detallesPago = Dt2020.query.all()
        detallesPago = list(
            map(lambda detallePago: detallePago.serialize(), detallesPago))
        return jsonify(detallesPago), 200

    if (request.method == 'POST'):
        request_body = request.data
        decoded_object = json.loads(request_body)
        mes = decoded_object['mes']
        numeroTransferencia = decoded_object['numeroTransferencia']
        montoPagado = decoded_object['montoPagado']
        montoCobrado = decoded_object['montoCobrado']
        mesesPagados = decoded_object['mesesPagados']
        facturaNumero = decoded_object['facturaNumero']
        comentario = decoded_object['comentario']
        fechaIngresoPago = decoded_object['fechaIngresoPago']
        clienteDtid = decoded_object['clienteDtid']

        dtPago2020 = Dt2020()
        dtPago2020.mes = mes
        dtPago2020.numeroTransferencia = numeroTransferencia
        dtPago2020.montoPagado = montoPagado
        dtPago2020.montoCobrado = montoCobrado
        dtPago2020.mesesPagados = mesesPagados
        dtPago2020.facturaNumero = facturaNumero
        dtPago2020.comentario = comentario
        dtPago2020.fechaIngresoPago = fechaIngresoPago
        dtPago2020.clienteDtid = clienteDtid

        dtPago2020.save()

        return jsonify(dtPago2020.serialize()), 201

    if (request.method == 'PUT'):
        request_body = request.data
        decoded_object = json.loads(request_body)
        mes = decoded_object['mes']
        numeroTransferencia = decoded_object['numeroTransferencia']
        montoPagado = decoded_object['montoPagado']
        montoCobrado = decoded_object['montoCobrado']
        mesesPagados = decoded_object['mesesPagados']
        facturaNumero = decoded_object['facturaNumero']
        comentario = decoded_object['comentario']

        dtPago2020 = Dt2020.query.get(id)

        if mes != None:
            dtPago2020.mes = mes
        if numeroTransferencia != None:
            dtPago2020.numeroTransferencia = numeroTransferencia
        if montoPagado != None:
            dtPago2020.montoPagado = montoPagado
        if montoCobrado != None:
            dtPago2020.montoCobrado = montoCobrado
        if facturaNumero != None:
            dtPago2020.facturaNumero = facturaNumero
        if comentario != None:
            dtPago2020.comentario = comentario
        if mesesPagados != None:
            dtPago2020.mesesPagados = mesesPagados

        dtPago2020.update()

        return jsonify(dtPago2020.serialize()), 201

    if (request.method == 'DELETE'):
        dtPago2020 = Dt2020.query.get(id)
        dtPago2020.delete()
        return jsonify({"success": "Deal deleted"}), 200


@app.route('/dt2021', methods=['GET', 'POST'])
@app.route('/dt2021/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def Dt2021s(id=None):
    if (request.method == 'GET'):
        if(id is not None):
            detallesPago = Dt2021.query.filter_by(clienteDtid=id).all()
            detallesPago = list(
                map(lambda detallePago: detallePago.serialize(), detallesPago))
            return jsonify(detallesPago), 200
        detallesPago = Dt2021.query.all()
        detallesPago = list(
            map(lambda detallePago: detallePago.serialize(), detallesPago))
        return jsonify(detallesPago), 200

    if (request.method == 'POST'):
        request_body = request.data
        decoded_object = json.loads(request_body)
        mes = decoded_object['mes']
        numeroTransferencia = decoded_object['numeroTransferencia']
        montoPagado = decoded_object['montoPagado']
        montoCobrado = decoded_object['montoCobrado']
        mesesPagados = decoded_object['mesesPagados']
        facturaNumero = decoded_object['facturaNumero']
        comentario = decoded_object['comentario']
        fechaIngresoPago = decoded_object['fechaIngresoPago']
        clienteDtid = decoded_object['clienteDtid']

        dtPago2021 = Dt2021()
        dtPago2021.mes = mes
        dtPago2021.numeroTransferencia = numeroTransferencia
        dtPago2021.montoPagado = montoPagado
        dtPago2021.montoCobrado = montoCobrado
        dtPago2021.mesesPagados = mesesPagados
        dtPago2021.facturaNumero = facturaNumero
        dtPago2021.comentario = comentario
        dtPago2021.fechaIngresoPago = fechaIngresoPago
        dtPago2021.clienteDtid = clienteDtid

        dtPago2021.save()

        return jsonify(dtPago2021.serialize()), 201

    if (request.method == 'PUT'):
        request_body = request.data
        decoded_object = json.loads(request_body)
        mes = decoded_object['mes']
        numeroTransferencia = decoded_object['numeroTransferencia']
        montoPagado = decoded_object['montoPagado']
        montoCobrado = decoded_object['montoCobrado']
        mesesPagados = decoded_object['mesesPagados']
        facturaNumero = decoded_object['facturaNumero']
        comentario = decoded_object['comentario']

        dtPago2021 = Dt2021.query.get(id)

        if mes != None:
            dtPago2021.mes = mes
        if numeroTransferencia != None:
            dtPago2021.numeroTransferencia = numeroTransferencia
        if montoPagado != None:
            dtPago2021.montoPagado = montoPagado
        if montoCobrado != None:
            dtPago2021.montoCobrado = montoCobrado
        if facturaNumero != None:
            dtPago2021.facturaNumero = facturaNumero
        if comentario != None:
            dtPago2021.comentario = comentario
        if mesesPagados != None:
            dtPago2021.mesesPagados = mesesPagados

        dtPago2021.update()

        return jsonify(dtPago2021.serialize()), 201

    if (request.method == 'DELETE'):
        dtPago2021 = Dt2021.query.get(id)
        dtPago2021.delete()
        return jsonify({"success": "Deal deleted"}), 200


@app.route('/dt2022', methods=['GET', 'POST'])
@app.route('/dt2022/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def Dt2022s(id=None):
    if (request.method == 'GET'):
        if(id is not None):
            detallesPago = Dt2022.query.filter_by(clienteDtid=id).all()
            detallesPago = list(
                map(lambda detallePago: detallePago.serialize(), detallesPago))
            return jsonify(detallesPago), 200
        detallesPago = Dt2022.query.all()
        detallesPago = list(
            map(lambda detallePago: detallePago.serialize(), detallesPago))
        return jsonify(detallesPago), 200

    if (request.method == 'POST'):
        request_body = request.data
        decoded_object = json.loads(request_body)
        mes = decoded_object['mes']
        numeroTransferencia = decoded_object['numeroTransferencia']
        montoPagado = decoded_object['montoPagado']
        montoCobrado = decoded_object['montoCobrado']
        mesesPagados = decoded_object['mesesPagados']
        facturaNumero = decoded_object['facturaNumero']
        comentario = decoded_object['comentario']
        fechaIngresoPago = decoded_object['fechaIngresoPago']
        clienteDtid = decoded_object['clienteDtid']

        dtPago2022 = Dt2022()
        dtPago2022.mes = mes
        dtPago2022.numeroTransferencia = numeroTransferencia
        dtPago2022.montoPagado = montoPagado
        dtPago2022.montoCobrado = montoCobrado
        dtPago2022.mesesPagados = mesesPagados
        dtPago2022.facturaNumero = facturaNumero
        dtPago2022.comentario = comentario
        dtPago2022.fechaIngresoPago = fechaIngresoPago
        dtPago2022.clienteDtid = clienteDtid

        dtPago2022.save()

        return jsonify(dtPago2022.serialize()), 201

    if (request.method == 'PUT'):
        request_body = request.data
        decoded_object = json.loads(request_body)
        mes = decoded_object['mes']
        numeroTransferencia = decoded_object['numeroTransferencia']
        montoPagado = decoded_object['montoPagado']
        montoCobrado = decoded_object['montoCobrado']
        mesesPagados = decoded_object['mesesPagados']
        facturaNumero = decoded_object['facturaNumero']
        comentario = decoded_object['comentario']

        dtPago2022 = Dt2022.query.get(id)

        if mes != None:
            dtPago2022.mes = mes
        if numeroTransferencia != None:
            dtPago2022.numeroTransferencia = numeroTransferencia
        if montoPagado != None:
            dtPago2022.montoPagado = montoPagado
        if montoCobrado != None:
            dtPago2022.montoCobrado = montoCobrado
        if facturaNumero != None:
            dtPago2022.facturaNumero = facturaNumero
        if comentario != None:
            dtPago2022.comentario = comentario
        if mesesPagados != None:
            dtPago2022.mesesPagados = mesesPagados

        dtPago2022.update()

        return jsonify(dtPago2022.serialize()), 201

    if (request.method == 'DELETE'):
        dtPago2022 = Dt2022.query.get(id)
        dtPago2022.delete()
        return jsonify({"success": "Deal deleted"}), 200


@app.route('/dt2023', methods=['GET', 'POST'])
@app.route('/dt2023/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def Dt2023s(id=None):
    if (request.method == 'GET'):
        if(id is not None):
            detallesPago = Dt2023.query.filter_by(clienteDtid=id).all()
            detallesPago = list(
                map(lambda detallePago: detallePago.serialize(), detallesPago))
            return jsonify(detallesPago), 200
        detallesPago = Dt2023.query.all()
        detallesPago = list(
            map(lambda detallePago: detallePago.serialize(), detallesPago))
        return jsonify(detallesPago), 200

    if (request.method == 'POST'):
        request_body = request.data
        decoded_object = json.loads(request_body)
        mes = decoded_object['mes']
        numeroTransferencia = decoded_object['numeroTransferencia']
        montoPagado = decoded_object['montoPagado']
        montoCobrado = decoded_object['montoCobrado']
        mesesPagados = decoded_object['mesesPagados']
        facturaNumero = decoded_object['facturaNumero']
        comentario = decoded_object['comentario']
        fechaIngresoPago = decoded_object['fechaIngresoPago']
        clienteDtid = decoded_object['clienteDtid']

        dtPago2023 = Dt2023()
        dtPago2023.mes = mes
        dtPago2023.numeroTransferencia = numeroTransferencia
        dtPago2023.montoPagado = montoPagado
        dtPago2023.montoCobrado = montoCobrado
        dtPago2023.mesesPagados = mesesPagados
        dtPago2023.facturaNumero = facturaNumero
        dtPago2023.comentario = comentario
        dtPago2023.fechaIngresoPago = fechaIngresoPago
        dtPago2023.clienteDtid = clienteDtid

        dtPago2023.save()

        return jsonify(dtPago2023.serialize()), 201

    if (request.method == 'PUT'):
        request_body = request.data
        decoded_object = json.loads(request_body)
        mes = decoded_object['mes']
        numeroTransferencia = decoded_object['numeroTransferencia']
        montoPagado = decoded_object['montoPagado']
        montoCobrado = decoded_object['montoCobrado']
        mesesPagados = decoded_object['mesesPagados']
        facturaNumero = decoded_object['facturaNumero']
        comentario = decoded_object['comentario']

        dtPago2023 = Dt2023.query.get(id)

        if mes != None:
            dtPago2023.mes = mes
        if numeroTransferencia != None:
            dtPago2023.numeroTransferencia = numeroTransferencia
        if montoPagado != None:
            dtPago2023.montoPagado = montoPagado
        if montoCobrado != None:
            dtPago2023.montoCobrado = montoCobrado
        if facturaNumero != None:
            dtPago2023.facturaNumero = facturaNumero
        if comentario != None:
            dtPago2023.comentario = comentario
        if mesesPagados != None:
            dtPago2023.mesesPagados = mesesPagados

        dtPago2023.update()

        return jsonify(dtPago2023.serialize()), 201

    if (request.method == 'DELETE'):
        dtPago2023 = Dt2023.query.get(id)
        dtPago2023.delete()
        return jsonify({"success": "Deal deleted"}), 200


@app.route('/dt2024', methods=['GET', 'POST'])
@app.route('/dt2024/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def Dt2024s(id=None):
    if (request.method == 'GET'):
        if(id is not None):
            detallesPago = Dt2024.query.filter_by(clienteDtid=id).all()
            detallesPago = list(
                map(lambda detallePago: detallePago.serialize(), detallesPago))
            return jsonify(detallesPago), 200
        detallesPago = Dt2024.query.all()
        detallesPago = list(
            map(lambda detallePago: detallePago.serialize(), detallesPago))
        return jsonify(detallesPago), 200

    if (request.method == 'POST'):
        request_body = request.data
        decoded_object = json.loads(request_body)
        mes = decoded_object['mes']
        numeroTransferencia = decoded_object['numeroTransferencia']
        montoPagado = decoded_object['montoPagado']
        montoCobrado = decoded_object['montoCobrado']
        mesesPagados = decoded_object['mesesPagados']
        facturaNumero = decoded_object['facturaNumero']
        comentario = decoded_object['comentario']
        fechaIngresoPago = decoded_object['fechaIngresoPago']
        clienteDtid = decoded_object['clienteDtid']

        dtPago2024 = Dt2024()
        dtPago2024.mes = mes
        dtPago2024.numeroTransferencia = numeroTransferencia
        dtPago2024.montoPagado = montoPagado
        dtPago2024.montoCobrado = montoCobrado
        dtPago2024.mesesPagados = mesesPagados
        dtPago2024.facturaNumero = facturaNumero
        dtPago2024.comentario = comentario
        dtPago2024.fechaIngresoPago = fechaIngresoPago
        dtPago2024.clienteDtid = clienteDtid

        dtPago2024.save()

        return jsonify(dtPago2024.serialize()), 201

    if (request.method == 'PUT'):
        request_body = request.data
        decoded_object = json.loads(request_body)
        mes = decoded_object['mes']
        numeroTransferencia = decoded_object['numeroTransferencia']
        montoPagado = decoded_object['montoPagado']
        montoCobrado = decoded_object['montoCobrado']
        mesesPagados = decoded_object['mesesPagados']
        facturaNumero = decoded_object['facturaNumero']
        comentario = decoded_object['comentario']

        dtPago2024 = Dt2024.query.get(id)

        if mes != None:
            dtPago2024.mes = mes
        if numeroTransferencia != None:
            dtPago2024.numeroTransferencia = numeroTransferencia
        if montoPagado != None:
            dtPago2024.montoPagado = montoPagado
        if montoCobrado != None:
            dtPago2024.montoCobrado = montoCobrado
        if facturaNumero != None:
            dtPago2024.facturaNumero = facturaNumero
        if comentario != None:
            dtPago2024.comentario = comentario
        if mesesPagados != None:
            dtPago2024.mesesPagados = mesesPagados

        dtPago2024.update()

        return jsonify(dtPago2024.serialize()), 201

    if (request.method == 'DELETE'):
        dtPago2024 = Dt2024.query.get(id)
        dtPago2024.delete()
        return jsonify({"success": "Deal deleted"}), 200


@app.route('/nota', methods=['GET', 'POST'])
@app.route('/nota/<int:id>', methods=['GET'])
def Notas(id=None):
    if (request.method == 'GET'):
        if(id is not None):
            notas = Nota.query.filter_by(clienteDtid=id).all()
            notas = list(
                map(lambda nota: nota.serialize(), notas))
            return jsonify(notas), 200
        notas = Nota.query.all()
        notas = list(
            map(lambda nota: nota.serialize(), notas))
        return jsonify(notas), 200

    if (request.method == 'POST'):
        request_body = request.data
        decoded_object = json.loads(request_body)
        comentario = decoded_object['comentario']
        fechaComentario = decoded_object['fechaComentario']
        clienteDtid = decoded_object['clienteDtid']

        nota = Nota()
        nota.comentario = comentario
        nota.fechaComentario = fechaComentario
        nota.clienteDtid = clienteDtid

        nota.save()

        return jsonify(nota.serialize()), 201


if __name__ == '__main__':
    app.run(debug=True)
