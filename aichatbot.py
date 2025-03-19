import ollama
from llm_axe import OnlineAgent,OllamaChat
model_name = 'mistral'
llm = OllamaChat(model=model_name)
messages = [{"role": "system", "content": ""},
            {"role":"user","content":"hello"}]
response=ollama.chat(model=model_name,messages=messages)
answer = response['message']['content']
onlineAgent = OnlineAgent(llm=llm)
print("bot:", answer)

while True:
    user_input = input("you: ")
    
    
    if not user_input:
        break
    messages.append({"role": "user", "content": user_input})
    response = ollama.chat(model=model_name, messages=messages)
    answer = response['message']['content']
    print("bot:", answer)
    
    messages.append({"role": "assistant", "content": answer})
    
if "search" in user_input.lower():
    query = f"Find reliable information about{user_input} from trusted sources."
    search_results = OnlineAgent.search(query,max_results=10, relevance_threshold=0.8)
    
    summary_prompt = f"Summarize this search result in simple words:{search_results}"
    response = ollama.chat(model=model_name,messages=[{"role":"user","content":summary_prompt}])
    
    print("Bot:", response['message']['content'])