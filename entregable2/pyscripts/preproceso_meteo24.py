import pandas as pd

def relacionar_meteo_area(meteo, areas):
    lugares = {102: "MORATALAZ", 103: "VILLAVERDE", 104:"LA CHINA", 106:"CENTRO MPAL. DE ACUSTICA", 107: "HORTALEZA", 108: "PEÑAGRANDE", 109:"CHAMBERI", 110:"CENTRO", 111:"CHAMARTIN", 112:"VALLECAS", 113:"VALLECAS", 114:"MATEDERO", 115:"MATADERO", 4: "PLAZA ESPAÑA", 8: "ESCUELAS AGUIRRE", 16: "ARTURO SORIA", 18:"FAROLILLO", 24:"CASA DE CAMPO", 36:"MORATALAZ", 38:"CUATRO CAMINOS", 39:"PILAR", 54:"ENSANCHE DE VALLECAS", 56:"PLAZA ELIPTICA", 58:"FUENCARRAL - EL PARDO", 59: "JUAN CARLOS I"  }

    for index, row in meteo.iterrows():
        estacion = row['ESTACION']
        if estacion in lugares:
            lugar = lugares[estacion]
            # Buscar el valor en las columnas BARRIO y DISTRITO
            area_row = areas[(areas['BARRIO'].str.contains(lugar, case=False, na=False)) | (areas['DISTRITO'].str.contains(lugar, case=False, na=False))]
            if not area_row.empty:
                # Tomar el valor del ID de la primera coincidencia
                meteo.at[index, 'ID_AREA'] = area_row.iloc[0]['ID']
            else:
                meteo.at[index, 'ID_AREA'] = -1

def preproceso_meteo24(csv_input, csv_output):
    meteo_csv = csv_input + "meteo24.csv"
    csv_output = csv_output + "meteo24_limpio.csv"

    areas_csv = csv_input + "AreasSucio.csv"

    meteo = pd.read_csv(meteo_csv, delimiter=';')
    areas = pd.read_csv(areas_csv)

    relacionar_meteo_area(meteo,areas)
    
    new_meteo = pd.DataFrame(columns=["FECHA","TEMPERATURA","PRECIPITACION","VIENTO","ID_AREA"])

    magnitudes = {81:"VIENTO",83:"TEMPERATURA",89:"PRECIPITACION"}

    for _,row in meteo.iterrows():
        magnitud = row["MAGNITUD"]
        if magnitud in magnitudes:
            año = row["ANO"]
            mes = row["MES"]
            dia = 1
            id_area = row["ID_AREA"]
            for dia in range(1,32):
                valor = row.iloc[7 + (dia - 1) * 2]
                fecha = f"{dia:02d}-{mes:02d}-{año}"

                # Verificar si ya existe una fila con la misma fecha e ID_AREA
                if not ((new_meteo["FECHA"] == fecha) & (new_meteo["ID_AREA"] == id_area)).any():
                    # Crear una nueva fila
                    new_row = {"FECHA": fecha, "ID_AREA": id_area, magnitudes[magnitud]: valor}
                    new_meteo.loc[len(new_meteo.index)] = new_row
                else:
                    # Actualizar la fila existente
                    new_meteo.loc[(new_meteo["FECHA"] == fecha) & (new_meteo["ID_AREA"] == id_area), magnitudes[magnitud]] = valor


    new_meteo.to_csv(csv_output,index=False)
