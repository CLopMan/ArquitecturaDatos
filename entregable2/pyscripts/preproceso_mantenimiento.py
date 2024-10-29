import pandas as pd

def fill_missing_tipo(row,column,string_missing):
    if pd.isnull(row[column]):
        return f'{string_missing}_{row["ID"]}'
    return row[column]

def preproceso_mantenimiento(csv_input, csv_output):
    csv_input = csv_input + "MantenimientoSucio.csv"
    csv_output = csv_output + "mantenimiento_limpio.csv"

    df = pd.read_csv(csv_input)
    df["TIPO_INTERVENCION"] = df["TIPO_INTERVENCION"].str.upper()
    df["FECHA_INTERVENCION"] = pd.to_datetime(df["FECHA_INTERVENCION"], format="mixed", dayfirst=True).dt.strftime("%d-%m-%Y")
    df["ESTADO_PREVIO"] = df["ESTADO_PREVIO"].str.upper()
    df["ESTADO_POSTERIOR"] = df["ESTADO_POSTERIOR"].str.upper()

    df["Tipo"] = df.apply(lambda row: fill_missing_tipo(row, "Tipo", "TIPO_DESCONOCIDO"), axis=1)
    df["Tipo"] = df["Tipo"].str.upper()

    df["Comentarios"] = df.apply(lambda row: fill_missing_tipo(row, "Comentarios", "COMENTARIO_DESCONOCIDO"), axis=1)

    df.to_csv(csv_output, index=False)

if __name__ == "__main__":
    preproceso_mantenimiento("./csvs/", "./")