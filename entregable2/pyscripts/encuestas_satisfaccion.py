import pandas as pd

def read_csv(path: str): 
    return pd.read_csv(path)

def standarize_date(df):
    # DD-MM-YYYY
    df["FECHA"] = pd.to_datetime(df["FECHA"], format="mixed", dayfirst=True).dt.strftime("%d-%m-%Y")

def standarize_str(df, column):
    df[column] = df[column].str.upper()
        

def encuestas_satisfaccion(source, dest):
    PATH = source + "EncuestasSatisfaccionSucio.csv"
    PATH_OUT = dest + "encuestas_satisfaccion_limpio.csv"

    df = read_csv(PATH)

    standarize_date(df)
    standarize_str(df, "COMENTARIOS")
    df.to_csv(PATH_OUT)
    
if __name__ == "__main__":
    encuestas_satisfaccion("../csvs/EcuestasSatisfaccionSucio.csv")
