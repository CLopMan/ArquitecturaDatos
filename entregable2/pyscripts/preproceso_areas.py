from math import isnan
import pandas as pd

def change_accents(word):
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

def fill_missing_tipo(row,column,string_missing):
    if pd.isnull(row[column]):
        return f'{string_missing}_{row["ID"]}'
    return row[column]

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
            areas.loc[indice, "FECHA_INSTALACION"] = "01/01/1970"
    
    areas["FECHA_INSTALACION"] = pd.to_datetime(areas["FECHA_INSTALACION"], format="mixed", dayfirst=True).dt.strftime("%d-%m-%Y")

    # Formateo de codigo_interno
    areas["CODIGO_INTERNO"] = areas.apply(lambda row: fill_missing_tipo(row, "CODIGO_INTERNO", "CODIGO_DESCONOCIDO"), axis=1)

    # Formateo de tipo
    areas["tipo"] = areas["tipo"].str.upper()

    areas.to_csv(csv_output, index=False)


    
if __name__=="__main__":
    preproceso_area("./csvs/", "./")
