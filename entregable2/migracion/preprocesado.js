use entregable2_old;
// ---------------- CAST --------------

db.areas.aggregate([
    {
        $addFields: {
            _id: {
                $convert: {
                    input: "$_id",
                    to: "string",
                    onError: null,
                    onNull: null
                }
            }
        }
    },
    {
        $addFields: {
            COD_POSTAL: {
                $convert: {
                    input: "$COD_POSTAL",
                    to: "int",
                    onError: null,
                    onNull: null
                }
            },
            COD_DISTRITO: {
                $convert: {
                    input: "$COD_DISTRITO",
                    to: "int",
                    onError: null,
                    onNull: null
                }
            }
        }
    },
    {
        $addFields: {
            LATITUD: {
                $convert: {
                    input: "$LATITUD",
                    to: "string",
                    onError: null,
                    onNull: null
                }
            },
            LONGITUD: {
                $convert: {
                    input: "$LONGITUD",
                    to: "string",
                    onError: null,
                    onNull: null
                }
            },
            NUM_VIA: {
                $convert: {
                    input: "$NUM_VIA",
                    to: "string",
                    onError: null,
                    onNull: null
                }
            }
        }
    },
    {
        $addFields: {
            FECHA_INSTALACION: {
                $dateFromString: {
                    dateString: "$FECHA_INSTALACION",
                    format: "%Y-%m-%dT%H:%M:%SZ"
                }
            }
        }
    },
    {
        $out: {
            db: "entregable2_old",
            coll: "areas"
        }
    }
]);

db.juegos.aggregate([
    {
        $addFields: {
            _id: {
                $convert: {
                    input: "$_id",
                    to: "string",
                    onError: null,
                    onNull: null
                }
            }
        }
    },
    {
        $addFields: {
            COD_DISTRITO: {
                $convert: {
                    input: "$COD_DISTRITO",
                    to: "int",
                    onError: null,
                    onNull: null
                }
            },
            COD_POSTAL: {
                $convert: {
                    input: "$COD_POSTAL",
                    to: "string",
                    onError: null,
                    onNull: null
                }
            },
            LATITUD: {
                $convert: {
                    input: "$LATITUD",
                    to: "string",
                    onError: null,
                    onNull: null
                }
            },
            LONGITUD: {
                $convert: {
                    input: "$LONGITUD",
                    to: "string",
                    onError: null,
                    onNull: null
                }
            },
            MODELO: {
                $convert: {
                    input: "$LONGITUD",
                    to: "string",
                    onError: null,
                    onNull: null
                }
            },
            ACCESIBLE: {
                $convert: {
                    input: "$LONGITUD",
                    to: "bool",
                    onError: null,
                    onNull: null
                }
            },
            NUM_VIA: {
                $convert: {
                    input: "$NUM_VIA",
                    to: "string",
                    onError: null,
                    onNull: null
                }
            }
        }
    },
    {
        $addFields: {
            FECHA_INSTALACION: {
                $dateFromString: {
                    dateString: "$FECHA_INSTALACION",
                    format: "%Y-%m-%dT%H:%M:%SZ"
                }
            }
        }
    },
    {
        $out: {
            db: "entregable2_old", coll: "juegos"
        }
    }
]);

db.encuestas_satisfaccion.aggregate([
    {
        $addFields: {
            _id: {
                $convert: {
                    input: "$_id",
                    to: "string",
                    onError: null,
                    onNull: null
                }
            }
        }
    },
    {
        $addFields: {
            FECHA: {
                $dateFromString: {
                    dateString: "$FECHA",
                    format: "%Y-%m-%dT%H:%M:%SZ"
                }
            }
        } 
    },
    {
        $addFields: {
            AreaRecreativaID: {
                $convert: {
                    input: "$AreaRecreativaID",
                    to: "string",
                    onError: null,
                    onNull: null
                }
            }
        } 
    },
    {$out: {
        db: "entregable2_old", coll:"encuestas_satisfaccion"
    }}
]);

db.incidentes_seguridad.aggregate([
    {
        $addFields: {
            _id: {
                $convert: {
                    input: "$_id",
                    to: "string",
                    onError: null,
                    onNull: null
                }
            }
        }
    },
    {
        $addFields: {
            FECHA_REPORTE: {
                $dateFromString: {
                    dateString: "$FECHA_REPORTE",
                    format: "%Y-%m-%dT%H:%M:%SZ"
                }
            }
        } 
    },
    {$out: {
        db: "entregable2_old", coll:"incidentes_seguridad"
    }}
]);

db.usuarios.aggregate([
    {
        $addFields: {
            _id: {
                $convert: {
                    input: "$_id",
                    to: "string",
                    onError: null,
                    onNull: null
                }
            }
        }
    },
    {
        $out: {
            db: "entregable2_old",
            coll: "usuarios"
        }
    }
])

db.mantenimiento.aggregate([
    {
        $addFields: {
            FECHA_REPORTE: {
                $dateFromString: {
                    dateString: "$FECHA_REPORTE",
                    format: "%Y-%m-%dT%H:%M:%SZ"
                }
            }
        } 
    },
    {
        $out: {
            db: "entregable2_old",
            coll: "mantenimiento"
        }
    }
]);

db.incidencias_usuarios.aggregate([
    {
        $addFields: {
            _id: {
                $convert: {
                    input: "$_id",
                    to: "string",
                    onError: null,
                    onNull: null
                }
            }
        }
    },
    {
        $addFields: {
            FECHA_REPORTE: {
                $dateFromString: {
                    dateString: "$FECHA_REPORTE",
                    format: "%Y-%m-%dT%H:%M:%SZ"
                }
            }
        } 
    },
    {$out: {
        db: "entregable2_old", coll:"incidencias_usuarios"
    }}
]);
// ------------- PARSER -----------------

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
                    }, ","]
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
                    }, ","]
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
        $out: { db: "entregable2_old", coll: "incidencias_usuarios" }
    }
]);
