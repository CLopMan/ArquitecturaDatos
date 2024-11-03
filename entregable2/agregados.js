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
                    {$floor: { $multiply: [{$rand: {}}, 100]}}, 
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
