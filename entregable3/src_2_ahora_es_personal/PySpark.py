from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_timestamp, date_add, sum, avg, count, concat
from pyspark.sql import DataFrame
from pyspark.sql.functions import lit, count, max, avg
from pyspark.sql.functions import to_date, date_format, col

# ----- CONSTANTES -----

KEYSPACE = "practica2"

# Ruta al archivo NDJSON
file_path = "./data/sample_parsed.json"

# ----- CREACIÓN DE LA SESIÓN DE PYSPARK -----
spark = SparkSession.builder \
    .appName("CargaDatos") \
    .config("spark.cassandra.connection.host", "127.0.0.1") \
    .config("spark.cassandra.connection.port", "9042") \
    .getOrCreate()

# ----- FUNCIONES AUXILIARES -----

def convertir_formato_fecha(df, columna_fecha):
    """
    Convierte el formato de una columna de fechas a timestamps

    :param df: DataFrame de PySpark
    :param columna_fecha: Nombre de la columna que contiene las fechas a convertir
    :return: DataFrame con la columna de fecha convertida
    """
    # Convertir la columna de fecha a formato timestamp
    df_converted = df.withColumn(
        columna_fecha,
        to_timestamp(col(columna_fecha), 'dd/MM/yyyy HH:mm:ss.SSS')
    )

    return df_converted

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

def write_to_cassandra(table, name, mode):
    table.write.format("org.apache.spark.sql.cassandra")\
    .options(table=name, keyspace=KEYSPACE)\
    .mode(mode)\
    .save()

# ----- FUNCIONES DE GENERACIÓN DE LAS TABLAS GENERALES -----
def gen_impago_sanciones():
    
    # Calcula los speeding tickets
    speed = speed_ticket.filter(col("fecha_pago").isNull() & (col("estado") != "fullfilled")).select("dni_deudor", "dni_propietario", "dni_conductor", "fecha_grabacion", "matricula", "cantidad").withColumn("tipo_multa", lit("velocidad"))
    
    # Calcula los clearence tickets
    clearance = clearance_ticket.filter(col("fecha_pago").isNull() & (col("estado") != "fullfilled")).select("dni_deudor","dni_propietario", "dni_conductor", "fecha_grabacion","matricula", "cantidad").withColumn("tipo_multa", lit("clearance"))
  
    # Calcula los stretch ticket
    stretch = clearance_ticket.filter(col("fecha_pago").isNull() & (col("estado") != "fullfilled")).select("dni_deudor","dni_propietario", "dni_conductor", "fecha_grabacion", "matricula", "cantidad").withColumn("tipo_multa", lit("stretch"))

    return speed.union(clearance).union(stretch)

def gen_sanciones():
    
    # Calcula los speeding tickets
    speed = speed_ticket.select("dni_deudor", "dni_propietario", "dni_conductor", "fecha_grabacion", "estado", "matricula", "cantidad").withColumn("tipo", lit("velocidad"))

    # Calcula los clearence tickets
    clearance = clearance_ticket.select("dni_deudor", "dni_propietario","dni_conductor", "fecha_grabacion", "estado", "matricula", "cantidad").withColumn("tipo", lit("clearance"))

    # Calcula los stretch ticket
    stretch = clearance_ticket.select("dni_deudor", "dni_propietario","dni_conductor", "fecha_grabacion", "estado" ,"matricula", "cantidad").withColumn("tipo", lit("stretch"))

    # Obtiene impago y reorganiza
    impago = impago_sanciones.select("dni_deudor","dni_propietario", "dni_conductor", "fecha_grabacion", "cantidad", "matricula").withColumn("tipo", lit("impago")).withColumn("estado", lit("stand by"))
    impago = impago.select("dni_deudor", "dni_propietario", "dni_conductor", "fecha_grabacion", "estado", "matricula", "cantidad", "tipo")

    # Obtiene carne y reorganiza TODO: Revisar estado y cantidad
    carne = discrepancia_carne.select("dni_propietario", "dni_conductor", "fecha_record", "matricula").withColumn("tipo", lit("discrepancia carne")).withColumn("estado", lit("stand by")).withColumn("cantidad", lit(1000)).withColumn("dni_deudor", discrepancia_carne["dni_conductor"])
    carne = carne.select("dni_deudor", "dni_propietario", "dni_conductor", "fecha_record", "estado", "matricula", "cantidad", "tipo")

    # Obtiene desperfectos y reorganiza TODO: Revisar estado y cantidad
    desperfectos = vehiculo_deficiente.select("dni_propietario", "dni_conductor", "fecha_record", "matricula").withColumn("tipo", lit("desperfectos")).withColumn("estado", lit("stand by")).withColumn("cantidad", lit(1000)).withColumn("dni_deudor", vehiculo_deficiente["dni_propietario"])
    desperfectos = desperfectos.select("dni_deudor", "dni_propietario", "dni_conductor", "fecha_record", "estado", "matricula","cantidad", "tipo")

    return speed.union(clearance).union(impago).union(stretch).union(carne).union(desperfectos)

def gen_sanciones_vehiculo():
    sanciones_vehiculo = sanciones.join(vehiculos, sanciones["matricula"] == vehiculos["matricula"]).select(vehiculos["matricula"], vehiculos["marca"], sanciones["tipo"], vehiculos["modelo"], vehiculos["color"], sanciones["fecha_grabacion"])
    return sanciones_vehiculo

# ----- FUNCIONES DE GENERACIÓN DE LAS TABLAS DE LOS CASOS DE USO -----

# Funciones del caso de uso 1
def gen_multas_marca_modelo():
    return sanciones_vehiculo.select("marca", "modelo", "matricula", "fecha_grabacion", "tipo")

def gen_multas_color():
    return sanciones_vehiculo.select("color", "matricula", "fecha_grabacion")

# Funciones del caso de uso 2
def gen_tramo_conflictivo():
    return speed_ticket.select("carretera","kilometro","sentido","fecha_grabacion")

def gen_exceso_velocidad_medio():
    return speed_ticket.select("carretera", "velocidad_registrada", "velocidad_limite_radar", "fecha_grabacion")

# Funciones del caso de uso 3
def gen_probabilidad_infraccion():
    return sanciones.select("matricula", "fecha_grabacion", (col("dni_conductor") == col("dni_propietario")).alias("conductor_igual_propietario"))

# ----- LECTURA DE FICHERO -----

# Leer el archivo NDJSON
json_df = spark.read.json(file_path)

# Aplicar la función al DataFrame original
json_df = rename_columns(json_df)

# ----- GENERACIÓN DE LAS TABLAS -----

# Seleccionar las columnas necesarias de la discrepancia carné
discrepancia_carne = json_df.select(
    col("vehicle.Driver.DNI").alias("dni_conductor"),
    col("vehicle.Owner.DNI").alias("dni_propietario"),
    concat(col("Record.date"), lit(" "), col("Record.time")).alias("fecha_record"),
    col("vehicle.Driver.Birthdate").alias("fecha_nacimiento"),
    col("vehicle.Driver.driving_license.date").alias("fecha_carne"),
    col("vehicle.number_plate").alias("matricula")
).filter(
    to_date(col("vehicle.Driver.driving_license.date"),"dd/MM/yyyy") < date_add(to_date(col("vehicle.Driver.Birthdate"),"dd/MM/yyyy"), 18 * 365)
)

vehiculo_deficiente = json_df.select(
    col("vehicle.Driver.DNI").alias("dni_conductor"),
    col("vehicle.Owner.DNI").alias("dni_propietario"),
    concat(col("Record.date"), lit(" "), col("Record.time")).alias("fecha_record"),
    col("vehicle.roadworthiness").alias("revisiones"),
    col("vehicle.make").alias("marca"),
    col("vehicle.model").alias("modelo"),
    col("vehicle.number_plate").alias("matricula")
).filter(
    ~col("vehicle.roadworthiness").rlike("^[0-9]{2}/[0-9]{2}/[0-9]{4}$") &
    ~col("vehicle.roadworthiness").rlike(r'.*\{"MOT date":"[0-9]{2}/[0-9]{2}/[0-9]{4}"\}]$')
)

# Seleccionar las columnas para la nueva tabla de clearance_ticket
clearance_ticket = json_df.filter(col("Clearance_ticket").isNotNull()).select(
    col("Clearance_ticket.Debtor.DNI").alias("dni_deudor"),
    col("vehicle.Owner.DNI").alias("dni_propietario"),
    col("vehicle.Driver.DNI").alias("dni_conductor"),
    concat(col("Record.date"), lit(" "), col("Record.time")).alias("fecha_grabacion"),
    col("Clearance_ticket.Pay_date").alias("fecha_pago"),
    col("Clearance_ticket.Amount").alias("cantidad"),
    col("vehicle.number_plate").alias("matricula"),
    col("Clearance_ticket.State").alias("estado")
)

# Seleccionar las columnas para la nueva tabla de stretch ticket
stretch_ticket = json_df.filter(col("Stretch_ticket").isNotNull()).select(
    col("Stretch_ticket.Debtor.DNI").alias("dni_deudor"),
    col("vehicle.Owner.DNI").alias("dni_propietario"),
    col("vehicle.Driver.DNI").alias("dni_conductor"),
    concat(col("Record.date"), lit(" "), col("Record.time")).alias("fecha_grabacion"),
    col("Stretch_ticket.Pay_date").alias("fecha_pago"),
    col("Stretch_ticket.Amount").alias("cantidad"),
    col("vehicle.number_plate").alias("matricula"),
    col("vehicle.Owner.DNI").alias("dni_propietario"),
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
    col("vehicle.Owner.DNI").alias("dni_propietario"),
    col("vehicle.Driver.DNI").alias("dni_conductor"),
    col("Speed_ticket.Pay_date").alias("fecha_pago"),
    col("Speed_ticket.Amount").alias("cantidad"),
    concat(col("Record.date"), lit(" "), col("Record.time")).alias("fecha_grabacion"),
    col("road.name").alias("carretera"),
    col("radar.mileage").alias("kilometro"),
    col("radar.direction").alias("sentido"),
    col("road.speed_limit").alias("velocidad_limite_carretera"),
    col("radar.speed_limit").alias("velocidad_limite_radar"),
    col("Record.speed").alias("velocidad_registrada"),
    col("vehicle.number_plate").alias("matricula"),
    col("Speed_ticket.State").alias("estado")
)

# Generar las sanciones 
impago_sanciones = gen_impago_sanciones()
sanciones = gen_sanciones()
sanciones_vehiculo = gen_sanciones_vehiculo()
sanciones_vehiculo = convertir_formato_fecha(sanciones_vehiculo, "fecha_grabacion")

# Caso de uso 1
multas_marca_modelo = gen_multas_marca_modelo()
multas_color = gen_multas_color()

# Caso de uso 2
tramo_conflictivo = gen_tramo_conflictivo()
exceso_velocidad_medio = gen_exceso_velocidad_medio()

# Caso de uso 3
probabilidad_infraccion = gen_probabilidad_infraccion()
probabilidad_infraccion = convertir_formato_fecha(probabilidad_infraccion, "fecha_grabacion")

# ----- ESCRITURA EN CASSANDRA -----
sanciones = convertir_formato_fecha(sanciones, "fecha_grabacion")
tramo_conflictivo = convertir_formato_fecha(tramo_conflictivo, "fecha_grabacion")
exceso_velocidad_medio = convertir_formato_fecha(exceso_velocidad_medio,"fecha_grabacion")
write_to_cassandra(sanciones, "sanciones", "append")
write_to_cassandra(multas_marca_modelo, "multas_marca_modelo", "append")
write_to_cassandra(multas_color, "multas_color_coche", "append")
write_to_cassandra(tramo_conflictivo, "conflictos_tramo_sentido", "append")
write_to_cassandra(exceso_velocidad_medio, "exceso_velocidad_carretera", "append")
write_to_cassandra(probabilidad_infraccion, "probabilidad_infraccion", "append")

spark.stop()
exit()
