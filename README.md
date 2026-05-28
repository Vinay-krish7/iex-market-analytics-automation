# IEX Market Analytics & Reporting Automation


## Overview

Python-based automation system developed for extracting, analyzing, visualizing, and distributing electricity market data from the Indian Energy Exchange (IEX).

The project automates:

* Market data extraction from the IEX portal
* Data cleaning and processing
* Hourly price and volume trend analysis
* Automated visualization generation
* HTML/Excel report creation
* Outlook email dissemination to stakeholders

The automation currently supports:

* Day Ahead Market (DAM)
* Real-Time Market (RTM)
* Green Day Ahead Market (GDAM)

---

## Key Features

* Automated IEX market data extraction using Selenium
* Dynamic filter selection and web interaction
* Hourly price and volume trend analytics
* Automated chart generation using Matplotlib
* HTML and Excel summary report generation
* Outlook email automation with inline visualizations
* Logging and exception handling framework
* Automated weighted market clearing price calculations
* Market-wise analytics workflow (DAM / RTM / GDAM)

---

## Technologies Used

* Python
* Selenium
* Pandas
* Matplotlib
* Outlook COM Automation (`win32com`)
* Logging
* DateTime Utilities
* HTML Reporting
* CSV / Excel Processing

---

## Workflow Architecture

```text
IEX Website
      ↓
Selenium Web Scraping
      ↓
Data Extraction & Cleaning
      ↓
Market Analytics Processing
      ↓
Price & Volume Visualization
      ↓
HTML / Excel Report Generation
      ↓
Automated Outlook Mail Trigger
```

---

## Project Structure

```text
iex-market-analytics-automation/
│
├── dam_market_automation.py
├── rtm_market_automation.py
├── gdam_market_automation.py
├── logs/
├── reports/
├── plots/
├── screenshots/
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Market Analytics Covered

### Day Ahead Market (DAM)

* Hourly MCP trend analysis
* Volume analysis
* Market clearing analytics

### Real-Time Market (RTM)

* Intraday price trend monitoring
* Real-time volume analytics
* Volatility tracking

### Green Day Ahead Market (GDAM)

* Renewable energy market analytics
* Weighted MCP trend analysis
* Solar / Hydro / Non-Solar volume analytics

---

## Outputs Generated

The automation generates:

* CSV Reports
* Excel Summary Files
* HTML Reports
* Price vs Volume Trend Plots
* Automated Outlook Email Notifications

---

## Sample Analytics

The generated reports include:

* Market Clearing Price (MCP)
* Weighted MCP
* Final Scheduled Volume (FSV)
* Purchase Bid Volume
* Sell Bid Volume
* Renewable market participation trends

---

## Setup Instructions

### 1. Clone Repository

```bash
git clone <repository-url>
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure ChromeDriver

Update ChromeDriver path in the script:

```python
service = Service("path_to_chromedriver")
```

### 4. Configure Output Directories

Update:

* report paths
* plot paths
* logging paths
* Outlook recipient configuration

### 5. Execute Script

```bash
python gdam_market_automation.py
```

---

## Future Enhancements

* Power BI integration
* Cloud deployment
* Automated scheduling using Task Scheduler / Airflow
* Historical trend dashboard
* AI-based market trend forecasting
* Database integration
* Multi-market consolidated reporting

---

## Disclaimer

This repository is intended for educational and portfolio purposes. Any confidential company information, directory structures, or stakeholder details have been sanitized prior to publication.
