// Query sacar las sanciones en stand by, funciona, tabla de cassandra no necesaria
select * from sanciones where estado = 'stand by' ALLOW FILTERING;

// Query 1.1: Funciona
SELECT marca, modelo, SUM(num_multas) AS total_multas FROM multas_marca_modelo WHERE marca = 'Toyota' AND modelo = 'Corolla';

// Query 1.2: Funciona, pero no ordena
SELECT color, SUM(num_multas) from multas_color_coche GROUP BY color;

// Query 1.3: Funciona
SELECT marca, modelo, SUM(num_multas) AS total_multas FROM velocidad_marca_modelo GROUP BY marca, modelo;
