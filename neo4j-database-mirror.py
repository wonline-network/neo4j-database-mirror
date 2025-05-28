# Wonline - Configuración de la migración de base de datos neo4j comunity edition
# Autor: Angel Luis
# Versión: 1.0.0
# Web: https://wonline.network
# Año: 2023

from neo4j import GraphDatabase
from dotenv import load_dotenv
import os

# Cargar las variables de entorno
load_dotenv()

# Credenciales y URLs de las instancias Neo4j
SOURCE_DB_URI = os.getenv("SOURCE_DB_URI")
SOURCE_DB_USER = os.getenv("SOURCE_DB_USER")
SOURCE_DB_PASSWORD = os.getenv("SOURCE_DB_PASSWORD")

TARGET_DB_URI = os.getenv("TARGET_DB_URI")
TARGET_DB_USER = os.getenv("TARGET_DB_USER")
TARGET_DB_PASSWORD = os.getenv("TARGET_DB_PASSWORD")

try:
    # Conectar a la base de datos de origen
    source_driver = GraphDatabase.driver(SOURCE_DB_URI, auth=(SOURCE_DB_USER, SOURCE_DB_PASSWORD))
    source_session = source_driver.session()

    # Conectar a la base de datos de destino
    target_driver = GraphDatabase.driver(TARGET_DB_URI, auth=(TARGET_DB_USER, TARGET_DB_PASSWORD))
    target_session = target_driver.session()

    # Función para eliminar todos los datos en la base de datos de destino
    def clear_target_db():
        target_session.run("MATCH (n) DETACH DELETE n")

    # Función para copiar nodos
    def copy_nodes():
        print("Copia copy_nodes.")
        result = source_session.run("MATCH (n) RETURN n")
        for record in result:
            node = record["n"]
            properties = node.items()
            create_query = f"CREATE (n:{':'.join(node.labels)} {{{', '.join([f'{k}: ${k}' for k in node.keys()])}}})"
            target_session.run(create_query, **node)

    # Función para copiar relaciones
    def copy_relationships():
        print("Copia copy_relationships")
        result = source_session.run("MATCH ()-[r]->() RETURN r")
        for record in result:
            relationship = record["r"]
            start_node_id = relationship.start_node.id
            end_node_id = relationship.end_node.id
            properties = relationship.items()
            create_query = (
                f"MATCH (a), (b) WHERE id(a) = {start_node_id} AND id(b) = {end_node_id} "
                f"CREATE (a)-[r:{relationship.type} {{{', '.join([f'{k}: ${k}' for k in relationship.keys()])}}}]->(b)"
            )
            target_session.run(create_query, **relationship)

    # Ejecutar las funciones para hacer la copia espejo
    clear_target_db()
    copy_nodes()
    copy_relationships()

except Exception as e:
    print(f"Ha ocurrido un error: {e}")

finally:
    # Cerrar las conexiones
    source_session.close()
    source_driver.close()
    target_session.close()
    target_driver.close()

print("Copia espejo completada exitosamente.")