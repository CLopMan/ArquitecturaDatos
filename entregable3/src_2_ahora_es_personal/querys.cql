SELECT marca, modelo, SUM(num_multas) AS total_multas
FROM multas_por_marca_modelo
WHERE marca = 'Toyota' AND modelo = 'Corolla';

SELECT color, SUM(num_multas) AS total_multas
FROM multas_color_coche
WHERE marca = 'Toyota' AND modelo = 'Corolla';

SELECT marca, modelo, SUM(num_multas) AS total_multas
FROM velocidad_marca_modelo
WHERE marca = 'Toyota' AND modelo = 'Corolla';

