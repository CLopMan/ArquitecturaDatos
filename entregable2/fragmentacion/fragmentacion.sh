### Servidor de configuración

# Creamos los directorios necesarios
sudo mkdir -p /var/lib/data/config-cluster
sudo chown mongodb:mongodb /var/lib/data/config-cluste

sudo mkdir -p /var/log/mongodb
sudo chown mongodb:mongodb /var/log/mongodb

# Levantamos el servidor de configuración
sudo /usr/bin/mongod --fork --config /etc/mongod-config.conf

# Iniciamos el conjunto de replicacion
mongosh --port 27025 < rs.initiate({ _id: "config", configsvr: true, members: [{ _id: 0, host: "localhost:27025" }] }); exit;

### Servidores de sharding

# Creamos los directorios necesarios
sudo mkdir -p /var/lib/data/shard1
sudo chown mongodb:mongodb /var/lib/data/shard1

sudo mkdir -p /var/lib/data/shard2
sudo chown mongodb:mongodb /var/lib/data/shard2

sudo mkdir -p /var/log/mongodb
sudo chown mongodb:mongodb /var/log/mongodb

# Iniciamos los servidores de sharding
sudo /usr/bin/mongod --fork --config /etc/mongo-shard1.conf
sudo /usr/bin/mongod --fork --config /etc/mongo-shard2.conf

# Iniciamos el conjunto de repliacion
mongosh --port 27023 < rs.initiate({ _id: "shard-1", members: [{ _id: 0, host: "localhost:27023" }] }); exit;
mongosh --port 27024 < rs.initiate({ _id: "shard-2", members: [{ _id: 0, host: "localhost:27024" }] }); exit:

### Servidor de enrutamiento

# Lanzar el enrutador en el puerto 27026 con la configuración del puerto 27025
sudo mongos --fork --syslog --bind_ip_all --port 27026 --configdb config/localhost:27025

mongosh --port 27017 < sh.addShard("shard-1/localhost:27023"); sh.addShard("shard-2/localhost:27024"); exit;

# Habilitar la fragmentación en la base de datos
mongosh --port 27017 < sh.enableSharding("entregable2"); exit;

### Claves de fragmentación
mongosh --port 27017 < use AirBnB; db.coleccion.createIndex({ atributo: "hashed" }); sh.shardCollection("entregable.coleccion", { atibuto: "hashed" }); exit;
