# Pesa Pulse: Where Are Our Customers?

## Overview
Pesa Pulse has a new partner that shares its customer directory through an API. Before marketing plans regional campaigns, this project answers "where are our customers?". It pulls the customer data, explores its nested structure, extracts the key attributes, and counts customers first with plain Python (sets, dictionaries, comprehensions) and then with pandas. It exports two CSV files and two charts.

## Project structure
```
day1-api-analysis/
├── analysis.py
├── analysis.ipynb
├── output/
│   ├── customers.csv
│   ├── city_counts.csv
│   ├── customer_distribution.png
│   └── email_domain_distribution.png
├── requirements.txt
└── README.md
```

## How to run
1. Install the requirements:
   ```
   python -m pip install -r requirements.txt
   ```
2. Run the analysis:
   ```
   python analysis.py
   ```
3. The CSVs and charts are written to the `output/` folder, and the findings are printed to the console.

**Running in Google Colab:** pandas was blocked by a security policy on my local computer, so I ran the full analysis in Google Colab. `analysis.ipynb` is the executed notebook. To reproduce it, open Colab, paste the contents of `analysis.py` into a cell and run it. Colab already includes `requests`, `pandas` and `matplotlib`.

## Approach
- **Task 1, retrieve data:** `get_customers` calls the API with `requests.get`, a 10-second timeout and `raise_for_status()`. Network errors, bad status codes and invalid JSON print a clear message and return an empty list instead of crashing.
- **Task 2, explore structure:** `explore` walks a record recursively and prints each key with its type, indented by depth.
- **Task 3, extract attributes:** `extract_attributes` returns one flat dictionary per customer. Latitude and longitude are converted to floats, and `email_domain` is the top-level domain (for example `biz`), as specified in the expected-output file.
- **Task 4, unique cities:** `unique_cities` uses a set comprehension.
- **Task 5, counting:** `city_counts` uses a loop with `dict.get`, and `email_domain_counts` uses a dict comprehension. Neither uses `collections.Counter` or pandas. Results are sorted from most to least common.
- **Task 6, pandas:** `to_dataframe` builds the DataFrame, and `value_counts()` is compared with the hand-written city counts.
- **Task 7, export:** both CSVs are written with `index=False`. `city_counts.csv` is sorted by `customer_count` descending, then by city.
- **Task 8, visualise:** `plot_distribution` saves a titled bar chart with labelled axes.

## Nested structure (Task 2)
Each customer record has two nested attributes:
- `address`, a dictionary that contains `street`, `suite`, `city`, `zipcode` and another nested dictionary, `geo`.
- `company`, a dictionary that contains `name`, `catchPhrase` and `bs`.

The deepest attributes are the coordinates, reached with `record["address"]["geo"]["lat"]` and `record["address"]["geo"]["lng"]`. The API returns them as strings, so they are converted to floats during extraction.

## Findings
- **Customers retrieved:** 10
- **Unique cities:** 10
- **Most common city:** Aliyaview (1)
- **Email domains:** `{'biz': 3, 'ca': 1, 'info': 1, 'io': 1, 'me': 1, 'net': 1, 'org': 1, 'tv': 1}`

In plain English:
1. There are 10 unique cities for 10 customers, so every customer lives in a different city. A city-level campaign would reach only one customer per city, so marketing needs a broader grouping, such as region.
2. The most common email domain is `biz` with 3 customers. Every other domain has 1, so email domain is a more useful way to segment these customers than city.
3. Aliyaview appears as the "most common city" only because of the alphabetical tie-break. With 1 customer, it is tied with every other city and says nothing about where customers are concentrated.

## Which chart is more useful?
The email-domain chart (`email_domain_distribution.png`) is more useful. The city chart (`customer_distribution.png`) is flat, with every bar equal to 1, so it shows no pattern marketing can act on. The domain chart has bars of different heights, so it shows where customers are concentrated.

## Assumptions
- The data comes from a mock API (JSONPlaceholder) and has exactly 10 records, so the results are illustrative rather than real Pesa Pulse customers.
- "Email domain" means the top-level domain (the part after the last dot), as in the expected-output file.
- Each customer appears once, with no duplicates or missing fields.
- Ties in counts are broken alphabetically.
- The pandas steps were run in Google Colab because pandas was blocked by a security policy on my local machine.