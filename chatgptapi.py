import requests

# Fonction pour appeler l'API ChatGPT et générer les questions et les choix
def generate_questions(prompt):
            api_endpoint = "https://api.openai.com/v1/chat/completions"
            headers = {
                "Authorization": "Bearer Your_bearer_token",
                "Content-Type": "application/json"
            }
            data = {
                "model": "gpt-3.5-turbo",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.7
            }

            
            response = requests.post(api_endpoint, headers=headers, json=data)
            if response.status_code == 200:
                questions = response.json()["choices"]
                return questions
            else:
                return None
