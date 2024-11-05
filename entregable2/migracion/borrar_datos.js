use entregable2

db.getCollectionNames().forEach(function (collection) {
    db[collection].drop();
    print("Colección '" + collection + "' eliminada.");
});