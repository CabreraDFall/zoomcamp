# NYC Taxi Dataset Ingestion

## The NYC Taxi Dataset
We will use data from the [NYC TLC Trip Record Data](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page) website.

Specifically, we will use the **Yellow taxi trip records CSV** file for January 2021.

### Why CSV?
Aunque los datos ahora se proporcionan principalmente en formato Parquet, queremos seguir usando **CSV** para este ejercicio porque necesitamos realizar pasos adicionales de preprocesamiento, lo cual es valioso para fines de aprendizaje.

## Reading a Sample of the Data
Puedes usar el siguiente código Python (que se encuentra en [notebook.ipynb](../pipeline/notebook.ipynb)) para leer las primeras 100 filas del conjunto de datos:

```python
import pandas as pd

prefix = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/'
df = pd.read_csv(prefix + 'yellow_tripdata_2021-01.csv.gz', nrows=100)
```

## Installing Database Dependencies

To interact with the PostgreSQL database, we need `SQLAlchemy` and `psycopg`. You can install them using `uv`.

If you are working in a Jupyter Notebook, you can run the following command directly in a notebook cell:

```bash
!uv add sqlalchemy "psycopg[binary,pool]"
```

This ensures that the dependencies are added to your project's virtual environment.

## Data Dictionary
Hay un diccionario disponible para entender cada campo aquí:
[Yellow Trip Records Data Dictionary (PDF)](https://www.nyc.gov/assets/tlc/downloads/pdf/data_dictionary_trip_records_yellow.pdf)
