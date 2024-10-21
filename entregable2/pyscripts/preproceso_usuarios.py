import pandas as pd

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
    print(csv_input)
    df = pd.read_csv(csv_input)
    df["NOMBRE"] = df["NOMBRE"].str.upper()
    df["EMAIL"] = df["EMAIL"].str.upper()
    df["TELEFONO"] = df["TELEFONO"].apply(format_phone_number)

    print(df["TELEFONO"])
   # df.to_csv(csv_output,index=False)
preproceso_mantenimiento("./csvs/",".")