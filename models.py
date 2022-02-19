from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(100), nullable=False, unique=True)
    clave = db.Column(db.String(20), nullable=False)
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


class ClienteDt(db.Model):
    __tablename__ = 'clientesDt'
    id = db.Column(db.Integer, primary_key=True)
    razon = db.Column(db.String(100), nullable=False)
    rut = db.Column(db.String(100), nullable=False)
    vigente = db.Column(db.String(100), nullable=True, default="true")
    correo = db.Column(db.String(100), nullable=False)
    correoSecundario = db.Column(db.String(100), nullable=True)
    correoTerciario = db.Column(db.String(100), nullable=True)
    fono = db.Column(db.String(100), nullable=True)
    whatsapp = db.Column(db.String(100), nullable=True)
    representante = db.Column(db.String(100), nullable=False)
    rutRepresentante = db.Column(db.String(100), nullable=False)
    fechaContratacion = db.Column(db.String(100), nullable=False)
    erpyme = db.Column(db.String(100), nullable=True, default="false")
    p = db.Column(db.String(5), nullable=True, default="")
    sacar = db.Column(db.String(5), nullable=True, default="")
    dicom = db.Column(db.String(5), nullable=True, default="")
    repetido = db.Column(db.String(10), nullable=True, default="")
    libre = db.Column(db.String(100), nullable=True, default="")
    mesesPagados = db.Column(db.String(20), nullable=True, default="")
    tipoPago = db.Column(db.String(10), nullable=True, default="mensual")
    dt2019ID = db.relationship(
        'Dt2019', cascade='all, delete', backref='clientesDt2019')
    dt2020ID = db.relationship(
        'Dt2020', cascade='all, delete', backref='clientesDt2020')
    dt2021ID = db.relationship(
        'Dt2021', cascade='all, delete', backref='clientesDt2021')
    dt2022ID = db.relationship(
        'Dt2022', cascade='all, delete', backref='clientesDt2022')
    dt2023ID = db.relationship(
        'Dt2023', cascade='all, delete', backref='clientesDt2023')
    dt2024ID = db.relationship(
        'Dt2024', cascade='all, delete', backref='clientesDt2024')
    notasID = db.relationship(
        'Nota', cascade='all, delete', backref='clientesDtNotas')

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
            "representante": self.representante,
            "rutRepresentante": self.rutRepresentante,
            "fechaContratacion": self.fechaContratacion,
            "erpyme": self.erpyme,
            "p": self.p,
            "sacar": self.sacar,
            "dicom": self.dicom,
            "repetido": self.repetido,
            "libre": self.libre,
            "mesesPagados": self.mesesPagados,
            "tipoPago": self.tipoPago,
            "dt2019ID": self.get_dt2019(),
            "dt2020ID": self.get_dt2020(),
            "dt2021ID": self.get_dt2021(),
            "dt2022ID": self.get_dt2022(),
            "dt2023ID": self.get_dt2023(),
            "dt2024ID": self.get_dt2024(),
            "notas": self.get_notas()
        }
    
    ''' Con la siguiente funcion, se hace el filtro en la vista ampliada '''
    def serializeX(self):  
        return {
        "id": self.id,
        "razon": self.razon,
        "rut": self.rut,
        "vigente": self.vigente,
        "correo": self.correo,
        "correoSecundario": self.correoSecundario,
        "correoTerciario": self.correoTerciario,
        "fono": self.fono,
        "fechaContratacion": self.fechaContratacion,
        "p": self.p,
        "libre": self.libre,
        "mesesPagados": self.mesesPagados,
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
        "representante": self.representante,
        "rutRepresentante": self.rutRepresentante,
        "fechaContratacion": self.fechaContratacion,
        "erpyme": self.erpyme,
        "p": self.p,
        "sacar": self.sacar,
        "dicom": self.dicom,
        "repetido": self.repetido,
        "libre": self.libre,
        "mesesPagados": self.mesesPagados,
        "tipoPago": self.tipoPago
    }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def get_dt2019(self):
        pagos = list(map(lambda pago: pago.serialize(),
                     self.dt2019ID))  # Revisar aqui, es probable que tenga malo el lambda.
        return pagos

    def get_dt2020(self):
        pagos = list(map(lambda pago: pago.serialize(),
                     self.dt2020ID))  # Revisar aqui, es probable que tenga malo el lambda.
        return pagos

    def get_dt2021(self):
        pagos = list(map(lambda pago: pago.serialize(),
                     self.dt2021ID))  # Revisar aqui, es probable que tenga malo el lambda.
        return pagos

    def get_dt2022(self):
        pagos = list(map(lambda pago: pago.serialize(),
                     self.dt2022ID))  # Revisar aqui, es probable que tenga malo el lambda.
        return pagos

    def get_dt2023(self):
        pagos = list(map(lambda pago: pago.serialize(),
                     self.dt2023ID))  # Revisar aqui, es probable que tenga malo el lambda.
        return pagos

    def get_dt2024(self):
        pagos = list(map(lambda pago: pago.serialize(),
                     self.dt2024ID))  # Revisar aqui, es probable que tenga malo el lambda.
        return pagos

    def get_notas(self):
        notas = list(map(lambda nota: nota.serialize(),
                         self.notasID))  # Revisar aqui, es probable que tenga malo el lambda.
        return notas


class Dt2019(db.Model):
    __tablename__ = 'dt2019s'
    id = db.Column(db.Integer, primary_key=True)
    mes = db.Column(db.String(100), nullable=False)
    numeroTransferencia = db.Column(db.String(100), nullable=True)
    montoPagado = db.Column(db.String(100), nullable=True)
    montoCobrado = db.Column(db.String(100), nullable=False, default="9900")
    mesesPagados = db.Column(db.String(20), nullable=False, default="1")
    facturaNumero = db.Column(db.String(100), nullable=True)
    comentario = db.Column(db.String(100), nullable=True)
    fechaIngresoPago = db.Column(db.String(100), nullable=True)
    clienteDtid = db.Column(db.Integer, db.ForeignKey(
        'clientesDt.id', ondelete='CASCADE'))

    def serialize(self):
        return {
            "id": self.id,
            "mes": self.mes,
            "numeroTransferencia": self.numeroTransferencia,
            "montoPagado": self.montoPagado,
            "montoCobrado": self.montoCobrado,
            "mesesPagados":self.mesesPagados,
            "facturaNumero": self.facturaNumero,
            "comentario": self.comentario,
            "fechaIngresoPago": self.fechaIngresoPago,
            "clienteDtid": self.clienteDtid
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Dt2020(db.Model):
    __tablename__ = 'dt2020s'
    id = db.Column(db.Integer, primary_key=True)
    mes = db.Column(db.String(100), nullable=False)
    numeroTransferencia = db.Column(db.String(100), nullable=True)
    montoPagado = db.Column(db.String(100), nullable=True)
    montoCobrado = db.Column(db.String(100), nullable=False, default="9900")
    mesesPagados = db.Column(db.String(20), nullable=False, default="1")
    facturaNumero = db.Column(db.String(100), nullable=True)
    comentario = db.Column(db.String(100), nullable=True)
    fechaIngresoPago = db.Column(db.String(100), nullable=True)
    clienteDtid = db.Column(db.Integer, db.ForeignKey(
        'clientesDt.id', ondelete='CASCADE'))

    def serialize(self):
        return {
            "id": self.id,
            "mes": self.mes,
            "numeroTransferencia": self.numeroTransferencia,
            "montoPagado": self.montoPagado,
            "montoCobrado": self.montoCobrado,
            "mesesPagados":self.mesesPagados,
            "facturaNumero": self.facturaNumero,
            "comentario": self.comentario,
            "fechaIngresoPago": self.fechaIngresoPago,
            "clienteDtid": self.clienteDtid
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Dt2021(db.Model):
    __tablename__ = 'dt2021s'
    id = db.Column(db.Integer, primary_key=True)
    mes = db.Column(db.String(100), nullable=False)
    numeroTransferencia = db.Column(db.String(100), nullable=True)
    montoPagado = db.Column(db.String(100), nullable=True)
    montoCobrado = db.Column(db.String(100), nullable=False, default="9900")
    mesesPagados = db.Column(db.String(20), nullable=False, default="1")
    facturaNumero = db.Column(db.String(100), nullable=True)
    comentario = db.Column(db.String(100), nullable=True)
    fechaIngresoPago = db.Column(db.String(100), nullable=True)
    clienteDtid = db.Column(db.Integer, db.ForeignKey(
        'clientesDt.id', ondelete='CASCADE'))

    def serialize(self):
        return {
            "id": self.id,
            "mes": self.mes,
            "numeroTransferencia": self.numeroTransferencia,
            "montoPagado": self.montoPagado,
            "montoCobrado": self.montoCobrado,
            "mesesPagados":self.mesesPagados,
            "facturaNumero": self.facturaNumero,
            "comentario": self.comentario,
            "fechaIngresoPago": self.fechaIngresoPago,
            "clienteDtid": self.clienteDtid
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Dt2022(db.Model):
    __tablename__ = 'dt2022s'
    id = db.Column(db.Integer, primary_key=True)
    mes = db.Column(db.String(100), nullable=False)
    numeroTransferencia = db.Column(db.String(100), nullable=True)
    montoPagado = db.Column(db.String(100), nullable=True)
    montoCobrado = db.Column(db.String(100), nullable=False, default="9900")
    mesesPagados = db.Column(db.String(20), nullable=False, default="1")
    facturaNumero = db.Column(db.String(100), nullable=True)
    comentario = db.Column(db.String(100), nullable=True)
    fechaIngresoPago = db.Column(db.String(100), nullable=True)
    clienteDtid = db.Column(db.Integer, db.ForeignKey(
        'clientesDt.id', ondelete='CASCADE'))

    def serialize(self):
        return {
            "id": self.id,
            "mes": self.mes,
            "numeroTransferencia": self.numeroTransferencia,
            "montoPagado": self.montoPagado,
            "montoCobrado": self.montoCobrado,
            "mesesPagados":self.mesesPagados,
            "facturaNumero": self.facturaNumero,
            "comentario": self.comentario,
            "fechaIngresoPago": self.fechaIngresoPago,
            "clienteDtid": self.clienteDtid
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Dt2023(db.Model):
    __tablename__ = 'dt2023s'
    id = db.Column(db.Integer, primary_key=True)
    mes = db.Column(db.String(100), nullable=False)
    numeroTransferencia = db.Column(db.String(100), nullable=True)
    montoPagado = db.Column(db.String(100), nullable=True)
    montoCobrado = db.Column(db.String(100), nullable=False, default="9900")
    mesesPagados = db.Column(db.String(20), nullable=False, default="1")
    facturaNumero = db.Column(db.String(100), nullable=True)
    comentario = db.Column(db.String(100), nullable=True)
    fechaIngresoPago = db.Column(db.String(100), nullable=True)
    clienteDtid = db.Column(db.Integer, db.ForeignKey(
        'clientesDt.id', ondelete='CASCADE'))

    def serialize(self):
        return {
            "id": self.id,
            "mes": self.mes,
            "numeroTransferencia": self.numeroTransferencia,
            "montoPagado": self.montoPagado,
            "montoCobrado": self.montoCobrado,
            "mesesPagados":self.mesesPagados,
            "facturaNumero": self.facturaNumero,
            "comentario": self.comentario,
            "fechaIngresoPago": self.fechaIngresoPago,
            "clienteDtid": self.clienteDtid
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Dt2024(db.Model):
    __tablename__ = 'dt2024s'
    id = db.Column(db.Integer, primary_key=True)
    mes = db.Column(db.String(100), nullable=False)
    numeroTransferencia = db.Column(db.String(100), nullable=True)
    montoPagado = db.Column(db.String(100), nullable=True)
    montoCobrado = db.Column(db.String(100), nullable=False, default="9900")
    mesesPagados = db.Column(db.String(20), nullable=False, default="1")
    facturaNumero = db.Column(db.String(100), nullable=True)
    comentario = db.Column(db.String(100), nullable=True)
    fechaIngresoPago = db.Column(db.String(100), nullable=True)
    clienteDtid = db.Column(db.Integer, db.ForeignKey(
        'clientesDt.id', ondelete='CASCADE'))

    def serialize(self):
        return {
            "id": self.id,
            "mes": self.mes,
            "numeroTransferencia": self.numeroTransferencia,
            "montoPagado": self.montoPagado,
            "montoCobrado": self.montoCobrado,
            "mesesPagados":self.mesesPagados,
            "facturaNumero": self.facturaNumero,
            "comentario": self.comentario,
            "fechaIngresoPago": self.fechaIngresoPago,
            "clienteDtid": self.clienteDtid
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Nota(db.Model):
    __tablename__ = 'notas'
    id = db.Column(db.Integer, primary_key=True)
    comentario = db.Column(db.String(500), nullable=False)
    fechaComentario = db.Column(db.String(500), nullable=False)
    clienteDtid = db.Column(db.Integer, db.ForeignKey(
        'clientesDt.id', ondelete='CASCADE'))

    def serialize(self):
        return {
            "id": self.id,
            "comentario": self.comentario,
            "fechaComentario": self.fechaComentario,
            "clienteDtid": self.clienteDtid
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
