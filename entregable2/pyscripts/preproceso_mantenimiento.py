import pandas as pd

def preproceso_mantenimiento(csv_input, csv_output):
    csv_input = csv_input + "MantenimientoSucio.csv"
    csv_output = csv_output + "mantenimiento_limpio.csv"
    df = pd.read_csv(csv_input)
    df["TIPO_INTERVENCION"] = df["TIPO_INTERVENCION"].str.upper()
    df["FECHA_INTERVENCION"] = pd.to_datetime(df["FECHA_INTERVENCION"], format="mixed", dayfirst=True).dt.strftime("%d-%m-%Y")
    df["ESTADO_PREVIO"] = df["ESTADO_PREVIO"].str.upper()
    df["ESTADO_POSTERIOR"] = df["ESTADO_POSTERIOR"].str.upper()
    df["Tipo"] = df["Tipo"].str.upper()

    # No se han tratado missing values

    df.to_csv(csv_output)
