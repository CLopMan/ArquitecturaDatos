drop keyspace practica2;

CREATE KEYSPACE practica2
with replication = {
    'class': 'SimpleStrategy',
    'replication_factor': 1
};

use practica2;

// Tabla general
CREATE TABLE sanciones (
    dni_deudor text,
    dni_propietario text,
    dni_conductor text,
    fecha_grabacion timestamp,
    estado text,
    matricula text,
    cantidad int,
    tipo text,
    PRIMARY KEY ((dni_deudor), tipo, fecha_grabacion)
);

// Caso de uso 1
CREATE TABLE multas_marca_modelo (
    marca text,
    modelo text,
    matricula text,
    fecha_grabacion timestamp,
    tipo text,
    PRIMARY KEY ((marca, modelo), matricula, fecha_grabacion)
);

CREATE TABLE multas_color_coche (
    color text,
    matricula text,
    fecha_grabacion timestamp,
    PRIMARY KEY (color, matricula, fecha_grabacion)
);

// Caso de uso 2
CREATE TABLE conflictos_tramo_sentido (
    carretera text,
    kilometro int,
    sentido text,
    fecha_grabacion timestamp,
    PRIMARY KEY ((carretera, kilometro, sentido), fecha_grabacion)
);
    
CREATE TABLE exceso_velocidad_carretera (
    carretera text,
    velocidad_registrada int,
    velocidad_limite_radar int,
    fecha_grabacion timestamp,
    PRIMARY KEY (carretera, fecha_grabacion)
);

// Caso de uso 3
CREATE TABLE probabilidad_infraccion (
    matricula text,
    fecha_grabacion timestamp,
    conductor_igual_propietario boolean,
    PRIMARY KEY (conductor_igual_propietario, matricula, fecha_grabacion)
);
