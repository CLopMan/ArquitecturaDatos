import pandas as pd
import sys # argumentos de programa

def read_csv(path: str): 
    return pd.read_csv(path)

def detect_missing_values(df):
    missing: bool = df.isnull().sum()
    return missing

def standarize_date(df):
    # DD-MM-YYYY
    print("[INFO] Actualizando la fecha al formato dd-mm-yyyy") 
    df["FECHA"] = pd.to_datetime(df["FECHA"], format="mixed", dayfirst=True).dt.strftime("%d-%m-%Y")

def standarize_str(df):
    print("[INFO] Actualizando los comentarios a mayúsculas") 
    df["COMENTARIOS"] = df["COMENTARIOS"].str.upper()
        

def encuestas_satisfaccion(source, dest):
#    # program args
#    if len(sys.argv) < 3:
#        print(f'[ERROR] Usage: python3 {sys.argv[0]} source.csv dest.csv')
#        return -1
#    else:
#        PATH = sys.argv[1]
#        PATH_OUT = sys.argv[2]
    # data frame
    PATH = source + "EncuestasSatisfaccionSucio.csv"
    PATH_OUT = dest + "encuestas_satisfaccion_limpio.csv"

    df = read_csv(PATH)
    
    print(df)
    print(df["PUNTUACION_ACCESIBILIDAD"].describe())
    print(df["PUNTUACION_CALIDAD"].describe())

    missing = detect_missing_values(df)
    if missing.sum() > 0:
        print("[INFO] Existen valores nulos: ", missing.sum()) 
    else: 
        print("[INFO] No existen valores nulos")

    standarize_date(df)
    standarize_str(df)
    print("[INFO] Generating csv")
    df.to_csv(PATH_OUT)
    


if __name__ == "__main__":
    encuestas_satisfaccion()
