import sys
from pyscripts.encuestas_satisfaccion import *
from pyscripts.preproceso_incidencias_usuario import *
from pyscripts.preproceso_incidencias_seguridad import *
from pyscripts.preproceso_areas import *
from pyscripts.preproceso_mantenimiento import preproceso_mantenimiento
from pyscripts.preproceso_usuarios import *
from pyscripts.juegos import *

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
    preproceso_area(input_path, output_path)
    preproceso_mantenimiento(input_path, output_path)
    preproceso_usuarios(input_path, output_path)

if __name__ == "__main__":
    main()
