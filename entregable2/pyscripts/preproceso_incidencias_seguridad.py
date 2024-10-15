import pandas as pd

def change_accents(word):
    for letter in range(len(word)):
        if word[letter] == "Á":
            word = word[0:letter] + "A" + word[letter + 1:]
        if word[letter] == "É":
            word = word[0:letter] + "E" + word[letter + 1:]
        if word[letter] == "Í":
            word = word[0:letter] + "I" + word[letter + 1:]
        if word[letter] == "Ó":
            word = word[0:letter] + "O" + word[letter + 1:]
        if word[letter] == "Ú":
            word = word[0:letter] + "U" + word[letter + 1:]
    return word

def preproceso_incidencias_seguridad(csv_input, csv_output):
    csv_input = csv_input + "IncidentesSeguridadSucio.csv"
    csv_output = csv_output + "incidentes_seguridad_limpio.csv"

    df = pd.read_csv(csv_input)
    df["FECHA_REPORTE"] = pd.to_datetime(df["FECHA_REPORTE"], format="mixed", dayfirst=True).dt.strftime("%d-%m-%Y")
    df["TIPO_INCIDENTE"] = df["TIPO_INCIDENTE"].str.upper().apply(change_accents)
    df["GRAVEDAD"] = df["GRAVEDAD"].str.upper().apply(change_accents)

    df.to_csv(csv_output)

