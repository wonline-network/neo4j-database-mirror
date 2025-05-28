from neo4j import GraphDatabase



# Conectar a la base de datos de origen
source_driver = GraphDatabase.driver(SOURCE_DB_URI, auth=(SOURCE_DB_USER, SOURCE_DB_PASSWORD))
source_session = source_driver.session()

# Conectar a la base de datos de destino
target_driver = GraphDatabase.driver(TARGET_DB_URI, auth=(TARGET_DB_USER, TARGET_DB_PASSWORD))
target_session = target_driver.session()

# Función para copiar nodos
def copy_nodes():
    print("Copiando nodos...")
    result = source_session.run("MATCH (n) RETURN n")
    for record in result:
        node = record["n"]
        labels = ":".join(node.labels)
        properties = {k: v for k, v in node.items()}
        properties_string = ", ".join([f"{k}: ${k}" for k in properties.keys()])
        merge_query = f"""
        MERGE (n:{labels} {{id: $id}})
        ON CREATE SET {properties_string}
        ON MATCH SET {properties_string}
        """
        target_session.run(merge_query, **properties)

# Función para copiar relaciones
def copy_relationships():
    print("Copiando relaciones...")
    result = source_session.run("MATCH ()-[r]->() RETURN r")
    for record in result:
        relationship = record["r"]
        start_node_id = relationship.start_node.id
        end_node_id = relationship.end_node.id
        rel_type = relationship.type
        properties = {k: v for k, v in relationship.items()}
        properties_string = ", ".join([f"{k}: ${k}" for k in properties.keys()])
        merge_query = f"""
        MATCH (a), (b)
        WHERE id(a) = {start_node_id} AND id(b) = {end_node_id}
        MERGE (a)-[r:{rel_type}]->(b)
        ON CREATE SET {properties_string}
        ON MATCH SET {properties_string}
        """
        target_session.run(merge_query, **properties)


# Ejecutar las funciones para hacer la copia espejo

copy_nodes()
copy_relationships()

# Cerrar las conexiones
source_session.close()
source_driver.close()
target_session.close()
target_driver.close()

print("Copia espejo completada exitosamente.")
