# RetailMind AI

AI-Powered Flexible Sales Insight Generator

## Overview

RetailMind AI is an end-to-end analytics platform that transforms raw retail sales datasets into interactive dashboards, AI-generated business insights, strategic recommendations, conversational business Q&A, and downloadable business reports.

Unlike traditional dashboards that require fixed schemas, RetailMind AI supports intelligent schema detection and flexible business field mapping, allowing different sales datasets to be standardized and analyzed through a unified analytics pipeline.

The platform combines data engineering, business intelligence, visualization, and generative AI to help business users discover opportunities, identify risks, and make data-driven decisions faster.

---

## Business Impact

RetailMind AI enables organizations to:

* Analyze sales performance without SQL knowledge
* Automatically detect business opportunities and risks
* Identify top-performing and underperforming products, stores, and regions
* Generate AI-powered business insights from KPI summaries
* Receive strategic recommendations based on actual business metrics
* Interact with business data using natural language
* Export executive-ready AI business reports

The platform significantly reduces manual reporting effort and accelerates business decision-making through AI-assisted analytics.

---

## Key Features

### Smart Schema Detection

* Automatic CSV column detection
* Confidence-based field matching
* Business-oriented schema mapping
* Dataset compatibility validation
* Flexible support for different sales datasets

### Schema Mapping Engine

* Manual override of detected fields
* Required-field validation
* Optional business field enrichment
* Mapping summary generation
* Field availability analysis

### Data Quality Engine

* Missing value detection
* Duplicate record detection
* Outlier analysis
* Data completeness scoring
* Dataset health assessment

### Executive KPI Dashboard

* Total Revenue
* Gross Profit / Gross Income
* Total Orders
* Quantity Sold
* Average Order Value
* Average Customer Rating

### Interactive Analytics

* Revenue by Product Category
* Revenue by Store / Branch
* Revenue by Region / City
* Customer Segment Analysis
* Payment Method Analysis
* Customer Satisfaction Analysis

### AI Business Intelligence

#### AI Insights

Generate executive-level business insights including:

* Executive Summary
* Key Business Insights
* Business Risks
* Business Opportunities

#### AI Recommendations

Generate strategic recommendations for:

* Revenue Growth
* Customer Experience
* Product Strategy
* Operational Improvement

#### AI Business Chatbot

Natural language business Q&A:

* Ask business questions
* KPI-based responses
* Evidence-supported answers
* Business interpretation layer

### AI Business Reporting

Generate downloadable Markdown reports containing:

* Dataset Overview
* KPI Summary
* Top Performers
* Segment Analysis
* AI Insights
* AI Recommendations
* Chat History
* AI Context
* Data Quality Results

---

## Application Screenshots

### Dashboard

Add screenshot here:

assets/dashboard.png

### AI Insights

Add screenshot here:

assets/ai_insights.png

### AI Recommendations

Add screenshot here:

assets/recommendations.png

### AI Chatbot

Add screenshot here:

assets/chatbot.png

---

## Tech Stack

### Frontend

* Streamlit

### Data Processing

* Pandas
* NumPy

### Visualization

* Plotly

### AI

* Google Gemini 3.5 Flash

### Environment

* Python 3.11+

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
├── assets/
├── data/
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

Create a `.env` file:

```env
GOOGLE_API_KEY=YOUR_API_KEY
```

---

## Run Application

```bash
streamlit run app.py
```

---

## Future Enhancements

* PDF Report Export
* Multi-dataset Benchmarking
* Forecasting & Demand Prediction
* Customer Segmentation using Machine Learning
* Executive AI Agent
* Cloud Deployment

---

## Author

Dat Pham


GitHub:
https://github.com/PhamDat-05/retailmind-ai
