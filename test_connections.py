from dotenv import load_dotenv
load_dotenv()

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

PROMPT = "In one sentence, what is your role in an automated warehouse?"

# Gemini 2.5 Flash
try:
    gemini_llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
    response = gemini_llm.invoke([HumanMessage(content=PROMPT)])
    print(f"[GEMINI] {response.content.strip()}")
except Exception as e:
    print(f"[GEMINI] Connection failed: {e}")


# Groq LLaMA 3.3 70B
try:
    groq_llm = ChatGroq(model="llama-3.3-70b-versatile")
    response = groq_llm.invoke([HumanMessage(content=PROMPT)])
    print(f"[GROQ]   {response.content.strip()}")
except Exception as e:
    print(f"[GROQ]   Connection failed: {e}")
