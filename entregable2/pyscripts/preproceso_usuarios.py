import pandas as pd

def fill_missing_tipo(row,column,string_missing):
    if pd.isnull(row[column]):
        return f'{string_missing}_{row["NIF"]}'
    return row[column]

def format_phone_number(phone):

    phone = phone.replace(" ", "")
    if phone.startswith("+34"):
        phone = phone[3:]
    if phone.startswith("34"):
        phone = phone[2:]
    return phone

def preproceso_mantenimiento(csv_input, csv_output):
    csv_input = csv_input + "UsuariosSucio.csv"
    csv_output = csv_output + "usuarios_limpios.csv"
    df = pd.read_csv(csv_input)
    df["NOMBRE"] = df["NOMBRE"].str.upper()
    df["EMAIL"] = df["EMAIL"].str.upper()
    df["TELEFONO"] = df["TELEFONO"].apply(format_phone_number)
    df = df.drop(columns=["Email"])
    df["EMAIL"] = df.apply(lambda row: fill_missing_tipo(row, "EMAIL", "EMAIL_DESCONOCIDO"), axis=1)

    df.to_csv(csv_output,index=False)