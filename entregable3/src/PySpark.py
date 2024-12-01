from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_date, date_add, sum, avg, count
from pyspark.sql import DataFrame
from pyspark.sql.functions import lit, count, max, avg

KEYSPACE = "practica2"

# Crear una sesión de Spark
spark = SparkSession.builder \
    .appName("Carga de datos con PySpark") \
    .getOrCreate()

# Ruta al archivo NDJSON
file_path = "./data/sample_parsed.json"

# Leer el archivo NDJSON
json_df = spark.read.json(file_path)


def rename_columns(df: DataFrame) -> DataFrame:
    def rename_struct_fields(schema):
        """Renombra campos dentro de estructuras anidadas."""
        from pyspark.sql.types import StructType, StructField
        
        new_fields = []
        for field in schema.fields:
            new_name = field.name.replace(" ", "_")  # Reemplazar espacios por "_"
            if isinstance(field.dataType, StructType):  # Si el campo es una estructura anidada
                new_field = StructField(new_name, rename_struct_fields(field.dataType), field.nullable)
            else:
                new_field = StructField(new_name, field.dataType, field.nullable)
            new_fields.append(new_field)
        return StructType(new_fields)
    
    new_schema = rename_struct_fields(df.schema)  # Aplicar renombrado al esquema
    # Aplicar los cambios al DataFrame
    return spark.createDataFrame(df.rdd, new_schema)

# Aplicar la función al DataFrame original
json_df = rename_columns(json_df)

# Mostrar el nuevo esquema
json_df.printSchema()

# Seleccionar las columnas necesarias de la discrepancia carné
discrepancia_carne = json_df.select(
    col("vehicle.Driver.DNI").alias("dni_conductor"),
    col("vehicle.Owner.DNI").alias("dni_propietario"),
    col("Record.date").alias("fecha_record"),
    col("vehicle.Driver.Birthdate").alias("fecha_nacimiento"),
    col("vehicle.Driver.driving_license.date").alias("fecha_carne"),
    col("vehicle.number_plate").alias("matricula")
).filter(
    to_date(col("vehicle.Driver.driving_license.date"),"dd/MM/yyyy") < date_add(to_date(col("vehicle.Driver.Birthdate"),"dd/MM/yyyy"), 18 * 365)
)

vehiculo_deficiente = json_df.select(
    col("vehicle.Driver.DNI").alias("dni_conductor"),
    col("vehicle.Owner.DNI").alias("dni_propietario"),
    col("Record.date").alias("fecha_record"),
    col("vehicle.roadworthiness").alias("revisiones"),
    col("vehicle.make").alias("marca"),
    col("vehicle.model").alias("modelo"),
    col("vehicle.number_plate").alias("matricula")
).filter(
    ~col("vehicle.roadworthiness").rlike("^[0-9]{2}/[0-9]{2}/[0-9]{4}$") &
    ~col("vehicle.roadworthiness").rlike(r'.*\{"MOT date":"[0-9]{2}/[0-9]{2}/[0-9]{4}"\}]$')
)

# Seleccionar las columnas para la nueva tabla de clearance_ticket
#### TODO: preguntarle a la profe que cojones es clearance_ticket porque en nuestro esquema guardamos una matrícula
clearance_ticket = json_df.filter(col("Clearance_ticket").isNotNull()).select(
    col("Clearance_ticket.Debtor.DNI").alias("dni_deudor"),
    col("Record.date").alias("fecha_grabacion"),
    col("Clearance_ticket.Pay_date").alias("fecha_pago"),
    col("Clearance_ticket.Amount").alias("cantidad"),
    col("vehicle.number_plate").alias("matricula"),
    col("Clearance_ticket.State").alias("estado")
)

# Seleccionar las columnas para la nueva tabla de stretch ticket
stretch_ticket = json_df.filter(col("Stretch_ticket").isNotNull()).select(
    col("Stretch_ticket.Debtor.DNI").alias("dni_deudor"),
    col("Record.date").alias("fecha_grabacion"),
    col("Stretch_ticket.Pay_date").alias("fecha_pago"),
    col("Stretch_ticket.Amount").alias("cantidad"),
    col("vehicle.number_plate").alias("matricula"),
    col("Stretch_ticket.State").alias("estado")
)

# Seleccionar las columnas para la nueva tabla de vehiculos
vehiculos = json_df.select(
    col("vehicle.number_plate").alias("matricula"),
    col("vehicle.make").alias("marca"),
    col("vehicle.model").alias("modelo"),
    col("vehicle.colour").alias("color")
)
vehiculos = vehiculos.dropDuplicates()

# Seleccionar las columnas para la nueva tabla de velocidad
speed_ticket = json_df.filter(col("radar.speed_limit") < col("Record.speed")).select(
    col("Speed_ticket.Debtor.DNI").alias("dni_deudor"),
    col("Speed_ticket.Pay_date").alias("fecha_pago"),
    col("Speed_ticket.Amount").alias("cantidad"),
    col("vehicle.Driver.DNI").alias("dni_conductor"),
    col("vehicle.Owner.DNI").alias("dni_propietario"),
    col("Record.date").alias("fecha_grabacion"),
    col("road.name").alias("carretera"),
    col("radar.mileage").alias("kilometro"),
    col("radar.direction").alias("sentido"),
    col("road.speed_limit").alias("velocidad_limite_carretera"),
    col("radar.speed_limit").alias("velocidad_limite_radar"),
    col("Record.speed").alias("velocidad_registrada"),
    col("vehicle.number_plate").alias("matricula"),
    col("Speed_ticket.State").alias("estado")
)


def gen_impago_sanciones():
    speed = speed_ticket.filter(col("fecha_pago").isNull() & (col("estado") != "fullfilled")).select("dni_deudor", "fecha_grabacion", "matricula", "cantidad").withColumn("tipo_multa", lit("velocidad"))
    clearance = clearance_ticket.filter(col("fecha_pago").isNull() & (col("estado") != "fullfilled")).select("dni_deudor", "fecha_grabacion","matricula", "cantidad").withColumn("tipo_multa", lit("clearance"))
    stretch = clearance_ticket.filter(col("fecha_pago").isNull() & (col("estado") != "fullfilled")).select("dni_deudor", "fecha_grabacion", "matricula", "cantidad").withColumn("tipo_multa", lit("stretch"))
    return speed.union(clearance).union(stretch)

def gen_sanciones():
    speed = speed_ticket.select("dni_deudor", "fecha_grabacion", "estado", "matricula", "cantidad").withColumn("tipo", lit("velocidad"))
    clearance = clearance_ticket.select("dni_deudor", "fecha_grabacion", "estado", "matricula", "cantidad").withColumn("tipo", lit("clearance"))
    stretch = clearance_ticket.filter(col("fecha_pago").isNull() & (col("estado") != "fullfilled")).select("dni_deudor", "fecha_grabacion", "estado" ,"matricula", "cantidad").withColumn("tipo", lit("stretch"))

    # Obtiene impago y reorganiza
    impago = impago_sanciones.select("dni_deudor", "fecha_grabacion", "cantidad", "matricula").withColumn("tipo", lit("impago")).withColumn("estado", lit("stand by"))
    impago = impago.select("dni_deudor", "fecha_grabacion", "estado", "matricula", "cantidad", "tipo")

    # Obtiene carne y reorganiza TODO: Revisar estado y cantidad
    carne = discrepancia_carne.select("dni_propietario", "fecha_record", "matricula").withColumn("tipo", lit("discrepancia carne")).withColumn("estado", lit("stand by")).withColumn("cantidad", lit(1000))
    carne = carne.select("dni_propietario", "fecha_record", "estado", "matricula", "cantidad", "tipo")

    # Obtiene desperfectos y reorganiza TODO: Revisar estado y cantidad
    desperfectos = vehiculo_deficiente.select("dni_propietario", "fecha_record", "matricula").withColumn("tipo", lit("discrepancia carne")).withColumn("estado", lit("stand by")).withColumn("cantidad", lit(1000))
    desperfectos = desperfectos.select("dni_propietario", "fecha_record", "estado", "matricula", "cantidad", "tipo")
    return speed.union(clearance).union(impago).union(stretch).union(carne).union(desperfectos)

def gen_sanciones_vehiculo():
    sanciones_vehiculo = sanciones.join(vehiculos, sanciones["matricula"] == vehiculos["matricula"]).select(vehiculos["matricula"], vehiculos["marca"], sanciones["tipo"], vehiculos["modelo"], vehiculos["color"])
    return sanciones_vehiculo

def write_to_cassandra(table, name, mode):
    df.write.format("org.apache.spark.sql.cassandra")\
    .options(table=name, keyspace=KEYSPACE)\
    .mode(mode)\
    .save()

def gen_tramo_conflictivo():
    # Primer groupBy para contar infracciones por tramo
    infracciones_por_tramo = speed_ticket.select("carretera", "kilometro", "sentido") \
        .groupBy("carretera", "kilometro", "sentido") \
        .agg(count("*").alias("numero_infracciones")) \
        .alias("t1")  # Alias para la primera tabla
    
    # Subconsulta con alias
    max_infracciones = infracciones_por_tramo \
        .groupBy("carretera") \
        .agg(max("numero_infracciones").alias("mayor_numero_infracciones_carretera")) \
        .alias("t2")  # Alias para la segunda tabla
    
    # Join usando los alias
    tramo_conflictivo = infracciones_por_tramo.join(
        max_infracciones,
        (col("t1.carretera") == col("t2.carretera")) &
        (col("t1.numero_infracciones") == col("t2.mayor_numero_infracciones_carretera"))
    ).select(
        col("t1.carretera"),
        col("t1.kilometro"),
        col("t1.sentido"),
        col("t2.mayor_numero_infracciones_carretera")
    )
    return tramo_conflictivo

def gen_exceso_velocidad_medio():
    exceso_velocidad_medio = speed_ticket.select("carretera", "velocidad_registrada") \
    .groupBy("carretera") \
    .agg(avg("velocidad_registrada").alias("exceso_velocidad_media"))
    return exceso_velocidad_medio


# Funciones del caso de uso 1
def gen_multas_marca_modelo():
    return sanciones_vehiculo.select("marca", "modelo").groupBy("marca", "modelo").agg(count("*").alias("num_multas"))

def gen_multas_color():
    return sanciones_vehiculo.select("color").groupBy("color").agg(count("*").alias("num_multas"))

def gen_velocidad_marca_modelo():
    return sanciones_vehiculo.filter(col("tipo") == "velocidad").select("marca", "modelo").groupBy("marca", "modelo").agg(count("*").alias("num_multas"))

# Funciones del caso de uso 3
def gen_conductores_infactores():
    return sanciones.select("dni_deudor").groupBy("dni_deudor").agg(count("*").alias("num_multas"))

# Función del caso de uso general
def gen_sanciones_en_proceso():
    return sanciones.filter(col("estado") == "stand by").select("dni_deudor", "tipo", "fecha_grabacion")

# Inserción en Cassandra
# write_to_cassandra(sanciones, "sanciones", "overwrite")

# Generar las sanciones 
impago_sanciones = gen_impago_sanciones()
sanciones = gen_sanciones()
sanciones_vehiculo = gen_sanciones_vehiculo()
tramo_conflictivo = gen_tramo_conflictivo()
exceso_velocidad_medio = gen_exceso_velocidad_medio()
multas_marca_modelo = gen_multas_marca_modelo()
multas_color = gen_multas_color()
velocidad_marca_modelo = gen_velocidad_marca_modelo()
conductores_infractores = gen_conductores_infactores()
sanciones_en_proceso = gen_sanciones_en_proceso()
