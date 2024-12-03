drop keyspace practica2;

CREATE KEYSPACE practica2
with replication = {
    'class': 'SimpleStrategy',
    'replication_factor': 1
};

use practica2;
CREATE TABLE sanciones (
    dni_deudor text,
    fecha_grabacion date,
    estado text,
    matricula text,
    cantidad int,
    tipo text,
    PRIMARY KEY ((dni_deudor), tipo, fecha_grabacion)
);


CREATE TABLE sanciones_en_proceso (
    dni_deudor text,
    tipo text,
    fecha_grabacion date, 
    PRIMARY KEY ((dni_deudor), tipo, fecha_grabacion)
);

CREATE TABLE conductores_mas_infractores (
    dni_deudor text,
    num_multas int,
    PRIMARY KEY (dni_deudor, num_multas)
);

CREATE TABLE multas_marca_modelo (
    marca text,
    modelo text,
    num_multas int,
    PRIMARY KEY ((marca, modelo), num_multas)
);

CREATE TABLE multas_color_coche (
    color text,
    num_multas int,
    PRIMARY KEY (color, num_multas)
);

CREATE TABLE velocidad_marca_modelo (
    marca text,
    modelo text,
    num_multas int,
    PRIMARY KEY ((marca, modelo), num_multas)
);

CREATE TABLE conflictos_tramo_sentido (
    carretera text,
    kilometro int,
    sentido text,
    mayor_numero_infracciones_carretera int,
    PRIMARY KEY ((carretera), mayor_numero_infracciones_carretera)
);

CREATE TABLE exceso_velocidad_carretera (
    carretera text,
    exceso_velocidad_media float,
    PRIMARY KEY (carretera)
);
