from langchain_core.runnables import RunnableBranch, RunnableLambda

from output_chains import gemini_chain, groq_summary_chain

#define the condition function
def is_special(inputs: dict) -> bool:
    return inputs["classification"].strip().upper() == "SPECIAL"

extract_description = RunnableLambda(lambda inputs: inputs["description"])
#build RunnableBranch
#branch 1: is_special → gemini_chain
#default : groq_summary_chain
router = RunnableBranch(
    (is_special, extract_description | gemini_chain),  # gemini_chain here
     extract_description | groq_summary_chain,         # groq_summary_chain as default
)
