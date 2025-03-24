from openai import OpenAI
import os

OPEN_API_KEY = os.environ.get('OPENAI_API_KEY')

client = OpenAI(api_key=OPEN_API_KEY)
trainer = client.fine_tuning.jobs.create(
    training_file="file-NXKRgkHRZo7UqQeYco6B93",
    model="gpt-4o-mini-2024-07-18",
    suffix= "ellie-1"
)

print(trainer)