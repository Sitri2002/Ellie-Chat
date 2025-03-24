from openai import OpenAI
import os
import time
OPEN_API_KEY = os.environ.get('OPENAI_API_KEY')

client = OpenAI(api_key=OPEN_API_KEY)
response = client.fine_tuning.jobs.list(limit=10)

# while True:
#     events = client.fine_tuning.jobs.list_events(fine_tuning_job_id="ftjob-PnzfgdScqsUtyjqqyCdxBQMJ", limit=1)
#     print(events)
#     time.sleep(10)

print(response)