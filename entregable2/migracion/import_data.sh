mongosh < /home/lab/borrar_datos.js

mongoimport --db entregable2_old --collection areas --type csv --file areas_limpias.csv --headerline 
mongoimport --db entregable2_old --collection juegos --type csv --file juegos_limpio.csv --headerline
mongoimport --db entregable2_old --collection encuestas_satisfaccion --type csv --file encuestas_satisfaccion_limpio.csv --headerline
mongoimport --db entregable2_old --collection estaciones_meteo_codigo_postal --type csv --file estaciones_meteo_codigo_postal.csv --headerline
mongoimport --db entregable2_old --collection incidencias_usuarios --type csv --file incidencias_usuarios_limpio.csv --headerline
mongoimport --db entregable2_old --collection incidentes_seguridad --type csv --file incidentes_seguridad_limpio.csv --headerline
mongoimport --db entregable2_old --collection mantenimiento --type csv --file mantenimiento_limpio.csv --headerline
mongoimport --db entregable2_old --collection meteo24 --type csv --file meteo24_limpio.csv --headerline
mongoimport --db entregable2_old --collection usuarios --type csv --file usuarios_limpios.csv --headerline

mongosh < /home/lab/parser.js
