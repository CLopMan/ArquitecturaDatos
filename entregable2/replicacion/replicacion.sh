sudo mkdir -p /var/lib/data/node1 /var/lib/data/node2 /var/lib/data/node3
sudo chwon -R mongodb:mongodb /var/lib/data/node*

sudo systemctl enable mongocluster@1
sudo systemctl enable mongocluster@2
sudo systemctl enable mongocluster@3

sudo systemctl start mongocluster@{1,2,3}

mongosh --port 27018 < rsconf = { _id: "rs0", members: [ {_id: 0, host: "localhost:27018"}, {_id: 1, host: "localhost:27019"}, {_id: 2, host: "localhost:27020"}]} rs.initiate(rsconf); exit;
