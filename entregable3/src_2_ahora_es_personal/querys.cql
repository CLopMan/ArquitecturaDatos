// Query sacar las sanciones en stand by, funciona, tabla de cassandra no necesaria
select * from sanciones where estado = 'stand by' ALLOW FILTERING;

// Query 1.1: Funciona
SELECT marca, modelo, COUNT(*) as total_multas FROM multas_marca_modelo GROUP BY marca, modelo;

// Query 1.2: Funciona, pero no ordena
SELECT color, COUNT(*) as total_multas from multas_color_coche GROUP BY color;

// Query 1.3: Funciona
SELECT marca, modelo, COUNT(*) as total_multas FROM multas_marca_modelo WHERE tipo = 'velocidad' GROUP BY marca, modelo;

// Query 2.1 
SELECT carretera, kilometro, sentido, COUNT(*) as infracciones_tramo FROM conflictos_tramo_sentido GROUP BY carretera, kilometro, sentido;
