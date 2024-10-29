import pandas as pd

def encuestas_satisfaccion(source, dest):
    PATH = source + "EncuestasSatisfaccionSucio.csv"
    PATH_OUT = dest + "encuestas_satisfaccion_limpio.csv"

    df = pd.read_csv(PATH)

    df["FECHA"] = pd.to_datetime(df["FECHA"], format="mixed", dayfirst=True).dt.strftime("%d-%m-%Y")
    df[column] = df[column].str.upper()
    df.to_csv(PATH_OUT)
    
if __name__ == "__main__":
    encuestas_satisfaccion("../csvs/EcuestasSatisfaccionSucio.csv")
