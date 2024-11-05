// --------- AGREGADO DE ÁREAS CON JUEGOS, METERO, INCIDENTES Y ENCUESTAS DE SATISFACCIÓN ---------


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
                                {$rand: {}}, 
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

// Creación del agregado con el resumen de usuarios y el dato agregado nivelEscalamiento
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
            USUARIOS: {
                $map: {
                    input: "$ref_usuarios",
                    as: "usuario",
                    in: {
                        nombre: "$$usuario.NOMBRE",
                        email: "$$usuario.EMAIL",
                        telefono: "$$usuario.TELEFONO"
                    }
                }
            },
            nivelEscalamiento: { 
                $add: [
                    {$floor: { $multiply: [{$rand: {}}, 10]}}, 
                    1
                ]
            }
        }
    },
    {
        $project: {
            _id: 1,
            TIPO_INCIDENCIA: 1,
            FECHA_REPORTE: 1,
            ESTADO: 1,
            USUARIOS: 1,
            MantenimeintoID: 1,
            nivelEscalamiento: 1
        }
    },
    {
        $out: {db:"entregable2", coll: "agregado_incidencia"}
    }
]);
