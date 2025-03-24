import json

SYSTEM_PROMPT = open("data/system.txt", 'r').read().strip()
unformatted = open("training/neuro.json", "r")
formatted = open("training/neuro_format.jsonl", "w+")
dataset = json.load(unformatted)

for data in dataset:
    data['instruction'] = data['instruction'].replace("Neuro", "Ellie")
    data['instruction'] = data['instruction'].replace("Vedal", "Sitri")
    data['output'] = data['output'].replace("Neuro", "Ellie")
    data['output'] = data['output'].replace("Vedal", "Sitri")
    to_dumped = {"messages": [{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": data['instruction']}, {"role": "assistant", "content": data['output']}]}
    json.dump(to_dumped, formatted)
    formatted.write("\n")
formatted.close()