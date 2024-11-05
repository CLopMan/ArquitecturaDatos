mongosh < ./borrar_datos.js

mongoimport --db entregable2_old --collection areas --type csv --file ../output/areas_limpias.csv --headerline 
mongoimport --db entregable2_old --collection juegos --type csv --file ../output/juegos_limpio.csv --headerline
mongoimport --db entregable2_old --collection encuestas_satisfaccion --type csv --file ../output/encuestas_satisfaccion_limpio.csv --headerline
mongoimport --db entregable2_old --collection estaciones_meteo_codigo_postal --type csv --file ../output/estaciones_meteo_codigo_postal.csv --headerline
mongoimport --db entregable2_old --collection incidencias_usuarios --type csv --file ../output/incidencias_usuarios_limpio.csv --headerline
mongoimport --db entregable2_old --collection incidentes_seguridad --type csv --file ../output/incidentes_seguridad_limpio.csv --headerline
mongoimport --db entregable2_old --collection mantenimiento --type csv --file ../output/mantenimiento_limpio.csv --headerline
mongoimport --db entregable2_old --collection meteo24 --type csv --file ../output/meteo24_limpio.csv --headerline
mongoimport --db entregable2_old --collection usuarios --type csv --file ../output/usuarios_limpios.csv --headerline

mongosh < ./preprocesado.js
