from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

#instantiate ChatGroq with the correct model
groq_llm = ChatGroq(model="llama-3.3-70b-versatile")

#build a prompt that instructs the LLM to return only
#       "SPECIAL" or "STANDARD" — nothing else
classifier_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        (
            "You are a warehouse package classifier. "
            "Your job is to read a package description and classify it.\n\n"
            "Reply with exactly one word — either SPECIAL or STANDARD — with no punctuation, "
            "explanation, or extra text.\n\n"
            "Reply SPECIAL if the description mentions any of the following: "
            "fragile, hazardous, perishable, oversized, dangerous, flammable, toxic, "
            "or temperature-sensitive.\n\n"
            "Reply STANDARD if none of those conditions apply."
        ),
    ),
    (
        "human",
        "Package description: {description}"
    ),
])

#chain prompt | llm | StrOutputParser
classifier_chain = classifier_prompt | groq_llm | StrOutputParser()
