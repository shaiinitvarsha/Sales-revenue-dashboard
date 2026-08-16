📊 Sales & Revenue Analysis Dashboard

Build a dashboard to analyze sales and revenue data.

## Key Features

- Import data from Excel, CSV, or database (CSV/Excel upload, or use the bundled sample data)
- Visualize KPIs like total sales, revenue trends, and top-performing products
- Use charts, filters, and slicers for interactive analysis

## Expected Outcome

Learn data visualization, KPI tracking, and business insight generation.

## Tech Stack

Python, Streamlit, Pandas, Plotly

## Project Structure

```
sales-dashboard/
├── app.py                  # Main Streamlit app
├── generate_data.py        # Script that generated the sample dataset
├── sample_sales_data.csv   # Bundled sample dataset
├── requirements.txt
└── README.md
```

## Run Locally

```
pip install -r requirements.txt
streamlit run app.py
```

Then open the URL Streamlit prints (usually http://localhost:8501).

## Dataset Columns

| Column | Description |
|---|---|
| Order ID | Unique order identifier |
| Date | Order date |
| Customer ID | Customer identifier |
| Product | Product name |
| Category | Product category |
| Region | Sales region |
| Quantity | Units sold |
| Unit Price | Price per unit |
| Revenue | Total revenue for the order |

If you upload your own file, it just needs columns roughly matching:
Date, Product, Category, Region, Quantity, Revenue.

## Deploy for free (Streamlit Community Cloud)

1. Push this folder to a new GitHub repository.
2. Go to https://share.streamlit.io, sign in with GitHub.
3. Click "New app", select the repo, branch, and set the main file to `app.py`.
4. Click "Deploy" — you'll get a public URL like `https://your-app-name.streamlit.app`.
