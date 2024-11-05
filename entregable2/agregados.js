db.incidencias_usuarios.aggregate([
    {
        // Convertir el string 'UsuarioID' en un array de valores
        $addFields: {
            MantenimientoID: {
                $split: [
                    {
                      $replaceAll: {
                        input: {
                            $replaceAll: {
                                input: {
                                    $replaceAll: {
                                        input:
                                        {
                                            $replaceAll: {
                                                input: "$MantenimeintoID",
                                                find: " ",
                                                replacement: ""
                                            }
                                        },
                                        find: "'",
                                        replacement: ""
                                    }
                                },
                                find: "]",
                                replacement: ""
                            }
                        },
                        find: "[",
                        replacement: ""
                    }
                  },","]
            },
            UsuarioID: { 
                $split: [
                    { 
                      $replaceAll: {  
                        input: {
                            $replaceAll: { 
                                input: {
                                    $replaceAll: { 
                                        input: 
                                        {
                                            $replaceAll: {
                                                input: "$UsuarioID",
                                                find: " ",
                                                replacement: ""
                                            }
                                        }, 
                                        find: "'", 
                                        replacement: "" 
                                    }
                                },
                                find: "]", 
                                replacement: "" 
                            }
                        },
                        find: "[", 
                        replacement: "" 
                    }
                  },","]
            }
        }
    },
    {
        $project: {
            _id: 1,
            TIPO_INCIDENCIA: 1,
            FECHA_REPORTE: 1,
            ESTADO: 1,
            UsuarioID: 1,
            MantenimientoID: 1
        }
    },
    {
        $out: {db: "entregable2", coll: "incidencias_usuarios"}
    }
])

db.juegos.aggregate([
    {
        // Juegos con mantenimiento
        $lookup: {
            from: 'juegos',
            localField: '_id',
            foreignField: 'JuegoID',
            as: 'ref_mantenimiento'
        }
    },
    {
        // Juego con incidencias
        $lookup: {
            from: 'incidencias_usuario',
            localField: '_id',
            foreignField: 'UsuarioID',
            as: 'ref_incidentes_usuario'
        }
    },
    {
        $out: {db:"entregable2", coll: "agregado_juego"}
    }
]);

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
