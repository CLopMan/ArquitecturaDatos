unzip ./data/sample.zip
python3 json_parser.py
cqlsh < tablas.cql
spark-submit --packages com.datastax.spark:spark-cassandra-connector_2.12:3.3.0 PySpark.py 2> /dev/null

