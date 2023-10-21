import json
import PyPDF2


def get_stand_data():
    shops_list = []
    id_list = []
    csv_file = open("RawFiles/export_stands20230922 (1).csv")
    headers = next(csv_file)[:-1].split(';')
    for row in csv_file:
        row_data = row[:-1].split(';')
        temp = {}
        for i in range(1, len(headers)):
            temp[headers[i]] = (row_data[i] if ', ' not in row_data[i] else row_data[i].split(', ')) if row_data[i] != '' else None
        shops_list.append(temp)
        id_list.append(row_data[0])

    json_file = open('RawFiles/fdv_stands20230920.geojson', "r")
    stand_list = json.loads(json_file.read())['features']

    for stand in stand_list:
        try:
            stand['properties']['details'] = shops_list[id_list.index(stand['properties']['numero'])]
        except ValueError:
            continue

    json_object = json.dumps({'stand_list': stand_list}, indent=4)
    with open("DataFiles/stand_data.json", "w") as outfile:
        outfile.write(json_object)


get_stand_data()
