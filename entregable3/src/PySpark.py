from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.sql import DataFrame

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



# Seleccionar las columnas necesarias de la tabla original
discrepancia_carne = json_df.select(
    col("vehicle.Driver.DNI").alias("dni_conductor"),
    col("vehicle.Owner.DNI").alias("dni_propietario"),
    col("Record.date").alias("fecha_record"),
    col("vehicle.Driver.Birthdate").alias("fecha_nacimiento"),
    col("vehicle.Driver.driving_license.date").alias("fecha_carne"),
    col("vehicle.number_plate").alias("matricula")

)

# Mostrar los datos seleccionados
discrepancia_carne.show()



