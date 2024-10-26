import sys
from datetime import datetime
from pyscripts.encuestas_satisfaccion import *
from pyscripts.preproceso_incidencias_usuario import *
from pyscripts.preproceso_incidencias_seguridad import *
from pyscripts.preproceso_areas import *
from pyscripts.preproceso_mantenimiento import preproceso_mantenimiento
from pyscripts.preproceso_usuarios import *
from pyscripts.juegos import *

def info_msg(msg: str):
    print(f'[INFO: {datetime.now().strftime("%H:%M:%S")}] {msg}')

def main():
    if len(sys.argv) != 3:
        print(f'[ERROR] Uso: python3 {sys.argv[0]} <directorio de entrada>/ <directorio de salida>/')
        return
    
    input_path = sys.argv[1]
    output_path = sys.argv[2]

    # Call functions from imported modules
    info_msg("executing encuestas_satisfaccion")
    encuestas_satisfaccion(input_path,output_path)
    info_msg("executing preproceso_incidencias_de_usuario")
    preproceso_incidencias_usuario(input_path,output_path)
    info_msg("executing preproceso_incidencias_seguridad")
    preproceso_incidencias_seguridad(input_path,output_path)
    info_msg("executing preproceso_area")
    preproceso_area(input_path, output_path)
    info_msg("executing preproceso_mantenimiento")
    preproceso_mantenimiento(input_path, output_path)
    info_msg("executing preproceso_usuario")
    preproceso_usuarios(input_path, output_path)
    info_msg("executing juegos")
    juegos(input_path, output_path)
    info_msg("FINISH")

if __name__ == "__main__":
    main()
