import pandas as pd

def preproceso_incidencias_usuario(csv_input, csv_output):
    csv_input = csv_input + "IncidenciasUsuariosSucio.csv"
    csv_output = csv_output + "incidencias_usuarios_limpio.csv"
    df = pd.read_csv(csv_input)
    df["TIPO_INCIDENCIA"] = df["TIPO_INCIDENCIA"].str.upper()
    df["FECHA_REPORTE"] = pd.to_datetime(df["FECHA_REPORTE"], format="mixed", dayfirst=True).dt.strftime("%d-%m-%Y")
    df["ESTADO"] = df["ESTADO"].str.upper()

    df.to_csv(csv_output, index=False)
