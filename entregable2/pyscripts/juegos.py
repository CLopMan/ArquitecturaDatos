import pandas as pd

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
    

def juegos(source, dest):
    source += "JuegosSucio.csv"
    dest += "JuegosLimpio.csv"
    df = pd.read_csv(source) 
    # analisis csv
    #print(df)
    #print(df.describe())

    # missing_values
    #missing = detect_missing_values(df)
    #if missing.sum() > 0:
    #    print("[INFO] Existen valores nulos: ", missing.sum()) 
    #    print("\n")
    #    print(missing)
    #else: 
    #    print("[INFO] No existen valores nulos")
    
    # correcting strings
    for c in df.columns.to_list():
        if (df[c].dtype == object):
           standarize_str(df, c)

    # imputacion cod_distrito y distrito
    imput_missing_district(df)
    imput_missing_addr(df)
    #print(df.groupby(['DISTRITO'])['COD_DISTRITO'].unique())
    #print(df['LONGITUD'].describe())



if __name__ == "__main__":
    juegos("./csvs/", "./output/")
