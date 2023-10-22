import openai
import read_data
import pandas as pd


chat_logs = {}


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def answer(question, ip):
    openai.api_key = open("API_KEY.txt", 'r').read()
    df = pd.read_csv("DataFiles/FAQ.csv")
    list_of_questions = ""

    faq_list_questions = df["Questions"].tolist()
    faq_list_answers = df["Answers"].tolist()[:-1]

    q_id = 0
    for question in faq_list_questions:
        q_id += 1
        list_of_questions += ' ,' + str(q_id) + ' \"' + question + '\"'

    faqTestResult = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user",
                   "content": "With the context that you are a festival assistant that has to answer questions. You have the following question from a festival participant:\"" + question + "\". Is the given question kind of similar in meaning has the same keywords, format or answer to any question in the following list of frequently asked questions:" + list_of_questions + "? If you can find a similar question return just YES and the number before the most similar question, example: 'YES,number', don't change the format: 'YES,number' and don't add anything more. If you can't find a question similar enough return just NO."}]
    )

    faq_content = faqTestResult['choices'][0]['message']['content']

    if faqTestResult['choices'][0]['message']['content'].lower().find("yes") != -1:
        AI_personality = "You are an AI Customer Relations, your role is to be the Central point of interaction with festival goers, your objectives are: Provide real-time information and Improve customer experience. "
        Task = "Use the information \"" + faq_list_answers[int(faq_content.split(',')[1].strip()) - 2] + "\""
        Limit = "don't change the sentence too much, but the message shouldn't exceed 300 characters."

        chat_logs[ip].append({"role": "user", "content": AI_personality + Task + " to answer: \"" + question + "\"." + Limit})
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=chat_logs[ip]
        )
        final_response = response['choices'][0]['message']['content']
        chat_logs[ip].append(
            {"role": "assistant", "content": response['choices'][0]['message']['content'].strip("\n").strip()})
        return final_response, None

    else:
        marker_list = None
        print("Not a FAQ.")

        base_string = "You are assisting with a festival and there are 10 categories: tickets, vital location, transport, food, music, program, beverage, urgency, history and other. If a question is not festival related it is considered other. In which category does this question fit (and only name exactly the category): "
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": base_string + question}]
        )
        tag_response = response['choices'][0]['message']['content'].lower()

        print(tag_response)

        AI_personality = "You are an AI Customer Relations, your role is to be the Central point of interaction with festival goers, your objectives are: Provide real-time information and Improve customer experience. "
        Information = "Use the following information if needed: \""
        Limit = "Give a concise answer in around a sentence "

        beverages, foods, urgency, stages, toilets, buses, trains, recycle, streets, other = read_data.get_location_lists()
        location_list = []
        q_id = 0
        if tag_response == "history":
            Information += faq_list_answers[0]
        if tag_response == "tickets":
            for question in faq_list_questions:
                q_id += 1
                if question.find("ticket") != -1:
                    Information += ' ,' + ' \"' + faq_list_answers[q_id] + '\"'
        elif tag_response == "vital location":
            for question in faq_list_questions:
                q_id += 1
                if question.find("location") != -1:
                    Information += ' ,' + ' \"' + faq_list_answers[q_id] + '\"'
                location_list.extend(toilets)
                location_list.extend(recycle)
                location_list.extend(stages)
                Information += location_list.__str__()
        elif tag_response == "transport":
            Information += read_data.get_route_info()
            location_list.extend(trains)
            location_list.extend(streets)
            location_list.extend(buses)
            Information += location_list.__str__()
        elif tag_response == "food":
            location_list.extend(foods)
            Information += location_list.__str__()
        elif tag_response == "music":
            for question in faq_list_questions:
                q_id += 1
                if question.find("music") != -1:
                    Information += ' ,' + ' \"' + faq_list_answers[q_id] + '\"'
        elif tag_response == "program":
            for question in faq_list_questions:
                q_id += 1
                if question.find("program") != -1:
                    Information += ' ,' + ' \"' + faq_list_answers[q_id] + '\"'
        elif tag_response == "beverage":
            for question in faq_list_questions:
                q_id += 1
                if question.find("beverage") != -1:
                    Information += ' ,' + ' \"' + faq_list_answers[q_id] + '\"'
                location_list.extend(beverages)
                Information += location_list.__str__()
        elif tag_response == "urgency":
            for question in faq_list_questions:
                q_id += 1
                if question.find("urgency") != -1:
                    Information += ' ,' + ' \"' + faq_list_answers[q_id] + '\"'
                location_list.extend(urgency)
                Information += location_list.__str__()
        else:
            Information += "Try to give a short response"
            Information += read_data.get_recycle_info()
            location_list.extend(other)
            Information += location_list.__str__()

        Information += "\""

        chat_logs[ip].append({"role": "user", "content": AI_personality + Limit + Information + question})
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=chat_logs[ip]
        )
        final_response = response['choices'][0]['message']['content']
        chat_logs[ip].append({"role": "assistant", "content": final_response.strip("\n").strip()})

        if len(location_list) is not 0:
            final_response += " Also here is a map that may help you!"
            marker_list = read_data.get_pins(location_list)
        return final_response, marker_list
