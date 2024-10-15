import pandas as pd

def preproceso_incidencias_usuario():
    df = pd.read_csv("../csvs/IncidenciasUsuariosSucio.csv")
    df["TIPO_INCIDENCIA"] = df["TIPO_INCIDENCIA"].str.upper()
    df["FECHA_REPORTE"] = pd.to_datetime(df["FECHA_REPORTE"], format="mixed", dayfirst=True).dt.strftime("%d-%m-%Y")
    df["ESTADO"] = df["ESTADO"].str.upper()

preproceso_incidencias_usuario()