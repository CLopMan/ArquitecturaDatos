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
    print(f'[INFO] Actualizando {column} a mayúsculas y elimninando tildes') 
    df[column] = df[column].str.upper().apply(change_accents)
    
def imput_missing_district(df):
    columnA = "DISTRITO"
    columnB = "COD_DISTRITO"
    print(f'[INFO] Imputando valores faltantes en {columnA} y {columnB}') 
    distritos = {} # relates distrito - cod_distrito bidirectional
    for row in df['DISTRITO']:
        if row not in distritos.keys():
            distritos[row] = None
    for index, row in df.iterrows():
        if row['DISTRITO'] is not None:
            if distritos[row['DISTRITO']] == None and row['COD_DISTRITO'] != None:
                distritos[row['DISTRITO']] = row['COD_DISTRITO']
                distritos[row['COD_DISTRITO']] = row['DISTRITO']
    # print(distritos)
    for d in distritos.keys():
        if (type(d) == str):
                df.loc[df['DISTRITO'] == d, 'COD_DISTRITO'] = distritos[d]
        elif (type(d) == int):
                df.loc[df['COD_DISTRITO'] == d, 'DISTRITO'] = distritos[d]


def juegos(source, dest):
    df = pd.read_csv(source) 
    
    # analisis csv
    print(df)
    print(df.describe())

    # missing_values
    missing = detect_missing_values(df)
    if missing.sum() > 0:
        print("[INFO] Existen valores nulos: ", missing.sum()) 
        print("\n")
        print(missing)
    else: 
        print("[INFO] No existen valores nulos")
    
    # correcting strings
    for c in df.columns.to_list():
        if (df[c].dtype == object):
           standarize_str(df, c) 

    # imputacion cod_distrito y distrito
    imput_missing_district(df)
    # print(df.groupby(['DISTRITO'])['COD_DISTRITO'].unique())


if __name__ == "__main__":
    juegos("../csvs/JuegosSucio.csv", "../juegos_limpio.csv")
    
    



