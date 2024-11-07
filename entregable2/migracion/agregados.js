// --------- AGREGADO DE ÁREAS CON JUEGOS, METERO, INCIDENTES Y ENCUESTAS DE SATISFACCIÓN ---------

// Agregado de áreas con los datos agregados: estadoGlobalArea, capacidadMáxima y cantidadJuegosPorTipo
db.areas.aggregate([
    {
        // Areas con juegos
        $lookup: {
            from: 'juegos',
            localField: '_id',
            foreignField: 'AREA',
            as: 'aux_ref_juegos'
        }
    },
    // juegos por tipo:
    { $unwind: "$aux_ref_juegos" },
    {
        $group: {
            _id: { tipo: "$aux_ref_juegos.tipo_juego", area_id: "$_id" }, // agrupar areas y tipos
            count: { $sum: 1 },
            ref_juegos: { $push: { _id: "$aux_ref_juegos._id" } },
            original: { $first: "$$ROOT" }
        }
    },
    {
        $group: { // Crear para cada área un array de {tipo, count}, {tipo, count}
            _id: "$_id.area_id",
            cuenta: {
                $push: {
                    k: "$_id.tipo", v: "$count"
                }
            },
            ref_juegos: { $push: "$ref_juegos" },
            original: { $first: "$original" }
        },
    },
    {
        $addFields: {
            "cantidad_juego_por_tipo": {
                $arrayToObject: "$cuenta"

            },
            "ref_juegos": {
                $reduce: {
                    input: "$ref_juegos",
                    initialValue: [],
                    in: { $concatArrays: ["$$value", "$$this"] }
                }
            }
        }
    },
    {
        $replaceRoot: {
            newRoot: {
                $mergeObjects: [
                    "$original",
                    { "cantidad_juego_por_tipo": "$cantidad_juego_por_tipo" },
                    { "ref_juegos": "$ref_juegos" }
                ]
            }
        }
    },

    {
        // Areas con incidentes_seguridad
        $lookup: {
            from: 'incidentes_seguridad',
            localField: '_id',
            foreignField: 'AreaRecreativaID',
            as: 'ref_incidentes_seguridad'
        }
    },

    {
        // Areas con encuestas_satisfaccion
        $lookup: {
            from: 'encuestas_satisfaccion',
            localField: '_id',
            foreignField: 'AreaRecreativaID',
            as: 'ref_encuestas_satisfaccion'
        }
    },
    {
        // Areas con estaciones_meteo_codigo_postal
        $lookup: {
            from: 'estaciones_meteo_codigo_postal',
            localField: 'COD_POSTAL',
            foreignField: 'Codigo Postal',
            as: 'ref_estaciones_meteo_codigo_postal'
        }
    },
    {
        // estaciones_meteo_codigo_postal con meteo24
        $lookup: {
            from: 'meteo24',
            localField: 'ref_estaciones_meteo_codigo_postal.CÓDIGO',
            foreignField: 'PUNTO_MUESTREO',
            as: 'ref_estaciones_meteo_codigo_postal.ref_meteo'
        }
    },
    {
        $set: {
            TOTAL_ELEM: { $size: "$ref_juegos" }
        }
    },
    {
        $addFields: {
            encuestas_accesibilidad_transformado: {
                $map: {
                    input: "$ref_encuestas_satisfaccion.PUNTUACION_ACCESIBILIDAD",
                    as: "puntuacion",
                    in: { $subtract: [6, "$$puntuacion"] }
                }
            },
            encuestas_calidad_transformado: {
                $map: {
                    input: "$ref_encuestas_satisfaccion.PUNTUACION_CALIDAD",
                    as: "puntuacion",
                    in: { $subtract: [6, "$$puntuacion"] }
                }
            }
        }
    },
    {
        $addFields: {
            capacidadMax: "$TOTAL_ELEM",
            nota_encuestas_area: {
                $sum: {
                    $concatArrays: ["$encuestas_accesibilidad_transformado", "$encuestas_calidad_transformado"]
                }
            },

            numero_incidencias_ponderado: {
                $multiply: [{ $size: "$ref_incidentes_seguridad" }, 3]
            },
            juegos_mantenimiento: {
                $size: {
                    $filter: {
                        input: "$ref_juegos",
                        as: "juego",
                        cond: {
                            $eq: ["$$juego.ESTADO", "EN REPARACION"]
                        }
                    }
                }
            },
        }
    },
    {
        $addFields: {
            nota_total_area: {
                $sum:
                    ["$nota_encuestas_area", "$numero_incidencias_ponderado", "$juegos_mantenimiento"]

            }
        }
    },
    {
        // Agrupamos para calcular el maximo de nota_total_area entre todos los documentos
        $group: {
            _id: null,
            max_nota_global: { $max: "$nota_total_area" },
            areas: { $push: "$$ROOT" }
        }
    },
    {
        // Desagregamos para aplicar el maximo calculado a cada documento
        $unwind: "$areas"
    },
    {
        $replaceRoot: {
            newRoot: {
                $mergeObjects: ["$areas", { max_nota: "$max_nota_global" }]
            }
        }
    },
    {
        $addFields: {
            estado_global_area: {
                $round: [
                    {
                        $multiply: [
                            { $divide: ["$nota_total_area", "$max_nota"] },
                            10
                        ]
                    },
                    2
                ]
            },
        }
    },
    {
        $addFields: {
            estado_global_area: {
                $subtract: [10, "$estado_global_area"]
            }
        }
    },
    {
        $project: {
            _id: 1,
            SISTEMA_COORD: 1,
            LATITUD: 1,
            LONGITUD: 1,
            BARRIO: 1,
            DISTRITO: 1,
            FECHA_INSTALACION: 1,
            ESTADO: 1,
            TOTAL_ELEM: 1,
            capacidadMax: 1,
            cantidad_juego_por_tipo: 1,
            estado_global_area: 1,
            ref_juegos: 1,
            ref_incidentes_seguridad: {
                _id: 1,
                GRAVEDAD: 1,
                FECHA_REPORTE: 1,
            },
            ref_encuestas_satisfaccion: {
                _id: 1
            },
            ref_estaciones_meteo_codigo_postal: {
                _id: 1
            },
        }
    },
    {
        $out: { db: "entregable2", coll: "agregado_area_recreativa_clima" }
    }
]);


// --------- AGREGADO DE JUEGOS CON MANTENIMIENTO E INCIDENCIAS ---------

// Agregado de juego
db.juegos.aggregate([
    {
        // Juegos con mantenimiento
        $lookup: {
            from: 'mantenimiento',
            localField: '_id',
            foreignField: 'JuegoID',
            as: 'ref_mantenimiento'
        }
    },
    {
        $lookup: {
            from: "incidencias_usuarios",
            localField: "ref_mantenimiento._id",
            foreignField: "MantenimientoID",
            as: "res_incidencias_usuarios"
        }
    },

    {
        $out: { db: "entregable2", coll: "agregado_juego" }
    }
]);

// Cálculo de los atributos derivados: indicadorExposición, últimaFechaMantenimiento, tiempoResolución y desgaste acumulado
db.agregado_juego.aggregate([
    {
        $addFields: {
            "indicadorExposicion": {
                $add: [
                    {
                        $floor: {
                            $multiply: [
                                { $rand: {} },
                                3
                            ]
                        }
                    },
                    1
                ]
            },
            "ultimaFechaMantenimiento": {
                $max: {
                    $map: {
                        input: "$ref_mantenimiento",
                        as: "ref",
                        in: {
                            $dateFromString: {
                                dateString: "$$ref.FECHA_INTERVENCION",
                                format: "%Y-%m-%dT%H:%M:%SZ"
                            }
                        }
                    }
                }
            },
            "res_incidencias_usuarios": {
                $map: {
                    input: "$res_incidencias_usuarios",
                    as: "ref",
                    in: {
                        ID: "$$ref._id",
                        TIPO_INCIDENCIA: "$$ref.TIPO_INCIDENCIA",
                        FECHA_REPORTE: "$$ref.FECHA_REPORTE",
                        ESTADO: "$$ref.ESTADO",
                        tiempoResolucion: {
                            $max: {
                                $map: {
                                    input: "$$ref.MantenimientoID",
                                    as: "mantenimiento_id",
                                    in: {
                                        $subtract: [
                                            {
                                                $arrayElemAt: [
                                                    {
                                                        $map: {
                                                            input: {
                                                                $filter: {
                                                                    input: "$ref_mantenimiento",
                                                                    as: "mantenimiento",
                                                                    cond: { $eq: ["$$mantenimiento._id", "$$mantenimiento_id"] }
                                                                }
                                                            },
                                                            as: "man",
                                                            in: {
                                                                $dateFromString: {
                                                                    dateString: "$$man.FECHA_INTERVENCION",
                                                                    format: "%Y-%m-%dT%H:%M:%SZ"
                                                                }
                                                            }
                                                        }
                                                    },
                                                    0
                                                ]
                                            },
                                            {
                                                $dateFromString: {
                                                    dateString: "$$ref.FECHA_REPORTE",
                                                    format: "%Y-%m-%dT%H:%M:%SZ"
                                                }
                                            }
                                        ]
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "ref_mantenimiento": {
                $map: {
                    input: "$ref_mantenimiento",
                    in: "$$this._id"
                }
            }
        }
    },
    {
        $addFields: {
            "desgasteAcumulado": {
                $max: [
                    {
                        $subtract: [
                            {
                                $multiply: [
                                    {
                                        $add: [
                                            {
                                                $floor: {
                                                    $multiply: [
                                                        { $rand: {} },
                                                        15
                                                    ]
                                                }
                                            },
                                            1
                                        ]
                                    },
                                    "$indicadorExposicion"
                                ]
                            },
                            {
                                $multiply: [
                                    { $size: "$ref_mantenimiento" },
                                    5
                                ]
                            }
                        ]
                    },
                    0
                ]
            }
        }
    },
    {
        $out: {
            db: "entregable2",
            coll: "agregado_juego"
        }
    }
]);


// --------- AGREGADO DE INCIDENCIAS Y USUARIOS ---------

// Agregado con el resumen de usuarios y el dato agregado nivelEscalamiento
db.incidencias_usuarios.aggregate([
    {
        // Incidencias con usuario
        $lookup: {
            from: 'usuarios',
            localField: 'UsuarioID',
            foreignField: '_id',
            as: 'ref_usuarios'
        }
    },
    {
        $addFields: {
            nivelEscalamiento: {
                $add: [
                    { $floor: { $multiply: [{ $rand: {} }, 10] } },
                    1
                ]
            }
        }
    },
    {
        $project: {
            UsuarioID: 0,
            MantenimientoID: 0
        }
    },
    {
        $out: { db: "entregable2", coll: "agregado_incidencia" }
    }
]);
