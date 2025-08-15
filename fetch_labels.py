# fetch_labels.py
import requests
from models import DrugLabel

BASE_URL = "https://api.fda.gov/drug/label.json"

def fetch_labels(drug_name: str, max_results: int = 3):
    """
    Fetches drug label information from OpenFDA.
    """
    params = {
        "search": f"openfda.brand_name:{drug_name}",
        "limit": max_results
    }

    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()
    data = response.json()

    labels = []
    for item in data.get("results", []):
        labels.append(DrugLabel(
            id=item.get("id", "N/A"),
            brand_name=", ".join(item.get("openfda", {}).get("brand_name", [])),
            generic_name=", ".join(item.get("openfda", {}).get("generic_name", [])),
            purpose="\n".join(item.get("purpose", [])) if "purpose" in item else None,
            warnings="\n".join(item.get("warnings", [])) if "warnings" in item else None,
            indications="\n".join(item.get("indications_and_usage", [])) if "indications_and_usage" in item else None
        ))
    return labels

if __name__ == "__main__":
    results = fetch_labels("trastuzumab")
    for r in results:
        print(r.dict())
