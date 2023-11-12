from flask_restful import Api, Resource, reqparse
from sodapy import Socrata
import logging as logs
import pandas as pd
from utils.utils import UtilsFuntions as utilsFuntions
from google.cloud import storage
import os
from io import StringIO  

class Incidentes(Resource):
    section = 'incidentes'
    client = Socrata("data.sfgov.org", None)

    parser = reqparse.RequestParser()
    #parser.add_argument('fecha', type=self.fecha_valida, help='Fecha en formato YYYY-MM-DD', required=True, location='args')
    parser.add_argument('fecha', type=str, help='Fecha en formato YYYY-MM-DD')

    def fecha_valida(fecha_str):
        try:
            # Intenta parsear la fecha y verifica el formato
            datetime.strptime(fecha_str, '%Y-%m-%d')
            return fecha_str
        except ValueError:
            raise argparse.ArgumentTypeError("Formato de fecha inválido. Debe ser YYYY-MM-DD.")


    def get(self,fecha):
        logs.info("endpoint {}".format(self.section))
       
        dataset = os.environ["DATASET"]
        gcs_client = storage.Client()
        gcs_bucket = os.environ["GCS_BUCKET"]

        try:
            client = Socrata(os.environ["URL"], None)
            results = client.get_all(dataset)
            #results = client.get(dataset,limit=1000)
            # Convert to pandas DataFrame
            results_df = pd.DataFrame.from_records(results)
            filename= "{}-{}.csv".format(dataset, fecha)

            # Opcion Generando el Archivo .CSV en memoria
            f = StringIO()
            results_df.to_csv(f,encoding='utf-8', index=False)
            f.seek(0)
            gcs_response = utilsFuntions.save_file_from_io_to_gcs(filename, f, fecha, gcs_client,gcs_bucket )

            # Opcion Generando el Archivo .CSV localmente/ contenedor
            # results_df.to_csv(filename, sep=';', encoding='utf-8', index=False)
            # gcs_response = utilsFuntions.save_file_to_gcs(filename, fecha, gcs_client,gcs_bucket )

            
            return {'message': f'Registros Generados Correctamente, archivo: {filename}'} 
        except Exception as e:
            return {'message': f'Error al procesar el archivo: {str(e)}'}, 500