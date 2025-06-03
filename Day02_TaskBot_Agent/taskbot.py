import os
from openai import OpenAI
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
client = OpenAI(api_key=os.getenv("GROQ_API_KEY"), base_url="https://api.groq.com/openai/v1")

def ask_groq(tasks):
    prompt = f"""You are a productivity assistant called TaskBot. I have the following tasks:
{tasks}

Please prioritize them and explain why in 3 sentences. Return the result as a numbered list.
"""
    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

def main():
    print("👋 Welcome to TaskBot!\n")
    tasks = []
    
    while True:
        task = input("Enter a task (or type 'done' to finish): ")
        if task.lower() == 'done':
            break
        tasks.append(task)
    
    if tasks:
        combined_tasks = "\n".join(f"- {t}" for t in tasks)
        result = ask_groq(combined_tasks)
        print("\n✅ Prioritized Tasks by TaskBot:\n")
        print(result)
    else:
        print("❌ No tasks entered.")

if __name__ == "__main__":
    main()
