import requests

URL = "https://jsonplaceholder.typicode.com/users"


def get_customers(url):
    """Fetch customers from the API and return them as a list."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Could not fetch customer data: {e}")
        return []

def explore(record, indent=0):
    """Walk a record recursively, printing each key and its type."""
    spaces = "    " * indent
    if isinstance(record, dict):
        for key, value in record.items():
            print(f"{spaces}{key}: {type(value).__name__}")
            if isinstance(value, (dict, list)):
                explore(value, indent + 1)
    elif isinstance(record, list):
        for i, item in enumerate(record):
            print(f"{spaces}[{i}]: {type(item).__name__}")
            if isinstance(item, (dict, list)):
                explore(item, indent + 1)
def extract_attributes(customers):
    """Return one flat dict per customer with the fields we need."""
    rows = []
    for c in customers:
        rows.append({
            "id": c["id"],
            "name": c["name"],
            "username": c["username"],
            "email": c["email"],
            "email_domain": c["email"].split("@")[1],
            "phone": c["phone"],
            "city": c["address"]["city"],
            "zipcode": c["address"]["zipcode"],
            "latitude": float(c["address"]["geo"]["lat"]),
            "longitude": float(c["address"]["geo"]["lng"]),
            "company": c["company"]["name"],
            "website": c["website"],
        })
    return rows
def unique_cities(customers):
    """Return the set of unique cities."""
    return {c["address"]["city"] for c in customers}
def city_counts(customers):
    """Count customers per city using a plain loop."""
    counts = {}
    for c in customers:
        city = c["address"]["city"]
        counts[city] = counts.get(city, 0) + 1
    return counts


def email_domain_counts(customers):
    """Count customers per email domain using a dict comprehension."""
    domains = [c["email"].split("@")[1] for c in customers]
    return {d: domains.count(d) for d in set(domains)}

if __name__ == "__main__":
    customers = get_customers(URL)
    print(f"Fetched {len(customers)} customers")

    if customers:
        rows = extract_attributes(customers)

        cities = unique_cities(customers)
        print(f"\nUnique cities: {len(cities)}")
        print(f"Total customers: {len(customers)}")

        by_city = city_counts(customers)
        print("\nCustomers by city (most to least common):")
        for city, n in sorted(by_city.items(), key=lambda item: item[1], reverse=True):
            print(f"  {city}: {n}")

        by_domain = email_domain_counts(customers)
        print("\nCustomers by email domain (most to least common):")
        for domain, n in sorted(by_domain.items(), key=lambda item: item[1], reverse=True):
            print(f"  {domain}: {n}")