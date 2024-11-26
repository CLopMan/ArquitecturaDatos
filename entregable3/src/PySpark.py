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
df_a = df.cache()
df_a.filter("_corrupt_record IS NOT NULL").select("_corrupt_record").show(n=880, truncate=False)
print(df.count())
print(df.rdd.filter(lambda row: row["_corrupt_record"] is not None).count())

