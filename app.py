import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.params import Depends
from starlette.responses import RedirectResponse
from sqlalchemy.orm import Session
from typing import List

import sql.models as models
import sql.schemas as schemas
from config.db import engine, get_db
from sql.repositories import ClienteRepo, MovimientoRepo, CategoriaClienteRepo, CuentaRepo, CategoriaRepo

models.Base.metadata.create_all(bind=engine)
app = FastAPI()



@app.get("/")
def main():
    return RedirectResponse(url="/docs/")


#  Lista todos los clientes.
@app.get('/clientes', response_model=List[schemas.Cliente])
def get_clientes(db: Session = Depends(get_db)):

    clientes = ClienteRepo.find_all(db)
    if clientes:
        return clientes
    raise HTTPException(status_code=400, detail="Ningun cliente fue encontrado")


# Registra un cliente
@app.post('/cliente', response_model=schemas.Cliente)
def add_clientes(cliente_request: schemas.ClienteCreate, db: Session = Depends(get_db)):

    db_cliente = ClienteRepo.find_by_name(db, nombre= cliente_request.nombre)
    if db_cliente:
        raise HTTPException(status_code=400, detail="El cliente ya existe")
    else:
        return ClienteRepo.create(db, cliente= cliente_request)


# Edita un cliente
@app.put('/cliente/{cliente_id}', response_model=schemas.Cliente)
def update_clientes(cliente_id: int, cliente_request: schemas.Cliente, db: Session = Depends(get_db)):

    db_cliente = ClienteRepo.find_by_id(db, cliente_id)
    if db_cliente:
        update_cliente_encoded = jsonable_encoder(cliente_request)
        db_cliente.nombre = update_cliente_encoded['nombre']

        return ClienteRepo.update(db, db_cliente)
    else:
        raise HTTPException(status_code=400, detail="El ID de cliente dado no fue encontrado")


# Elimina un cliente
@app.delete('/cliente/{cliente_id}')
def add_clientes(cliente_id: int, db: Session = Depends(get_db)):

    db_cliente = ClienteRepo.find_by_id(db, cliente_id)
    if db_cliente is None:
        raise HTTPException(status_code=404, detail="El ID de cliente  no fue encontrado")

    ClienteRepo.delete(db, cliente_id)
    return "Cliente borrado"


# Consulta un movimiento
@app.get('/movimiento/{mov_id}', response_model=schemas.Movimiento)
def get_movimiento(mov_id: int, db: Session = Depends(get_db)):

    movimiento = MovimientoRepo.find_by_id(db, mov_id)
    if movimiento:
        return movimiento
    raise HTTPException(status_code=400, detail="El ID de movimiento no fue encontrado")


# Registra un movimiento.
@app.post('/movimiento', response_model=schemas.Movimiento)
def add_movimiento(mov_request: schemas.MovimientoCreate, db: Session = Depends(get_db)):

    mov_encoded = jsonable_encoder(mov_request)
    # Si es un egreso, consulta el saldo disponible.
    if not mov_encoded['tipo']:
        saldo_dispo = MovimientoRepo.get_saldo(db, mov_encoded['id_cuenta'])

        if mov_encoded['importe'] <= saldo_dispo:
            return MovimientoRepo.create(db, movimiento=mov_request)
        else:
            raise HTTPException(status_code=400, detail="Saldo insuficiente")

    return MovimientoRepo.create(db, movimiento=mov_request)


# Elimina un movimiento.
@app.delete('/movimiento/{mov_id}')
def add_movimiento(mov_id: int, db: Session = Depends(get_db)):

    db_movimiento = MovimientoRepo.find_by_id(db, mov_id)
    if db_movimiento is None:
        raise HTTPException(status_code=404, detail="El ID de movimiento no fue encontrado")

    MovimientoRepo.delete(db, mov_id)
    return "Movimiento borrado"


# Agrega un cliente a categoria
@app.post('/categoria_cliente', response_model=schemas.CategoriaCliente)
def add_cliente_categoria(cat_request: schemas.CategoriaClienteCreate, db: Session = Depends(get_db)):

    categoria = CategoriaRepo.find_by_id(db, cat_request.id_categoria)
    cliente = ClienteRepo.find_by_id(db, cat_request.id_cliente)

    if categoria and cliente:
        return CategoriaClienteRepo.create(db, categoria_cliente=cat_request)
    raise HTTPException(status_code=404, detail="ID de cliente o categoria no encontrado")


# Consulta el saldo disponible en todas las cuentas del cliente.
@app.get('/saldo/{id_cliente}')
def get_saldo(id_cliente: int, db: Session = Depends(get_db)):

    cuentas_cliente = CuentaRepo.find_by_id_cliente(db, id_cliente)
    result = []
    usd_bolsa = CuentaRepo.get_usd()

    if cuentas_cliente:
        for id_cuenta in cuentas_cliente:
            saldo_cuenta = MovimientoRepo.get_saldo(db, id_cuenta.id)

            try:
                saldo_usd = saldo_cuenta/usd_bolsa
            except ZeroDivisionError:
                return {'message:': 'precio de usd cero'}

            dic = {'cuenta': id_cuenta.id, 'saldo': saldo_cuenta, 'saldo_em_usd': saldo_usd}
            result.append(dic)

        return result
    raise HTTPException(status_code=404, detail="ID de cliente no encontrado")


# Consulta un cliente, sus cuentas y categorias.
@app.get('/info_cliente/{id_cliente}')
def get_info_cliente(id_cliente: int, db: Session = Depends(get_db)):

    categorias = CategoriaClienteRepo.find_by_id(db, id_cliente)
    resul_categorias = []
    cuentas = CuentaRepo.find_by_id_cliente(db, id_cliente)
    resul_cuentas = []

    if categorias and cuentas:
        for id_cat in categorias:
            nombre_cat = CategoriaRepo.get_all_name_cat(db, id_cat.id_categoria)
            resul_categorias.append(nombre_cat[0].nombre)

        for id_cuentas in cuentas:
            resul_cuentas.append(id_cuentas.id)

        return {'Cliente': id_cliente, 'Categorias': resul_categorias, 'Cuentas': resul_cuentas }
    raise HTTPException(status_code=404, detail="El cliente ingresdo no tiene una cuenta o categoria asociada")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)