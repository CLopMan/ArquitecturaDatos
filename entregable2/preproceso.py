import sys
import warnings
import pandas as pd
from datetime import datetime

def change_accents(word):
    if type(word) != str:
        #print("[WARNING] word no es una string", word)
        return
    for letter in range(len(word)):
        if word[letter] == "Á":
            word = word[0:letter] + "A" + word[letter + 1:]
        if word[letter] == "É":
            word = word[0:letter] + "E" + word[letter + 1:]
        if word[letter] == "Í":
            word = word[0:letter] + "I" + word[letter + 1:]
        if word[letter] == "Ó":
            word = word[0:letter] + "O" + word[letter + 1:]
        if word[letter] == "Ú":
            word = word[0:letter] + "U" + word[letter + 1:]
    return word

def detect_missing_values(df):
    missing: bool = df.isnull().sum()
    return missing

def standarize_str(df, column):
    #print(f'[INFO] Actualizando {column} a mayúsculas y elimninando tildes')
    df[column] = df[column].str.upper().apply(change_accents)
    df[column] = df[column].str.rstrip()
    df[column] = df[column].str.lstrip()    

def imput_missing_district(df):
    columnA = "DISTRITO"
    columnB = "COD_DISTRITO"
    #print(f'[INFO] Imputando valores faltantes en {columnA} y {columnB}') 
    distritos = {} # relates distrito - cod_distrito bidirectional
    for row in df['DISTRITO']:
        if row not in distritos.keys():
            distritos[row] = None
    for index, row in df.iterrows():
        if row['DISTRITO'] is not None:
            if distritos[row['DISTRITO']] == None and row['COD_DISTRITO'] != None:
                distritos[row['DISTRITO']] = row['COD_DISTRITO']
                distritos[row['COD_DISTRITO']] = row['DISTRITO']
    #print(distritos)
    for d in distritos.keys():
        if (type(d) == str):
            df.loc[df['DISTRITO'] == d, 'COD_DISTRITO'] = distritos[d]
        elif (type(d) == float):
            df.loc[df['COD_DISTRITO'] == d, 'DISTRITO'] = distritos[d]

def parse_dir_aux(dir_aux, ID):
    out = {
        "via"        : "",
        "nombre_via" : "",
        "num_via"    : ""
    }
    patrones = [ 
                 "PARQUE", "CALLE", "C", "PLAZA", "VIA", "PASAJE", "PJE",
                 "PASEO", "AUTOVIA",  "AUTOV", "AVENIDA", "AVDA", "AV", 
                 "RONDA", "RDA","PLAZA", "PZA", "PARQUE", "JAR"
               ]
    separators = " ,·;:/-"
    # Get Tipo_Via
    word = ""
    i = 0
    state = "via"
    name = ""
    num = ""
    while i < len(dir_aux):
        word = ""
        name = ""
        while i < len(dir_aux) and dir_aux[i] not in separators:
            word += dir_aux[i]
            i += 1
        # #print(word, len(word))
        i += 1
        # Get via type
        if state == "via":
            try:
                tipo_via_ix = patrones.index(word)
                match tipo_via_ix:
                    case 2:
                        tipo_via_ix = 1
                    case 6:
                        tipo_via_ix = 5
                    case 9:
                        tipo_via_ix = 8
                    case 11:
                        tipo_via_ix = 10
                    case 12:
                        tipo_via_ix = 10
                    case 14:
                        tipo_via_ix = 13
                    case 16:
                        tipo_via_ix = 15
                    case 18:
                        tipo_via_ix = 17
                    case _:
                        pass

                out["via"] = patrones[tipo_via_ix]
                word = ""
            except ValueError as e:
                # no existe el tipo de la via
                out["via"] = None
            state = "nombre_via"
        if state == "nombre_via":
            if not word.isdigit() and "Nº" not in word:
                name += word + " "
                out["nombre_via"] += word + " "
            else:
                state = "num_via"
            
        if state == "num_via":
            if "Nº" in word:
                # get num from word
                for c in word:
                    if c in "0123456789":
                        num += c
                if len(num) > 0:    
                    num = str(int(num)) # delete unnecesary 0's
            if len(num) == 0:
                # search for the first num
                 if (word.isdigit()):
                    num = str(int(word))
            if len(num) > 0:
                out["num_via"] = num

    out["nombre_via"] = out["nombre_via"].rstrip()
    out["nombre_via"] = out["nombre_via"].lstrip()
    out["num_via"] = out["num_via"] if len(out["num_via"]) > 0 else None
    return out


def imput_missing_addr(df):
    #print(f'[INFO] Imputando valores faltantes en TIPO_VIA, NUM_VIA y NOM_VIA') 
    for indice, valor in df.iterrows():
        tipo_via = valor["TIPO_VIA"]
        nom_via = valor["NOM_VIA"]
        num_via = valor["NUM_VIA"]
        dir_aux = valor["DIRECCION_AUX"]
        if dir_aux is not None:
            dir_aux = parse_dir_aux(dir_aux.upper(), valor["ID"])
            df.loc[indice, ["TIPO_VIA"]] = dir_aux["via"] if not tipo_via else tipo_via
            df.loc[indice, ["NOM_VIA"]] = dir_aux["nombre_via"] if not nom_via else nom_via
            df.loc[indice, ["NUM_VIA"]] = dir_aux["num_via"] if not num_via else num_via

def fill_dates(df):
    df.loc[(df["FECHA_INSTALACION"] == "fecha_incorrecta") |
    (df["FECHA_INSTALACION"].isna()), 'FECHA_INSTALACION'] = "1970-01-01T00:00:00Z"


def fussion_df(df1, df2, columnas_clave, new_column):
    df1[new_column] = None
    for i, row in df2.iterrows():
        condition = False
        for key in columnas_clave:
            condition |= (df1[key] == row[key])
        #print(condition)

        df1.loc[condition, new_column] = row["ID"] # rows de juegos
        for c in df1.columns.tolist(): # copiar valores faltantes del uno al otro
            if c in df2.columns.tolist():
                if row[c] is not None:
                    with warnings.catch_warnings(record=True) as w:
                        warnings.simplefilter("ignore")
                        if pd.isna(df1.loc[condition, c]).all(): 
                            df1.loc[df1[new_column] == row["ID"], c] = row[c]
                else:
                    for j, r in df1.interrows():
                        if not pd.isna(r[c]) and pd.isna(df2.loc[i, c]):
                            df2.loc[i, c] = r[c] # actualizamos al primero
                            break

def fill_missing_tipo(row,column,string_missing, id_row):
    if pd.isnull(row[column]):
        return f'{string_missing}_{row[id_row]}'
    return row[column]


def fill_missing(df, optionals:list):
    for c in df.columns.tolist():
        if c not in optionals:
            df[c] = df.apply(lambda row: fill_missing_tipo(row, c, f'{c}_DESCONOCIDO', "ID"), axis=1)
    return df


def preproceso_juegos(source, dest):
    optionals = ["DIRECCION_AUX"]
    source += "JuegosSucio.csv"
    dest_csv = dest + "juegos_limpio.csv"
    df = pd.read_csv(source) 
    # correcting strings
    for c in df.columns.to_list():
        if (df[c].dtype == object):
           standarize_str(df, c)
    # Correcting dates
    fill_dates(df)

    # imputacion de valores en el propio df
    imput_missing_district(df)
    imput_missing_addr(df)

    # fusion con Area
    df_areas = pd.read_csv(dest + "areas_limpias.csv")
    fussion_df(df, df_areas, ["CODIGO_INTERNO", "NDP"], "AREA") 
    df = fill_missing(df, optionals)
    df_areas = fill_missing(df_areas, optionals)
    df.to_csv(dest_csv, index=False)
    df_areas.to_csv(dest + "areas_limpias.csv", index=False)

def preproceso_area(csv_input, csv_output):
    csv_input = csv_input + "AreasSucio.csv"
    csv_output = csv_output + "areas_limpias.csv"

    # Leemos las areas
    areas = pd.read_csv(csv_input)

    # Estandarizar la descripción de la clasificación
    for indice, valor in areas.iterrows():
        areas.loc[indice, "DESC_CLASIFICACION"] = change_accents(valor["DESC_CLASIFICACION"].upper())

    # Cambiamos los nombres de los Barrios para estandarizarlos
    zips_por_barrio = {}
    for indice, valor in areas.iterrows():
        barrio = change_accents(valor["BARRIO"].upper())
        areas.loc[indice, "BARRIO"] = barrio
        
        # Guardamos el codigo postal del barrio
        cod_postal = valor["COD_POSTAL"]
        if pd.notna(cod_postal) and cod_postal != 0.0:
            zips_por_barrio[barrio] = cod_postal

    # Rellenamos los Códigos Postales que falten
    for indice, valor in areas.iterrows():
        barrio = valor["BARRIO"]
        areas.loc[indice, "COD_POSTAL"] = zips_por_barrio[barrio]

    # Cambiamos los nombres de los Distrito para estandarizarlos
    codigos_por_distritos = {}
    distritos_por_codigo = {}
    for indice, valor in areas.iterrows():
        distrito = valor["DISTRITO"]
        codigo = valor["COD_DISTRITO"]
        if pd.notna(distrito):
            distrito = change_accents(valor["DISTRITO"].upper())
            areas.loc[indice, "DISTRITO"] = distrito
            if pd.notna(codigo):
                codigos_por_distritos[distrito] = codigo
                distritos_por_codigo[codigo] = distrito
    
    # Rellenamos los datos faltantes para los distritos y sus códigos
    for indice, valor in areas.iterrows():
        distrito = valor["DISTRITO"]
        codigo = valor["COD_DISTRITO"]
        if not pd.notna(distrito):
            areas.loc[indice, "DISTRITO"] = distritos_por_codigo[codigo]
        if not pd.notna(codigo):
            areas.loc[indice, "COD_DISTRITO"] = codigos_por_distritos[distrito]

    # Rellenamos los datos de las vías que sean nulos
    for indice, valor in areas.iterrows():
        tipo_via = valor["TIPO_VIA"]
        nom_via = valor["NOM_VIA"]
        num_via = valor["NUM_VIA"]
        dir_aux = valor["DIRECCION_AUX"]
        
        # Si no hay tipo de vía
        if not pd.notna(tipo_via):
            # Si existe dirección auxiliar, cogemos el tipo a partir de la dirección auxiliar
            if pd.notna(dir_aux):
                dir_aux = dir_aux.lower()
                if ("parque" in dir_aux):
                    areas.loc[indice, "TIPO_VIA"] = "PARQUE"
                elif ("avda" in dir_aux or "avenida" in dir_aux):
                    areas.loc[indice, "TIPO_VIA"] = "AVENIDA"
                elif ("calle" in dir_aux or "sous" in dir_aux) :
                    areas.loc[indice, "TIPO_VIA"] = "CALLE"
                elif ("plaza" in dir_aux):
                    areas.loc[indice, "TIPO_VIA"] = "PLAZA"
                elif ("via" in dir_aux):
                    areas.loc[indice, "TIPO_VIA"] = "VIA"
                elif ("pje" in dir_aux):
                    areas.loc[indice, "TIPO_VIA"] = "PAISAJE"
                elif ("paseo" in dir_aux):
                    areas.loc[indice, "TIPO_VIA"] = "PASEO"
            else:
                areas.loc[indice, "TIPO_VIA"] = "tipo_desconocido_" + str(areas.loc[indice, "ID"])
            
        # Si no existe nombre, conseguimos los datos de la dirección auxiliar
        if not pd.notna(nom_via):
            if pd.notna(dir_aux):
                dir_aux = dir_aux.lower()
                try:
                    areas.loc[indice, "NOM_VIA"] = dir_aux[0:dir_aux.index(',')-1].upper()
                except:
                    areas.loc[indice, "NOM_VIA"] = dir_aux[0:].upper()
                try:
                    areas.loc[indice, "NOM_VIA"] = areas.loc[indice, "NOM_VIA"][areas.loc[indice, "NOM_VIA"].index('·') + 2:].upper()
                except ValueError as e:
                    pass

                # Si no tiene número, lo conseguimos de la vía auxiliar
                if not pd.notna(num_via):
                    first_index = True
                    try:
                        indice_num = dir_aux.index(',') - 2
                        num = ""
                        while(indice_num >= 0 and dir_aux[indice_num] in "1234567890"):
                            num = dir_aux[indice_num] + num 
                            indice_num -= 1
                        if num == "":
                            first_index = False
                        else:
                            areas.loc[indice, "NUM_VIA"] = num
                            local_nom = areas.loc[indice, "NOM_VIA"]
                            indice_nom = len(local_nom) - 1
                            while (local_nom[indice_nom] in "1234567890º"):
                                if (local_nom[indice_nom] == "º"):
                                    indice_nom -= 1
                                indice_nom -= 1
                            areas.loc[indice, "NOM_VIA"] = local_nom[0:indice_nom]
                    except ValueError:
                        first_index = False  
                    if not first_index:
                        try:  
                            indice_num = dir_aux.index(':') + 2
                            num = ""
                            while(indice_num < len(dir_aux) and dir_aux[indice_num] in "1234567890"):
                                num += dir_aux[indice_num] 
                                indice_num += 1
                            if num != "":
                                areas.loc[indice, "NUM_VIA"] = int(num)
                        except ValueError:
                            pass
                    # Borramos la dirección auxiliar
                    areas.loc[indice, "DIRECCION_AUX"] = ""
            else:
                areas.loc[indice, "NOM_VIA"] = "NOMBRE_DESCONOCIDO_" + str(areas.loc[indice, "ID"])
                areas.loc[indice, "NUM_VIA"] = "NUMERO_DESCONOCIDO_" + str(areas.loc[indice, "ID"])

        if not pd.notna(num_via):
            areas.loc[indice, "NUM_VIA"] = "NUMERO_DESCONOCIDO_" + str(areas.loc[indice, "ID"])
            

    # Formateo de fechas            
    for indice, value in areas.iterrows():
        if not pd.notna(value["FECHA_INSTALACION"]) or value["FECHA_INSTALACION"] == "fecha_incorrecta":
            areas.loc[indice, "FECHA_INSTALACION"] = "1970-01-01T00:00:00Z"
    
    areas["FECHA_INSTALACION"] = pd.to_datetime(areas["FECHA_INSTALACION"],
    format="mixed", dayfirst=True, utc=True).dt.strftime('%Y-%m-%dT%H:%M:%SZ')

    # Formateo de codigo_interno
    areas["CODIGO_INTERNO"] = areas.apply(lambda row: fill_missing_tipo(row, "CODIGO_INTERNO", "CODIGO_DESCONOCIDO", "ID"), axis=1)

    # Formateo de tipo
    areas["tipo"] = areas["tipo"].str.upper()

    areas.to_csv(csv_output, index=False)

def encuestas_satisfaccion(source, dest):
    PATH = source + "EncuestasSatisfaccionSucio.csv"
    PATH_OUT = dest + "encuestas_satisfaccion_limpio.csv"

    df = pd.read_csv(PATH)

    df["FECHA"] = pd.to_datetime(df["FECHA"], utc=True, format="mixed", dayfirst=True).dt.strftime('%Y-%m-%dT%H:%M:%SZ')
    column = "COMENTARIOS"
    df[column] = df[column].str.upper()
    df.to_csv(PATH_OUT, index=False)
 
def preproceso_incidencias_usuario(csv_input, csv_output):
    csv_input = csv_input + "IncidenciasUsuariosSucio.csv"
    csv_output = csv_output + "incidencias_usuarios_limpio.csv"
    df = pd.read_csv(csv_input)
    df["TIPO_INCIDENCIA"] = df["TIPO_INCIDENCIA"].str.upper()
    df["FECHA_REPORTE"] = pd.to_datetime(df["FECHA_REPORTE"], format="mixed",
    dayfirst=True, utc=True).dt.strftime('%Y-%m-%dT%H:%M:%SZ')
    df["ESTADO"] = df["ESTADO"].str.upper()

    df.to_csv(csv_output, index=False)

def preproceso_incidencias_seguridad(csv_input, csv_output):
    csv_input = csv_input + "IncidentesSeguridadSucio.csv"
    csv_output = csv_output + "incidentes_seguridad_limpio.csv"

    df = pd.read_csv(csv_input)
    df["FECHA_REPORTE"] = pd.to_datetime(df["FECHA_REPORTE"],
    format="mixed",utc=True, dayfirst=True).dt.strftime('%Y-%m-%dT%H:%M:%SZ')
    df["TIPO_INCIDENTE"] = df["TIPO_INCIDENTE"].str.upper().apply(change_accents)
    df["GRAVEDAD"] = df["GRAVEDAD"].str.upper().apply(change_accents)

    df.to_csv(csv_output, index=False)

def preproceso_mantenimiento(csv_input, csv_output):
    csv_input = csv_input + "MantenimientoSucio.csv"
    csv_output = csv_output + "mantenimiento_limpio.csv"

    df = pd.read_csv(csv_input)
    df["TIPO_INTERVENCION"] = df["TIPO_INTERVENCION"].str.upper()
    df["FECHA_INTERVENCION"] = pd.to_datetime(df["FECHA_INTERVENCION"],
    format="mixed", dayfirst=True, utc=True).dt.strftime('%Y-%m-%dT%H:%M:%SZ')
    df["ESTADO_PREVIO"] = df["ESTADO_PREVIO"].str.upper()
    df["ESTADO_POSTERIOR"] = df["ESTADO_POSTERIOR"].str.upper()

    df["Tipo"] = df.apply(lambda row: fill_missing_tipo(row, "Tipo", "TIPO_DESCONOCIDO", "ID"), axis=1)
    df["Tipo"] = df["Tipo"].str.upper()

    df["Comentarios"] = df["Comentarios"].str.upper()
    df["Comentarios"] = df.apply(lambda row: fill_missing_tipo(row, "Comentarios", "COMENTARIO_DESCONOCIDO", "ID"), axis=1)

    df.to_csv(csv_output, index=False)

def preproceso_meteo24(csv_input, csv_output):
    meteo_csv = csv_input + "meteo24.csv"
    csv_output = csv_output + "meteo24_limpio.csv"

    areas_csv = csv_input + "AreasSucio.csv"

    meteo = pd.read_csv(meteo_csv, delimiter=';')
    areas = pd.read_csv(areas_csv)
    
    new_meteo = pd.DataFrame(columns=["ID","FECHA","TEMPERATURA","PRECIPITACION","VIENTO","ESTACION"])

    magnitudes = {81:"VIENTO",83:"TEMPERATURA",89:"PRECIPITACION"}
    count_id = 1
    for _,row in meteo.iterrows():
        magnitud = row["MAGNITUD"]
        if magnitud in magnitudes:
            año = row["ANO"]
            mes = row["MES"]
            dia = 1
            estacion = row["ESTACION"]
            for dia in range(1,32):
                valor = row.iloc[7 + (dia - 1) * 2]
                fecha = f"{dia:02d}-{mes:02d}-{año}"

                # Verificar si ya existe una fila con la misma fecha e ID_AREA
                if not ((new_meteo["FECHA"] == fecha) & (new_meteo["ESTACION"] == estacion)).any():
                    # Crear una nueva fila
                    new_row = {"ID":count_id,"FECHA": fecha, "ESTACION": estacion, magnitudes[magnitud]: valor}
                    new_meteo.loc[len(new_meteo.index)] = new_row
                else:
                    # Actualizar la fila existente
                    new_meteo.loc[(new_meteo["FECHA"] == fecha) & (new_meteo["ESTACION"] == estacion), magnitudes[magnitud]] = valor
                count_id+=1
    new_meteo = new_meteo.astype(object)
    for i, row in new_meteo.iterrows():
        new_meteo.loc[i, 'VIENTO'] = 1 if row['VIENTO'] > 11.4 else 0
    fill_missing(new_meteo,[])

    new_meteo.to_csv(csv_output,index=False)

def preproceso_estaciones_meteo_codigo_postal(csv_input, csv_output):
    csv_input = csv_input + "estaciones_meteo_CodigoPostal.csv"
    csv_output = csv_output + "estaciones_meteo_codigo_postal.csv"

    input_csv = pd.read_csv(csv_input, delimiter=";")


    input_csv.at[0,"Codigo Postal"] = input_csv.at[0,"Codigo Postal"].split(',')[0]

    input_csv.to_csv(csv_output,index=False)


def format_phone_number(phone):
    phone = phone.replace(" ", "")
    if phone.startswith("+34"):
        phone = phone[3:]
    if phone.startswith("34"):
        phone = phone[2:]
    return phone

def preproceso_usuarios(csv_input, csv_output):
    csv_input = csv_input + "UsuariosSucio.csv"
    csv_output = csv_output + "usuarios_limpios.csv"
    df = pd.read_csv(csv_input)
    df["NOMBRE"] = df["NOMBRE"].str.upper()
    df["EMAIL"] = df["EMAIL"].str.upper()
    df["TELEFONO"] = df["TELEFONO"].apply(format_phone_number)
    df = df.drop(columns=["Email"])
    df["EMAIL"] = df.apply(lambda row: fill_missing_tipo(row, "EMAIL", "EMAIL_DESCONOCIDO", "NIF"), axis=1)

    df.to_csv(csv_output,index=False)

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
    preproceso_juegos(input_path, output_path)
    info_msg("executing preproceso_meteo24")
    preproceso_meteo24(input_path, output_path)
    info_msg("executing preprocese_estaciones_meteo_codigo_postal")
    preproceso_estaciones_meteo_codigo_postal(input_path,output_path)
    info_msg("FINISH")

if __name__ == "__main__":
    main()
