# GST Rate Finder

A simple Streamlit application for looking up product GST information in India and calculating the price including GST.

## Features

- Search products by name.
- Display product name, price, GST rate, applicability status, HSN code and source.
- Identify intra-state and inter-state transactions using supplier and buyer states.
- Calculate CGST + SGST for intra-state transactions and IGST for inter-state transactions.
- Calculate the final price including GST.
- Clear the search form and start another search.

## Project files

- `app.py` – Streamlit application.
- `products.csv` – Editable product database.
- `requirements.txt` – Python dependencies.

## Important: Add product data

The included `products.csv` is a blank template. Add one product per row using these columns:

| Column | Meaning |
|---|---|
| `product_name` | Product name |
| `product_price` | Base price in INR, numbers only |
| `gst_rate` | GST rate as a number, e.g. `18` |
| `hsn_code` | Applicable HSN code |
| `gst_applicability` | For example, `Taxable` or `Exempt` |
| `official_source` | Official source URL supporting the classification/rate |

Do not assume a rate or HSN code from a product name alone. Verify the correct classification and rate against the latest official notifications and CBIC rate schedules before adding it. Rates can depend on product specifications and applicable conditions.

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy on Streamlit Community Cloud

1. Upload `app.py`, `products.csv`, `requirements.txt` and `README.md` to a GitHub repository.
2. Open Streamlit Community Cloud and connect your GitHub account.
3. Select the repository and choose `app.py` as the main file.
4. Deploy the application.

## Official reference links

- CBIC GST goods and services rates: https://cbic-gst.gov.in/hindi/gst-goods-services-rates.html
- GST Council – State-specific GST: https://gstcouncil.gov.in/state-specific-gst
- GST portal: https://www.gst.gov.in/

## Calculation logic

- Intra-state: CGST = half of the total GST rate; SGST = half of the total GST rate.
- Inter-state: IGST = the full GST rate.
- Final price = base price + GST amount.

This is an educational project, not tax or legal advice. Confirm the applicable rate, HSN classification, place of supply and transaction treatment before using the result for an actual invoice.
