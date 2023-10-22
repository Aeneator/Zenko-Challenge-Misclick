import openai
import read_data


chat_logs = {}


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def ask_question_topic(question, ip):
    openai.api_key = open("API_KEY.txt", 'r').read()

    base_string = "You are assisting with a festival and there are 10 categories: tickets, vital location, transport, food, music, program, beverage, urgency, history and other. If a question is not festival related it is considered other. In which category does this question fit (and only name exactly the category): "
    chat_logs[ip].append({"role": "user", "content": base_string + question})
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=chat_logs[ip]
    )
    assistant_response = response['choices'][0]['message']['content']
    chat_logs[ip].append({"role": "assistant", "content": assistant_response.strip("\n").strip()})

    beverages, foods, urgency, stages, toilets, buses, trains, recycle, streets, other = read_data.get_location_lists()
    return assistant_response, read_data.get_pins(recycle)
