# RetailMind AI

AI-Powered Flexible Sales Insight Generator

## Overview

RetailMind AI is an end-to-end analytics platform that transforms raw retail sales datasets into interactive dashboards, AI-generated business insights, strategic recommendations, conversational business Q&A, and downloadable business reports.

The system supports flexible CSV schema mapping, automated data quality validation, KPI generation, and LLM-powered business intelligence.

---

## Key Features

### Smart Schema Detection

- Automatic column detection
- Flexible business field mapping
- Dataset compatibility validation

### Data Quality Engine

- Missing value detection
- Duplicate record detection
- Outlier analysis
- Dataset health scoring

### Executive Dashboard

- Revenue KPIs
- Gross Profit KPIs
- Order Metrics
- Customer Metrics

### Interactive Analytics

- Revenue by Product
- Revenue by Branch
- Revenue by Region
- Customer Segmentation
- Payment Method Analysis

### AI Business Intelligence

- AI Business Insights
- AI Strategic Recommendations
- AI Business Chatbot
- Context-Aware Q&A

### AI Business Reports

- Markdown Report Export
- KPI Summary
- Business Risks
- Opportunities
- AI Context
- Chat History

---

## Tech Stack

### Frontend

- Streamlit

### Data Processing

- Pandas
- NumPy

### Visualization

- Plotly

### AI

- Google Gemini 2.5 Flash

### Environment

- Python 3.11+

---

## Project Structure

```text
retailmind-ai/
│
├── app.py
├── requirements.txt
├── README.md
│
├── src/
│   ├── ai_context_builder.py
│   ├── ai_insight_generator.py
│   ├── chat_manager.py
│   ├── data_cleaning.py
│   ├── data_loader.py
│   ├── filters.py
│   ├── kpi_calculator.py
│   ├── report_generator.py
│   ├── schema_mapper.py
│   └── visualizations.py
│
├── data/
├── assets/
└── notebooks/
```

---

## Installation

```bash
git clone https://github.com/PhamDat-05/retailmind-ai.git

cd retailmind-ai

pip install -r requirements.txt
```

---

## Environment Setup

Create:

```bash
.env
```

```env
GOOGLE_API_KEY=YOUR_API_KEY
```

---

## Run

```bash
streamlit run app.py
```

---

## Author

Dat Pham