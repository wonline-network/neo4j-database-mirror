# Wonline - Configuración de la migración de base de datos neo4j community edition
# Autor: Angel Luis
# Versión: 1.0.0
# Web: https://wonline.network
# Año: 2023

from neo4j import GraphDatabase
from dotenv import load_dotenv
import os
from tqdm import tqdm  # Para la barra de progreso

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

    # Función para copiar nodos con barra de progreso y ETA
    def copy_nodes():
        # Obtener total de nodos
        total_nodes = source_session.run("MATCH (n) RETURN count(n) AS c").single()["c"]
        print(f"Copiando {total_nodes} nodos...")
        result = source_session.run("MATCH (n) RETURN n")
        # Barras de progreso con tqdm
        for record in tqdm(result, total=total_nodes, desc="Nodos", unit="node"):
            node = record["n"]
            # Construir query de creación
            create_query = (
                f"CREATE (n:{':'.join(node.labels)} "
                f"{{{', '.join([f'{k}: ${k}' for k in node.keys()])}}})"
            )
            target_session.run(create_query, **node)

    # Función para copiar relaciones con barra de progreso y ETA
    def copy_relationships():
        # Obtener total de relaciones
        total_rels = source_session.run("MATCH ()-[r]->() RETURN count(r) AS c").single()["c"]
        print(f"Copiando {total_rels} relaciones...")
        result = source_session.run("MATCH ()-[r]->() RETURN r")
        for record in tqdm(result, total=total_rels, desc="Relaciones", unit="rel"):
            r = record["r"]
            start_id = r.start_node.id
            end_id = r.end_node.id
            create_query = (
                f"MATCH (a), (b) "
                f"WHERE id(a) = {start_id} AND id(b) = {end_id} "
                f"CREATE (a)-[rel:{r.type} "
                f"{{{', '.join([f'{k}: ${k}' for k in r.keys()])}}}]->(b)"
            )
            target_session.run(create_query, **r)

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
