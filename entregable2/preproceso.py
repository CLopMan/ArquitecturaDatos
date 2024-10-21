import sys
import pandas as pd
from pyscripts.encuestas_satisfaccion import *
from pyscripts.preproceso_incidencias_usuario import *
from pyscripts.preproceso_incidencias_seguridad import *

def main():
    if len(sys.argv) != 3:
        print(f'[ERROR] Uso: python3 {sys.argv[0]} <directorio de entrada>/ <directorio de salida>/')
        return
    
    input_path = sys.argv[1]
    output_path = sys.argv[2]

    # Call functions from imported modules
    encuestas_satisfaccion(input_path,output_path)
    preproceso_incidencias_usuario(input_path,output_path)
    preproceso_incidencias_seguridad(input_path,output_path)


""" def main_2():
    if len(sys.argv) != 3:
        print(f'[ERROR] Uso: python3 {sys.argv[0]} <directorio de entrada> <directorio de salida>')
        return
    
    input_path = sys.argv[1]
    output_path = sys.argv[2]

    areas_df = pd.read_csv(input_path + "AreasSucio.csv")
    encuestas_df = pd.read_csv(input_path + "EncuestasSatisfaccionSucio.csv")
    incidencias_usuario_df = pd.read_csv(input_path + "IncidenciasUsuarioSucio.csv")
    incidentes_seguridad_df = pd.read_csv(input_path + "IncidentesSeguridadSucio.csv")
    juegos_df = pd.read_csv(input_path + "JuegosSucios.csv")
    mantenimiento_df = pd.read_csv(input_path + "MantenimientoSucio.csv")
    meteo_df = pd.read_csv(input_path + "meteo24.csv")
    usuarios_df = pd.read_csv(input_path + "UsuariosSucio.csv")


    encuestas_df = encuestas_satisfaccion(encuestas_df)
    incidencias_usuario_df = preproceso_incidencias_usuario(incidencias_usuario_df)
    incidentes_seguridad_df = preproceso_incidencias_seguridad(incidentes_seguridad_df)    
 """
if __name__ == "__main__":
    main()

