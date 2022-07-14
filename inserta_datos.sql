-- Inserta un registro en la tabla
--INSERT INTO movimiento (id, id_cuenta, tipo, importe, tipo)
--VALUES(4, 1, 1, 150.0, ' ' )

INSERT INTO cuenta (id, id_cliente)
VALUES(3, 2)

--INSERT INTO categoria_cliente (id, id_categoria, id_cliente)
--VALUES(2, 2, 1)



--INSERT INTO categoria (id, nombre)
--VALUES(2, "basic")

--SELECT
--	tipo,
--	SUM(importe) AS saldo
--FROM movimiento
--WHERE id_cuenta = 1
--GROUP BY tipo;