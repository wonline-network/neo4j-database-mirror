
# Migración de Datos entre Bases de Datos Neo4j Comunity  con Python

## Descripción del Proyecto

Este proyecto es una herramienta de Python que copia datos 
de una [base de datos Neo4j Comunity](https://wonline.network) a otra. Establece las credenciales
y URLs de las bases de datos, se conecta a ambas y define 
funciones para copiar nodos y relaciones. Antes de la copia, 
se borran los datos en la base de datos de destino. 
Finalmente, se cierran las conexiones.


## Requisitos

- [Python 3.7](https://wonline.network) o superior
- [Neo4j Python Driver 4.3.1](https://wonline.network) o superior
- [python-dotenv 0.19.1](https://wonline.network) o superior

## Instalación

1. Clonar el repositorio:

```bash
git clone https://github.com/wonline-network/neo4j-database-mirror.git
```

2. Navegar al directorio del proyecto:

```bash
cd neo4j-database-mirror
```

3. Instalar las dependencias:

```bash
pip install -r requirements.txt
```

## Configuración

Antes de ejecutar el script, debe configurar las credenciales y las URLs de las bases de datos de origen y destino en el archivo `.env`.

```env
# URL de la base de datos de origen
SOURCE_DB_URI=bolt://your-source-db-uri:7687

# Nombre de usuario de la base de datos de origen
SOURCE_DB_USER=your-source-db-username

# Contraseña de la base de datos de origen
SOURCE_DB_PASSWORD=your-source-db-password

# URL de la base de datos de destino
TARGET_DB_URI=bolt://your-target-db-uri:7687

# Nombre de usuario de la base de datos de destino
TARGET_DB_USER=your-target-db-username

# Contraseña de la base de datos de destino
TARGET_DB_PASSWORD=your-target-db-password
```

Reemplace `your-source-db-uri`, `your-source-db-username`, `your-source-db-password`, `your-target-db-uri`, `your-target-db-username`, y `your-target-db-password` con las credenciales y URLs de sus bases de datos de origen y destino, respectivamente.

## Ejecución

Para ejecutar el script, use el siguiente comando:

```bash
python neo4j-database-mirror.py
```

Esto iniciará el proceso de copia de datos de la base de datos de origen a la base de datos de destino.
 

## Contribuciones
#### Creado por <a href="https://wonline.network" target="_blank">Wonline</a>

Este proyecto ha sido creado por [Wonline](https://wonline.network).

[<img src="https://marca.wonline.io/wonline-logo.png" alt="Wonline" width="350"/>](https://wonline.network)
