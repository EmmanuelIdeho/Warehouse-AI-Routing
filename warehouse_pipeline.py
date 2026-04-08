from dotenv import load_dotenv
load_dotenv()

from classifier_chain import classifier_chain
from router import router

# Full pipeline

def run_pipeline(description: str) -> None:
    # Step 1: classify
    classification = classifier_chain.invoke({"description": description})
    classification = classification.strip().upper()

    # Step 2: route and generate
    result = router.invoke({
        "description":    description,
        "classification": classification,
    })

    # Step 3: print
    print(f"Package       : {description}")
    print(f"Classification: {classification}")
    print(f"Output:\n{result}")
    print("-" * 70)



# Test cases
if __name__ == "__main__":
    test_packages = [
        #"A crate of antique glass vases wrapped in foam.",
        #"500 units of ballpoint pens, assorted colors.",
        "Lithium-ion battery packs for electric scooters.",
    ]

    for description in test_packages:
        run_pipeline(description)
