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
    DNI text,
    Tipo text,
    Fecha date, 
    PRIMARY KEY ((DNI), Tipo, Fecha)
);

CREATE TABLE concutores_mas_infractores (
    DNI text,
    Suma_infracciones int,
    PRIMARY KEY (DNI, Suma_infracciones)
);

CREATE TABLE multas_marca_modelo (
    Marca text,
    Modelo text,
    Multas int,
    PRIMARY KEY ((Marca, Modelo), Multas)
);

CREATE TABLE multas_color_coche (
    Color text,
    Multas int,
    PRIMARY KEY (Color, Multas)
);

CREATE TABLE velocidad_marca_modelo (
    Marca text,
    Modelo text,
    Multas int,
    PRIMARY KEY ((Marca, Modelo), Multas)
);

CREATE TABLE conflictos_tramo_sentido (
    Carretera text,
    Kilometro int,
    Sentido text,
    Infracciones int,
    PRIMARY KEY (Carretera, Infracciones)
);

CREATE TABLE exceso_velocidad_carretera (
    Carretera text,
    Exceso_velocidad float,
    PRIMARY KEY (Carretera)
);
