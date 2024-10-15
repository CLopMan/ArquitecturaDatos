import pandas as pd

def preproceso_incidencias_usuario(csv_input, cvs_output):
    df = pd.read_csv(csv_input)
    df["TIPO_INCIDENCIA"] = df["TIPO_INCIDENCIA"].str.upper()
    df["FECHA_REPORTE"] = pd.to_datetime(df["FECHA_REPORTE"], format="mixed", dayfirst=True).dt.strftime("%d-%m-%Y")
    df["ESTADO"] = df["ESTADO"].str.upper()

    df.to_csv(cvs_output)
    
preproceso_incidencias_usuario()