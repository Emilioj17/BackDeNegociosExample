from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(30), nullable=False)
    apellido = db.Column(db.String(30), nullable=False)
    correo = db.Column(db.String(30), nullable=False, unique=True)
    clave = db.Column(db.String(200), nullable=False)
    tipo = db.Column(db.String(20), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "correo": self.correo,
            # "clave": self.clave, No retornará clave.
            "tipo": self.tipo,
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

''' CONTABILIDAD '''

class ClienteContabilidad(db.Model):
    __tablename__ = 'clientesContabilidad'
    id = db.Column(db.Integer, primary_key=True)
    razon = db.Column(db.String(100), nullable=False)
    rut = db.Column(db.String(20), nullable=False)
    vigente = db.Column(db.String(10), nullable=True, default="Si")
    correo = db.Column(db.String(50), nullable=False)
    correoSecundario = db.Column(db.String(50), nullable=True)
    correoTerciario = db.Column(db.String(50), nullable=True)
    fono = db.Column(db.String(10), nullable=True)
    whatsapp = db.Column(db.String(10), nullable=True)
    erpyme = db.Column(db.String(10), nullable=True, default="No")
    dicom = db.Column(db.String(10), nullable=True, default="No")
    repetido = db.Column(db.String(10), nullable=True, default="No")
    libre = db.Column(db.String(200), nullable=True)
    pagosContabilidadID = db.relationship(
        'PagosContabilidad', cascade='all, delete', backref='pagosContabilidad')
    notasContabilidadID = db.relationship(
        'NotaContabilidad', cascade='all, delete', backref='clientesContabilidadNotas')

    def serialize(self):
        return {
            "id": self.id,
            "razon": self.razon,
            "rut": self.rut,
            "vigente": self.vigente,
            "correo": self.correo,
            "correoSecundario": self.correoSecundario,
            "correoTerciario": self.correoTerciario,
            "fono": self.fono,
            "whatsapp": self.whatsapp,
            "erpyme": self.erpyme,
            "dicom": self.dicom,
            "repetido": self.repetido,
            "libre": self.libre,
            "pagosContabilidadID": self.get_pagosContabilidad(),
            "notasContabilidad": self.get_notasContabilidad()
        }

    '''La siguiente funcion, muestra info especifica del cliente en la vista de detalle'''
    def serializeInfo(self):
        return {
        "id": self.id,
        "razon": self.razon,
        "rut": self.rut,
        "vigente": self.vigente,
        "correo": self.correo,
        "correoSecundario": self.correoSecundario,
        "correoTerciario": self.correoTerciario,
        "fono": self.fono,
        "whatsapp": self.whatsapp,
        "erpyme": self.erpyme,
        "dicom": self.dicom,
        "repetido": self.repetido,
        "libre": self.libre
    }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def get_pagosContabilidad(self):
        pagos = list(map(lambda pago: pago.serialize(),
                     self.pagosContabilidadID))  # Revisar aqui, es probable que tenga malo el lambda.
        return pagos

    def get_notasContabilidad(self):
        notas = list(map(lambda nota: nota.serialize(),
                         self.notasContabilidadID))  # Revisar aqui, es probable que tenga malo el lambda.
        return notas


class PagosContabilidad(db.Model):
    __tablename__ = 'pagosContabilidad'
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.String(10), nullable=False)
    mes = db.Column(db.String(10), nullable=False)
    numeroTransferencia = db.Column(db.String(100), nullable=True)
    montoPagado = db.Column(db.String(50), nullable=True)
    montoCobrado = db.Column(db.String(100), nullable=False, default="9900")
    facturaNumero = db.Column(db.String(30), nullable=True)
    comentario = db.Column(db.String(100), nullable=True)
    clienteContabilidadid = db.Column(db.Integer, db.ForeignKey(
        'clientesContabilidad.id', ondelete='CASCADE'))

    def serialize(self):
        return {
            "id": self.id,
            "year": self.year,
            "mes": self.mes,
            "numeroTransferencia": self.numeroTransferencia,
            "montoPagado": self.montoPagado,
            "montoCobrado": self.montoCobrado,
            "facturaNumero": self.facturaNumero,
            "comentario": self.comentario,
            "clienteContabilidadid": self.clienteContabilidadid
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class NotaContabilidad(db.Model):
    __tablename__ = 'notasContabilidad'
    id = db.Column(db.Integer, primary_key=True)
    comentario = db.Column(db.String(500), nullable=False)
    fechaComentario = db.Column(db.String(20), nullable=False)
    clienteContabilidadid = db.Column(db.Integer, db.ForeignKey(
        'clientesContabilidad.id', ondelete='CASCADE'))

    def serialize(self):
        return {
            "id": self.id,
            "comentario": self.comentario,
            "fechaComentario": self.fechaComentario,
            "clienteContabilidadid": self.clienteContabilidadid
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

