CREATE TABLE sanciones (
    DNI text,
    Tipo text,
    Fecha date, 
    Estado text,
    Matricula text,
    Cantidad int,
    PRIMARY KEY (DNI, (Tipo, Fecha))
);

CREATE TABLE sanciones_pagadas (
    DNI text,
    Tipo text,
    Fecha date, 
    PRIMARY KEY (DNI, (Tipo, Fecha))
);

CREATE TABLE concutores_mas_infractores (
    DNI text,
    Suma_infracciones int,
    PRIMARY KEY (DNI)
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

