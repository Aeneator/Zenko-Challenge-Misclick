import openai
import csv
import pandas as pd

API_KEY = open("..\API_KEY.txt", 'r').read()
openai.api_key = API_KEY

FAQ_file = "..\DataFiles\FAQ.csv"

chat_log = []

while True:
    user_message = input()

    df = pd.read_csv(FAQ_file)
    list_of_questions = ""

    faq_list_questions = df["Questions"].tolist()
    faq_list_answers = df["Answers"].tolist()

    q_id = 0
    for question in faq_list_questions:
        q_id += 1
        list_of_questions += ' ,'+str(q_id)+' \"' + question + '\"'

    faqTestResult = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  #If it is, return exactly 'YES' and 'the number of the question it's most similar to', else return just NO."
        messages=[{"role": "user", "content": "With the context that you are a festival assistant that has to answer questions. You have the following question from a festival participant:\"" + user_message + "\". Is the given question similar to any question in the following list of frequently asked questions:" + list_of_questions + "? If you can find a similar question return just YES and the number before the most similar question, example: 'YES,number'. If you can't find a question similar enough return just NO." }]
    )

    faq_content = faqTestResult['choices'][0]['message']['content']

    if faqTestResult['choices'][0]['message']['content'].lower().find("yes") != -1:
        AI_personality = "You are an AI Customer Relations, your role is to be the Central point of interaction with festival goers, your objectives are: Provide real-time information and Improve customer experience. "
        Task = "Use the sentence \"" + faq_list_answers[int(faq_content.split(',')[1].strip())-1] + "\""
        Limit = "don't change the sentence too much"
        response = openai.ChatCompletion.create(

            model="gpt-3.5-turbo",
            # If it is, return exactly 'YES' and 'the number of the question it's most similar to', else return just NO."
            messages=[{"role": "user",
                       "content": Task + " to answer: \"" + user_message + "\"." + Limit}]
        )
        print(response['choices'][0]['message']['content'])

    else:
        print("No")

        # AI_personality="You are an AI Customer Relations, your role is to be the Central point of interaction with festival goers, your objectives are: Provide real-time information and Improve customer experience. "
        # Task="Answer the following message from an event goers: "
        # Limit="Give a concise answer in around a sentence "
        #
        # chat_log.append({"role": "user", "content": AI_personality + Limit + Task + user_message})
        # response = openai.ChatCompletion.create(
        #     model="gpt-3.5-turbo",
        #     messages=chat_log
        # )
        # assistant_response = response['choices'][0]['message']['content']
        # print("ChatGPT:", assistant_response.strip("\n").strip())
        # #print(response)
        # chat_log.append({"role": "assistant", "content": assistant_response.strip("\n").strip()})