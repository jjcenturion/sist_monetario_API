import requests
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from . import models, schemas


class ClienteRepo:

    def create(db: Session, cliente: schemas.ClienteCreate):
        db_cliente = models.Cliente(nombre=cliente.nombre)
        db.add(db_cliente)
        db.commit()
        db.refresh(db_cliente)
        return db_cliente

    def find_by_id(db: Session, _id):
        return db.query(models.Cliente).filter(models.Cliente.id == _id).first()

    def find_by_name(db: Session, nombre):
        return db.query(models.Cliente).filter(models.Cliente.nombre == nombre).first()

    def find_all(db: Session, skip: int = 0, limit: int = 100):
        return db.query(models.Cliente).offset(skip).limit(limit).all()

    def delete(db: Session, cliente_id):
        db_cliente = db.query(models.Cliente).filter_by(id=cliente_id).first()
        db.delete(db_cliente)
        db.commit()

    def update(db: Session, cliente_data):
        updated_cliente = db.merge(cliente_data)
        db.commit()
        return updated_cliente


class CuentaRepo:

    def find_by_id_cliente(db: Session, id_cliente):
        return db.query(models.Cuenta).filter(models.Cuenta.id_cliente == id_cliente).all()

    def get_usd():

        ENDPOINT = "https://www.dolarsi.com/api/api.php?type=valoresprincipales"

        try:
            r = requests.get(ENDPOINT)
            response = r.json()
        except requests.exceptions.HTTPError as err:
            return {'message': 'Http Error'}
        except requests.exceptions.ConnectionError as errc:
            return {'message': 'Http ConnectionError'}
        except requests.exceptions.Timeout as errt:
            return {'message': 'Http Timeout'}

        venta_usd_bolsa = response[4]['casa']['venta']
        usd_f = float(venta_usd_bolsa.replace('.','').replace(',','.'))
        return usd_f


class MovimientoRepo:

    def create(db: Session, movimiento: schemas.MovimientoCreate):
        db_movimiento = models.Movimiento(id_cuenta=movimiento.id_cuenta, tipo=movimiento.tipo, importe=movimiento.importe, fecha=movimiento.fecha)
        db.add(db_movimiento)
        db.commit()
        db.refresh(db_movimiento)

        return db_movimiento

    def find_by_id(db: Session, _id):
        r = db.query(models.Movimiento).filter(models.Movimiento.id == _id).first()
        return r

    def delete(db: Session, mov_id):
        db_movimiento = db.query(models.Movimiento).filter_by(id=mov_id).first()
        db.delete(db_movimiento)
        db.commit()

    def get_saldo(db: Session, id_cuenta):

        r = db.query(models.Movimiento.tipo, func.sum(models.Movimiento.importe).label('Ingreso')).filter(models.Movimiento.id_cuenta==id_cuenta).group_by(models.Movimiento.tipo)
        resul = r.all()

        if not resul:
            saldo = 0.0  # la cuenta todavia no tiene movimientos
            return saldo

        if len(resul) == 1:       # solo existe un ingreso o egreso para ese id de cuenta.
            if resul[0][0]:
                return resul[0][1]  # es un ingreso por tanto positivo
            else:
                return - resul[0][1]

        return resul[1][1] - resul[0][1]


class CategoriaClienteRepo:

    def create(db: Session, categoria_cliente: schemas.CategoriaClienteCreate):
        db_cat_cliente = models.CategoriaCliente(id_categoria=categoria_cliente.id_categoria, id_cliente=categoria_cliente.id_cliente)
        db.add(db_cat_cliente)
        db.commit()
        db.refresh(db_cat_cliente)

        return db_cat_cliente

    def find_by_id(db: Session, _id):
        return db.query(models.CategoriaCliente).filter(models.CategoriaCliente.id_cliente == _id).all()


class CategoriaRepo:

    def find_by_id(db: Session, _id):
        return db.query(models.Categoria).filter(models.Categoria.id == _id).first()

    def get_all_name_cat(db: Session, _id):
        return db.query(models.Categoria).filter(models.Categoria.id == _id).all()