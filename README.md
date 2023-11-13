This repository is a challenge for the Data Engineer role, which uses the following technologies and services: 

- [x] GCP cloud
    - GCS (Google Cloud Storage)
    - Cloud Run
    - Bigquery
    - Composer (optional) 
- [x] Python 3.x
- [x] Flask_RESTful API
- [x] Pandas


>```env
>|- api/ Application module (API REST)
>| |- resources/             folder containing the classes defined in each of the endpoints
>| |- |.. incidentes.py            definition of the endpoints for /api/incidentes/<int:fecha>  
>| |- utils/                 folder contains utility functions 
>| |- |.. utils.py           
>| |- app.py           main project file
>| |- requirements.txt         Libraries to install 
>|- airflow/  contains dag and airflow configurations
>|- airflow/dags/orquestador_dag.py  dag to all pipeline
>|- data/csv/.. .csv files
>|- data/ddl/.. .sql ddl files
>|- data/dml/.. .sql dml files
>|- data/schema/.. json schemas for BQ
>|- doc/.. Documentions
>|.. .gitignore
>|.. README.md
>```

# Architeceture: 

# Pre requeriments: 
- [X] Have Docker and Docker Compose Installed
- [X] Have Airflow with docker or Composer Instance
- [X] Have a GCP Account
- [X] for GCP:
    - Create a Service Account with these roles: 
        - BigQuery Admin
        - Composer Administrator
        - Storage Admin
        - Storage Object Admin
    - Generate service account JSON key

    # QuickStart

    >```shell
>python -m venv .venv
>
>```

The virtual environment should be activated every time you start a new shell session before running subsequent commands:

> On Linux/MacOS:
> ```shell
> source .venv/bin/activate
> ```

> On Windows:
> ```shell
> .venv\Scripts\activate.bat
> ```

set the GOOGLE_APPLICATION_CREDENTIALS variable
> On Linux/MacOS:
> ```
> export GOOGLE_APPLICATION_CREDENTIALS=/path/with/json_key.json
> ```

> On Windows:
> ```
> $env:GOOGLE_APPLICATION_CREDENTIALS='/path/with/json_key.json'
> ```

set the GCS_BUCKET variable
> On Linux/MacOS:
> ```
> export GCS_BUCKET=bucket_name
> ```

> On Windows:
> ```
> $env:GCS_BUCKET='prueba-da-dw-01'
> ```

set the DATASET variable
> On Linux/MacOS:
> ```
> export DATASET=wr8u-xric
> ```

> On Windows:
> ```
> $env:DATASET='wr8u-xric'
> ```

set the URL variable
> On Linux/MacOS:
> ```
> export URL=data.sfgov.org
> ```

> On Windows:
> ```
> $env:URL='data.sfgov.org'
> ```

### Run API

locate us inside the api folder: 
> ```
> cd api
> ```

install dependencies.
> ```
> pip install -r requirements.txt
> ```

run locally
> ```
> python app.py 
> ```

curls to locally test 
> ```
> curl --location 'http://127.0.0.1:8081/api/v1/incidentes/20231112' \
> --header 'Content-Type: text/plain' \
> --data '@'
> ```

#### Cloud RUN (API):

create Image to container register: 
> ```
> gcloud builds submit --tag gcr.io/prueba-da-dw/flask-api-incidentes
> ```

deploy Api with Cloud Run:
> ```
> gcloud run deploy api-incidentes --image=gcr.io/prueba-da-dw/flask-api-incidentes --timeout=1500 
> ```


update variables to Api :
> ```
> gcloud run deploy api-incidentes \
> --image=gcr.io/prueba-da-dw/flask-api-incidentes \
> --cpu=4 \
> --memory=4Gi \
> --max-instances=20 \
> --set-env-vars=PROJECT_ID=prueba-da-dw,DATASET=wr8u-xric,GCS_BUCKET=prueba-da-dw-01,URL=data.sfgov.org \
> --region=us-east1 \
> --project=prueba-da-dw \
>  && gcloud run services update-traffic api-incidentes --to-latest
> ```

### Configure Airflow

To deploy Airflow on Docker Compose, you should fetch docker-compose.yaml.
> ```shell
>curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.6.3/docker-compose.yaml'
> ```

create folders base
> ```shell
> mkdir -p ./dags ./logs ./plugins ./config
> echo -e "AIRFLOW_UID=$(id -u)" > .env
> ```

Initialize the database

> ```shell
> docker compose up airflow-init
> ```

go to the url http://127.0.0.1:8080/home in your browser
login and password : airflow

for more informacion: https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html

Configure Connection: 
You need a connection to the BQ and GCP Storage services, so go to the `Admin->Connection` path and create a connection and type `GCP providers`, there load the `json key` created previously. 

Configure Variable: 
you also need to load the variables used by the different dags, so go to `Admin->Variables` and load the `variable.json` file found in the `dags` folder.


### GCP Usage

#### BiQuery:

> ```shell
> bq mk --table --schema incidentes.json prueba-da-dw:raw.incidentes 
> ```

The raw dataset must be created for the project. 
