from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
 
from classifier_chain import groq_llm
#Gemini chain
gemini_llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
gemini_prompt =  ChatPromptTemplate.from_messages([
    (
        "system",
        (
            "You are a warehouse safety officer. "
            "When given a description of a special-handling package, produce a structured "
            "Special Handling Report with the following four sections:\n\n"
            "1. Risk Type — identify the primary hazard (e.g. fragile, flammable, perishable).\n"
            "2. Required PPE — list any personal protective equipment staff must wear.\n"
            "3. Storage Conditions — specify temperature, orientation, segregation, or other "
            "storage requirements.\n"
            "4. Carrier Instructions — detail any labelling, loading, or transit requirements "
            "the carrier must follow.\n\n"
            "Be thorough and precise. Use clear, professional language."
        ),
    ),
    (
        "human",
        "Package description: {description}"
    ),
])
   # Special Handling Report prompt
gemini_chain = gemini_prompt | gemini_llm | StrOutputParser()   # prompt | gemini_llm | StrOutputParser

# TODO: Groq summary chain (reuse groq_llm from classifier)
groq_summary_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        (
            "You are a warehouse logistics assistant. "
            "When given a description of a standard package, write a concise 2–3 sentence "
            "Standard Processing Note for warehouse floor workers. "
            "Cover what the package contains, how it should be handled, and where it should go. "
            "Use plain, direct language suitable for a busy warehouse environment."
        ),
    ),
    (
        "human",
        "Package description: {description}"
    ),
])  # Processing Note prompt
groq_summary_chain  = groq_summary_prompt | groq_llm | StrOutputParser()  # prompt | groq_llm | StrOutputParser
