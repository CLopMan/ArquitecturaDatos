db.areas.aggregate([
    {
        $addFields:{
            FECHA_INTERVENCION: {
                $convert: {
                    input:"$FECHA_INTERVENCION",
                    to: "date",
                    onError: null,
                    onNull: null,
                }
            }
        }
    }
]);
