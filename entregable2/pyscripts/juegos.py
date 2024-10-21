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


if __name__ == "__main__":
    juegos("../csvs/JuegosSucio.csv", "../juegos_limpio.csv")
    



