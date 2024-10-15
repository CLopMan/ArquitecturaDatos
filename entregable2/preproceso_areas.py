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

def preproceso_area():
    areas = pd.read_csv("AreasSucio.csv")

    # Cambiamos los nombres de los Barrios para estandarizarlos
    for indice, valor in areas.iterrows():
        barrio = change_accents(valor["BARRIO"].upper())
        areas.loc[indice, "BARRIO"] = barrio

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
                
                # Si no existe nombre, conseguimos los datos de la dirección auxiliar
                if not pd.notna(nom_via):
                    try:
                        areas.loc[indice, "NOM_VIA"] = dir_aux[0:dir_aux.index(',')-1].upper()
                    except:
                        areas.loc[indice, "NOM_VIA"] = dir_aux[0:].upper()
                    try:
                        areas.loc[indice, "NOM_VIA"] = areas.loc[indice, "NOM_VIA"][areas.loc[indice, "NOM_VIA"].index('·') + 2:].upper()
                    except ValueError:
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

    # Formateo de fechas            
    for indice, value in areas.iterrows():
        if value["FECHA_INSTALACION"] == "fecha_incorrecta":
            areas.loc[indice, "FECHA_INSTALACION"] = ""
    
    areas["FECHA_INSTALACION"] = pd.to_datetime(areas["FECHA_INSTALACION"], format="mixed", dayfirst=True).dt.strftime("%d-%m-%Y")


    
if __name__=="__main__":
    preproceso_area()