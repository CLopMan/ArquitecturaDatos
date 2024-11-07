use entregable2_old;
// crear esquema de validacion
db.runCommand({collMod: "areas", 
    validator: {
        $jsonSchema: {
            bsonType: "object",
            title: "Areas Validator",
            required: ["_id", "DESC_CLASIFICACION", "COD_BARRIO", "BARRIO", "COD_DISTRITO", "DISTRITO", "ESTADO", "COORD_GIS_X", "COORD_GIS_Y", "LATITUD", "LONGITUD", "TIPO_VIA", "NOM_VIA", "NUM_VIA", "COD_POSTAL", "FECHA_INSTALACION"],
            properties: {
                _id: {
                    bsonType: "string",
                    description: "id del área"
                },
                DESC_CLASIFICACION: {
                    bsonType: "string",
                    enum: ["AREA DE JUEGO/ESPECIAL", "AREA DE MAYORES", "AREA INFANTIL", "CIRCUITO DEPORTIVO ELEMENTAL"],
                    description: "descripción del tipo de área recreativa"
                },
                COD_BARRIO: {
                    bsonType: "int",
                    description: "código del barrio al que pertenece el área"
                },
                BARRIO: {
                    bsonType: "string",
                    description: "barrio al que pertenece el área"
                },
                COD_DISTRITO: {
                    bsonType: "int",
                    description: "código del distrito al que pertenece el área"
                },
                DISTRITO: {
                    bsonType: "string",
                    description: "distrito al que pertenece el área"
                },
                ESTADO: {
                    bsonType: "string",
                    enum: ["OPERATIVO"],
                    description: "estado del área"
                },
                COORD_GIS_X: {
                    bsonType: "number",
                    description: "coordenadas en el eje X del área"
                },
                COORD_GIS_Y: {
                    bsonType: "number",
                    description: "coordenadas en el eje Y del área"
                },
                LATITUD: {
                    bsonType: "string",
                    description: "latitud del área"
                },
                LONGITUD: {
                    bsonType: "string",
                    description: "longitud del área"
                },
                TIPO_VIA: {
                    bsonType: "string",
                    description: "tipo del vía donde se encuentra el área"
                },
                NOM_VIA: {
                    bsonType: "string",
                    description: "nombre de la vía donde se encuentra el área"
                },
                NUM_VIA: {
                    bsonType: "string",
                    description: "número de la vía donde se encuentra el área"
                },
                COD_POSTAL: {
                    bsonType: "int",
                    description: "código postal de la zona postal en la que se encuentra el área"
                },
                FECHA_INSTALACION: {
                    bsonType: "date",
                    description: "fecha en la que se instaló el área"
                },
                TOTAL_ELEM: {
                    bsonType: "int",
                    description: "número de juegos"
                },
                tipo: {
                    bsonType: "string",
                    description: "tipo de área"
                }
            }
        }
    }
});

db.runCommand({collMod: "encuestas_satisfaccion", 
    validator: {
        $jsonSchema: {
            bsonType: "object",
            title: "encuestas_satisfaction_validation",
            required: ["_id", "PUNTUACION_ACCESIBILIDAD", "PUNTUACION_CALIDAD", "COMENTARIOS", "FECHA", "AreaRecreativaID"],
            properties: {
                _id: {
                    bsonType: "string",
                    description: "identificador de la encuesta"
                },
                PUNTUACION_ACCESIBILIDAD: {
                    bsonType: "int",
                    description: "puntuación de la accesibilidad del area asociada a la encuesta"
                },
                PUNTACION_CALIDAD: {
                    bsonType: "int",
                    description: "puntuación de la calidad del area asociada a la encuesta"
                },
                COMENTARIOS: {
                    bsonType: "string",
                    description: "comentarios adicionales de los usuarios"
                },
                FECHA: {
                    bsonType: "date",
                    description: "fecha de realización de la encuesta"
                },
                AeraRecreativaID: {
                    bsonType: "int",
                    description: "identificador del área recreativa evaluada"
                }
            }
        }
    }
});

db.runCommand({collMod: "incidentes_seguridad", 
    validator: {
        $jsonSchema: {
            bsonType: "object",
            title: "Incidencias Seguridad Validator",
            required: [
                "ID",
                "FECHA_REPORTE",
                "TIPO_INCIDENTE",
                "GRAVEDAD",
                "AreaRecreativaID",
            ],
            properties: {
                ID: {
                    bsonType: "string",
                    description: "'id' es el identificador de la fila",
                },
                FECHA_REPORTE: {
                    bsonType: "date",
                    description:
                        "'fecha_reporte' corresponde con la fecha en la que se realizó el reporte",
                },
                tipo_incidente: {
                    bsonType: "string",
                    enum: [
                        "ROBO",
                        "VANDALISMO",
                        "ACCIDENTE",
                        "CAIDA",
                        "DAÑO ESTRUCTURAL"
                    ],
                    description:
                        "'tipo_incidente' corresponde con el tipo de incidente reportado",
                },
                gravedad: {
                    bsonType: "string",
                    enum: ["CRITICA", "ALTA", "MEDIA", "BAJA"],
                    description:
                        "'gravedad' corresponde con el nivel de gravedad del incidente",
                },
                AreaRecreativaID: {
                    bsonType: "string",
                    description:
                        "'area_recreativa_id' corresponde con el identificador del área a la que corresponde el reporte del incidente",
                },
            },
        },
    },
});

db.runCommand({ collMod: "incidencias_usuarios", 
    validator: {
        $jsonSchema: {
            bsonType: "object",
            title: "Incidencias Usuario Validator",
            required: [
                "_id",
                "TIPO_INCIDENCIA",
                "FECHA_REPORTE",
                "ESTADO",
                "UsuarioID",
                "MantenimientoID",
            ],
            properties: {
                _id: {
                    bsonType: "string",
                    description: "número identificativo de la columna",
                },
                TIPO_INCIDENCIA: {
                    bsonType: "string",
                    enum: ["DESGASTE", "ROTURA", "VANDALISMO", "MAL FUNCIONAMIENTO"],
                    description: "tipo de incidencia reportada",
                },
                FECHA_REPORTE: {
                    bsonType: "date",
                    description: "fecha en la que se reportó la incidencia",
                },
                ESTADO: {
                    bsonType: "string",
                    enum: ["CERRADA", "ABIERTA"],
                    description: "estado actual de la incidencia",
                },
                UsuarioID: {
                    bsonType: ["string"],
                    description: "listado de usuarios",
                },
                MantenimientoID: {
                    bsonType: ["string"],
                    description: "id de mantenimiento",
                }
            },
        },
    },
});

db.runCommand({ collMod: "juegos", 
    validator: {
        $jsonSchema: {
            bsonType: "object",
            title: "juegos Validator",
            required: ["ID", "DESC_CLASIFICACION", "COD_BARRIO", "BARRIO", "COD_DISTRITO", "DISTRITO", "ESTADO", "COORD_GIS_X", "COORD_GIS_Y", "LATITUD", "LONGITUD", "TIPO_VIA", "NOM_VIA", "NUM_VIA", "COD_POSTAL", "FECHA_INSTALACION", "MODELO", "tipo_juego", "ACCESIBLE", "AREA"],
            properties: {
                _id: {
                    bsonType: "string",
                    description: "id del juego"
                },
                DESC_CLASIFICACION: {
                    bsonType: "string",
                    enum: ["AREAS DE JUEGO/ESPECIAL", "AREAS DE MAYORES", "AREAS INFANTIL", "CIRCUITO DEPORTIVO ELEMENTAL"],
                    description: "descripción del tipo de juego recreativa"
                },
                COD_BARRIO: {
                    bsonType: "int",
                    description: "código del barrio al que pertenece el juego"
                },
                BARRIO: {
                    bsonType: "string",
                    description: "barrio al que pertenece el juego"
                },
                COD_DISTRITO: {
                    bsonType: "int",
                    description: "código del distrito al que pertenece el juego"
                },
                DISTRITO: {
                    bsonType: "string",
                    description: "distrito al que pertenece el juego"
                },
                ESTADO: {
                    bsonType: "string",
                    enum: ["OPERATIVO"],
                    description: "estado del juego"
                },
                COORD_GIS_X: {
                    bsonType: "number",
                    description: "coordenadas en el eje X del juego"
                },
                COORD_GIS_Y: {
                    bsonType: "number",
                    description: "coordenadas en el eje Y del juego"
                },
                LATITUD: {
                    bsonType: "string",
                    description: "latitud del juego"
                },
                LONGITUD: {
                    bsonType: "string",
                    description: "longitud del juego"
                },
                TIPO_VIA: {
                    bsonType: "string",
                    description: "tipo del vía donde se encuentra el juego"
                },
                NOM_VIA: {
                    bsonType: "string",
                    description: "nombre de la vía donde se encuentra el juego"
                },
                NUM_VIA: {
                    bsonType: "string",
                    description: "número de la vía donde se encuentra el juego"
                },
                COD_POSTAL: {
                    bsonType: "int",
                    description: "código postal de la zona postal en la que se encuentra el juego"
                },
                FECHA_INSTALACION: {
                    bsonType: "date",
                    description: "fecha en la que se instaló el juego"
                },
                MODELO: {
                    bsonType: "string",
                    description: "modelo de juego"
                },
                tipo_juego: {
                    bsonType: "string",
                    description: "tipo de juego"
                },
                ACCESIBLE: {
                    bsonType: "bool",
                    description: "indica si el juego es accesible"
                },
                AREA: {
                    bsonType: ["int", "string"],
                    description: "area al que pertenece el juego"
                }
            }
        }
    }
});

db.runCommand({collMod: "mantenimiento",
    validator: {
        $jsonSchema: {
            bsonType: "object",
            title: "Maintenance Validation",
            required: ["ID", "FECHA_INTERVENCION", "TIPO_INTERVENCION", "ESTADO_PREVIO", "ESTADO_POSTERIOR", "JuegoID", "Tipo", "Comentarios"],
            properties: {
                ID: {
                    bsonType: "string",
                    description: "id del mantenimiento",
                },
                FECHA_INTERVENCION: {
                    bsonType: "date",
                    description: "fecha en la que se realizaón la intervención",
                },
                TIPO_INTERVENCION: {
                    bsonType: "string",
                    enum: ["CORRECTIVO", "EMERGENCIA", "PREVENTIVO"],
                    description: "tipo de la intervención realizada"
                },
                ESTADO_PREVIO: {
                    bsonType: "string",
                    enum: ["MALO", "REGULAR", "BUENO"],
                    description: "estado previo a la revisión"
                },
                ESTADO_POSTERIOR: {
                    bsonType: "string",
                    enum: ["MALO", "REGULAR", "BUENO"],
                    description: "estado posterior a la revisión",
                },
                JuegoID: {
                    bsonType: "int",
                    description: "identificador del juego al que se le realizó el mantenimiento",
                },
                Tipo: {
                    bsonType: "string",
                    description: "tipo de mantenimiento",
                },
                Comentarios: {
                    bsonType: "string",
                    description: "comentario realizado sobre el mantimiento",
                },
            }
        }
    }
});

db.runCommand({collMod: "meteo24",
    validator: {
        $jsonSchema: {
            bsonType: "object",
            title: "meteo validator",
            required: ["FECHA", "TEMPERATURA", "PRECIPITACION", "VIENTO", "PUNTO_MUESTREO"],
            properties: {
                FECHA: {
                    bsonType: "date",
                    description: "fecha en la que se recoge el clima"
                },
                TEMPERATURA: {
                    bsonType: "number",
                    description: "temperatura"
                },
                PRECIPITACION: {
                    bsonType: "number",
                    description: "cantidad de precipitación"
                },
                VIENTO: {
                    bsonType: 'int',
                    description: "indica si ha habido vientos fuertes"
                },
                PUNTO_MUESTREO: {
                    bsonType: "int",
                    description: "area asociada"
                }
            }
        }
    }
});

db.runCommand({collMod: "usuarios",
    validator: {
        $jsonSchema: {
            bsonType: "object",
            title: "Users Validator",
            required: ["NIF", "NOMBRE", "EMAIL", "TELEFONO"],
            properties: {
                _id: {
                    bsonType: "string",
                    description: "número de identificación del usuario",
                },
                NOMBRE: {
                    bsonType: "string",
                    description: "nombre del usuario",
                },
                EMAIL: {
                    bsonType: "string",
                    description: "email del usuario",
                },
                TELEFONO: {
                    bsonType: "string",
                    description: "telefono del usuario",
                },
            },
        },
    },
});

// comprobar esquema
console.log(db.areas.validate())
console.log(db.juegos.validate())
console.log(db.encuestas_satisfaccion.validate())
console.log(db.estaciones_meteo_codigo_postal.validate())
console.log(db.incidencias_usuarios.validate())
console.log(db.incidentes_seguridad.validate())
console.log(db.mantenimiento.validate())
console.log(db.meteo24.validate())
console.log(db.usuarios.validate())