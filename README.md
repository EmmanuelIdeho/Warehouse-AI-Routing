# Automated Warehouse AI Routing Pipeline

A LangChain pipeline that classifies incoming package descriptions and automatically routes them to the most appropriate LLM — Google Gemini for special-handling safety reports, and Groq LLaMA for fast standard processing notes.

---

## What I Built

When a package arrives at the warehouse, a staff member types a short free-text description. The pipeline:

1. **Classifies** the description using Groq LLaMA 3.3 70B — returning exactly `SPECIAL` or `STANDARD`
2. **Routes** the description using LangChain's `RunnableBranch`
3. **Generates** the appropriate output:
   - `SPECIAL` → Google Gemini 2.5 Flash produces a structured **Special Handling Report** (risk type, PPE, storage conditions, carrier instructions)
   - `STANDARD` → Groq LLaMA 3.3 70B produces a concise **2–3 sentence processing note** for warehouse floor workers

---

## What I Learned

### LangChain LCEL (LangChain Expression Language)
Chains are built by piping components together with `|`. Each component receives the output of the previous one:

```python
chain = prompt | llm | StrOutputParser()
```

This pattern is consistent across all chains in the project — the classifier, the Gemini report chain, and the Groq summary chain all follow the same structure.

### Conditional Routing with RunnableBranch
`RunnableBranch` evaluates a list of `(condition, runnable)` tuples in order, running the first branch whose condition returns `True`. The last argument (no tuple) is the default fallback:

```python
router = RunnableBranch(
    (is_special, extract_description | gemini_chain),  # condition → runnable
    extract_description | groq_summary_chain,          # default
)
```

### The Adapter Pattern with RunnableLambda
The router receives a dict with both `"description"` and `"classification"`, but downstream chains only expect the description string. A `RunnableLambda` bridges the gap:

```python
extract_description = RunnableLambda(lambda inputs: inputs["description"])
```

This is a key pattern whenever the shape of data needs to change between pipeline steps.

### Prompt Engineering for Constrained Output
Getting an LLM to return exactly one word requires explicit constraints in the system prompt — stated clearly and early. Even then, `.strip().upper()` should be applied defensively before using the output for routing logic.

### Model Selection as a Design Decision
Not all tasks warrant the same model. Using a fast, lightweight model (Groq LLaMA) as a classifier keeps latency low for every package. Only descriptions that truly need it are escalated to a more capable model (Gemini). This tradeoff — cost/speed vs. depth — is a core consideration in production AI systems.

### Modular Pipeline Design
Each concern lives in its own file and can be developed, tested, and imported independently:

```
classifier_chain.py   → classification logic
output_chains.py      → both downstream LLM chains
router.py             → routing logic
warehouse_pipeline.py → entry point, wires everything together
test_connections.py   → standalone API connectivity check
```

### API Key Management
API keys are loaded from a `.env` file using `python-dotenv` and never hardcoded in source files. LangChain's integrations (`ChatGroq`, `ChatGoogleGenerativeAI`) pick up keys from environment variables automatically.

---

## Project Structure

```
.
├── .env                    # GROQ_API_KEY and GOOGLE_API_KEY (not committed)
├── .gitignore
├── README.md
├── classifier_chain.py     # Groq classifier → "SPECIAL" or "STANDARD"
├── output_chains.py        # Gemini safety report + Groq processing note
├── router.py               # RunnableBranch routing logic
├── warehouse_pipeline.py   # Entry point — runs all three test cases
└── test_connections.py     # Verify both APIs are reachable before running
```

---

## Setup

### Prerequisites
- Python 3.9+
- A [Groq API key](https://console.groq.com)
- A [Google AI API key](https://aistudio.google.com)

### Installation

```bash
pip install langchain langchain-google-genai langchain-groq python-dotenv
```

### Environment Variables

Create a `.env` file in the project root:

```
GROQ_API_KEY=your_groq_key_here
GOOGLE_API_KEY=your_google_key_here
```

> **Never commit your `.env` file.** Add it to `.gitignore`.

---

## Usage

Test that both APIs are reachable:

```bash
python test_connections.py
```

Run the full pipeline on all three test descriptions:

```bash
python warehouse_pipeline.py
```

### Example Output

```
Package       : A crate of antique glass vases wrapped in foam.
Classification: SPECIAL
Output:
Special Handling Report
1. Risk Type: Fragile — antique glassware at high risk of breakage under impact or pressure.
2. Required PPE: Cut-resistant gloves, steel-toed boots.
3. Storage Conditions: Store upright, do not stack. Keep away from heavy machinery.
4. Carrier Instructions: Label "FRAGILE – THIS SIDE UP". Hand-load only.
----------------------------------------------------------------------
Package       : 500 units of ballpoint pens, assorted colors.
Classification: STANDARD
Output:
This shipment contains 500 assorted ballpoint pens ready for standard processing.
Handle with care to avoid crushing the outer carton. Route to general inventory intake.
----------------------------------------------------------------------
```

---

## Models Used

| Model | Provider | Role |
|---|---|---|
| `llama-3.3-70b-versatile` | Groq | Classifier + standard processing notes |
| `gemini-2.5-flash-preview-05-20` | Google | Special handling safety reports |
