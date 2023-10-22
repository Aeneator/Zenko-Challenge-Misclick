import json
import openai
import csv

openai.api_key = open("API_KEY.txt", 'r').read()


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


def get_location_lists():
    json_file = open("DataFiles/stand_data.json", "r")
    stand_list = json.loads(json_file.read())['stand_list']
    beverages = []
    foods = []
    urgency = []
    stages = []
    toilets = []
    buses = []
    trains = []
    recycle = []
    streets = []
    other = []
    for stand in stand_list:
        ok = False
        if 'details' in stand['properties']:
            if stand['properties']['details']['food_types'] is not None:
                foods.append(stand)
                ok = True
            if stand['properties']['details']['drink_categories'] is not None:
                beverages.append(stand)
                ok = True
        if 'eau' in stand['properties']['numero']:
            beverages.append(stand)
            ok = True
        if 'GSN' in stand['properties']['numero']:
            urgency.append(stand)
            ok = True
        if 'voirie' in stand['properties']['numero']:
            streets.append(stand)
            ok = True
        if 'TransN' in stand['properties']['numero']:
            trains.append(stand)
            ok = True
        if 'scÃ¨ne' in stand['properties']['numero']:
            stages.append(stand)
            ok = True
        if 'camion' in stand['properties']['numero']:
            buses.append(stand)
            ok = True
        if 'WC' in stand['properties']['numero']:
            toilets.append(stand)
            ok = True
        if 'Centre tri' in stand['properties']['numero']:
            recycle.append(stand)
            ok = True
        if ok is False:
            other.append(stand)
    return beverages, foods, urgency, stages, toilets, buses, trains, recycle, streets, other


def get_pins(loc_list):
    return [{"coordinates": [loc['properties']['centerpoint'].split(', ')[1], loc['properties']['centerpoint'].split(', ')[0]],
             "popupText": loc_list.index(loc)} for loc in loc_list]


# def gpt_test(prompt_question):
#     openai.api_key = open("API_KEY.txt", 'r').read()
#     questions = '\"'
#     answers = []
#     with open('DataFiles/FAQ.csv', newline='') as csvfile:
#         csv_reader = csv.reader(csvfile)
#         for row in csv_reader:
#             questions += row[0] + '\", '
#             answers.append(row[1])
#     questions = questions[:-3] + ';'
#     prompt = f"You are a festival assistant for the FDV festival and you are given this question: \"{prompt_question}\"; give me the question number you are most confident is similar in topic to the previous question among the next ones and a confidence level from 0 to 100 under this format: \"confidence=X, answer_number=Y\" : {questions}."
#
#     chat_logs = []
#     chat_logs.append({"role": "user", "content": prompt})
#     response = openai.ChatCompletion.create(
#         model="gpt-3.5-turbo",
#         messages=chat_logs
#     )
#     assistant_response = response['choices'][0]['message']['content']
#     chat_logs.append({"role": "assistant", "content": assistant_response.strip("\n").strip()})
#
#     question_number = int(assistant_response.split(':')[0].split(", ")[1].split('=')[1])
#     prompt = f"Now answer the following question in under 100 words in this question's language: \"{prompt_question}\" using this information: \n{answers[question_number - 1]}\""
#     chat_logs.append({"role": "user", "content": prompt})
#     response = openai.ChatCompletion.create(
#         model="gpt-3.5-turbo",
#         messages=chat_logs
#     )
#     return response['choices'][0]['message']['content']

