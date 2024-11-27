from pyspark.sql import SparkSession

# Crear una sesión de Spark
spark = SparkSession.builder \
    .appName("Leer NDJSON con PySpark") \
    .getOrCreate()

# Ruta al archivo NDJSON
file_path = "./data/sample_parsed.json"

# Leer el archivo NDJSON
df = spark.read.json(file_path)


# Mostrar los datos leídos
#df.show(truncate=False)

# Mostrar el esquema del DataFrame
#df.printSchema()
# Filtrar los registros donde la edad es mayor a 25
df.show(n=100)
print(df.count())
print(df.rdd.filter(lambda row: row["_corrupt_record"] is not None).count())

