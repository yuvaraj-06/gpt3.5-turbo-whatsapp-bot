import openai
import re
import json
import requests

OPENAI_API_KEY = "API_KEY"


class GPT:
    def __init__(self, id):
        self.id = id
        self.file_name = f"{str(self.id)}.json"
        self.session = {
            "start": True,
            "data": "Hi there! My name is RajGPT, and I'm here to help you with anything , you can ask me any question",
            "log": [
                {
                    "role": "system",
                    "content": "You are a helpful assistant",
                },
                {
                    "role": "assistant",
                    "content": "Hi there! My name is RajGPT, and I'm here to help you with anything , you can ask me any question",
                },
            ],
        }

        try:
            with open(self.file_name) as outfile:
                data = json.load(outfile)
            outfile.close()
            self.session = data
        except Exception:
            with open(self.file_name, "w") as outfile:
                json.dump(self.session, outfile)
            outfile.close()

    def bot(self, input_query):

        if self.session["start"]:

            self.session["start"] = False
            with open(self.file_name, "w") as outfile:
                json.dump(self.session, outfile)
            outfile.close()
            return "Hi there! My name is RajGPT, and I'm here to help you with anything , you can ask me any question"

        openai.api_key = OPENAI_API_KEY

        self.session["log"].append({"role": "user", "content": input_query})
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.session["log"],
            temperature=0.8,
            max_tokens=800,
            top_p=1,
        )

        res = response["choices"][0]["message"]["content"]
        self.session["log"].append({"role": "assistant", "content": res})
        self.session["data"] += res + " \n "
        with open(self.file_name, "w") as jsonFile:
            json.dump(self.session, jsonFile)
        jsonFile.close()

        return res
