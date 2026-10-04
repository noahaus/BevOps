# Beverage Order Prioritization Dashboard

## 📊 Project Overview

The **Beverage Order Prioritization Dashboard** is a data analytics project designed to help beverage-based businesses better manage incoming orders across multiple fulfillment channels.

Beverage businesses often receive orders simultaneously through different methods, including:

* 🏪 **In-House Orders** — Customers ordering directly at the counter
* 📱 **Mobile Orders** — Orders placed through a business's mobile application
* 🚗 **Delivery Orders** — Orders placed through third-party platforms such as DoorDash, Uber Eats, and similar services

When multiple orders arrive at the same time, determining which order should be prepared first can become challenging. This project explores a data-driven approach to prioritizing orders based on factors such as **order age, order quantity, fulfillment method, and current order volume**.

The goal is to create a dashboard that provides employees or managers with a clear view of which orders require attention and why.

---

## 🎯 Project Objectives

The primary objectives of this project are to:

1. Analyze incoming beverage orders across different fulfillment methods.
2. Determine how orders can be prioritized using measurable criteria.
3. Account for the amount of time an order has been waiting.
4. Consider the number of items included in an order.
5. Analyze how different fulfillment methods affect prioritization.
6. Create a dashboard that communicates order priority clearly.
7. Develop a repeatable prioritization framework that could potentially be adapted to different beverage businesses.

---

## 🧾 Order Fulfillment Methods

The dashboard will categorize orders into three primary fulfillment methods.

| Method       | Description                                            |
| ------------ | ------------------------------------------------------ |
| **In-House** | Orders placed directly at the business                 |
| **Mobile**   | Orders placed through the company's mobile application |
| **Delivery** | Orders placed through third-party delivery platforms   |

Delivery orders may include platforms such as:

* DoorDash
* Uber Eats
* Grubhub
* Other third-party delivery services

---

## ⚖️ Order Prioritization Criteria

The project will evaluate multiple variables when determining an order's priority.

### 1. ⏱️ Order Age

The amount of time an order has been waiting is one of the primary factors.

For example:

| Wait Time     | Priority |
| ------------- | -------- |
| 0–5 minutes   | Low      |
| 5–10 minutes  | Moderate |
| 10–15 minutes | High     |
| 15+ minutes   | Critical |

These thresholds are configurable and can be adjusted based on business requirements.

---

### 2. 🧋 Order Quantity

Larger orders may require additional preparation time and resources.

For example:

| Items in Order | Consideration |
| -------------: | ------------- |
|            1–2 | Low           |
|            3–5 | Moderate      |
|            6–9 | High          |
|            10+ | Very High     |

Quantity should not automatically determine priority. Instead, it can be combined with wait time and fulfillment method.

---

### 3. 📦 Fulfillment Method

Different fulfillment methods may require different operational considerations.

For example:

**In-House**

* Customer may already be waiting inside the store.
* Orders can potentially be handed directly to the customer.

**Mobile**

* Customer may arrive expecting the order to be ready.
* Preparation time can affect pickup experience.

**Delivery**

* A driver may be waiting for the order.
* Additional delivery time may affect the customer's experience.

The dashboard can therefore assign different weights to each fulfillment method depending on the business's operational strategy.

---

# 🧮 Proposed Priority Score

One potential approach is to calculate a **Priority Score** for each order.

For example:

```text
Priority Score =
    Wait Time Score
    + Quantity Score
    + Fulfillment Method Score
```

An example weighting system could be:

| Factor             | Weight |
| ------------------ | -----: |
| Wait Time          |    50% |
| Order Quantity     |    20% |
| Fulfillment Method |    30% |

> **Note:** These weights are examples for the prototype. The project will evaluate whether different weighting strategies produce more useful prioritization results.

The resulting score could then categorize each order:

```text
0–30   → Low Priority
31–60  → Moderate Priority
61–80  → High Priority
81–100 → Critical Priority
```

---

# 📈 Dashboard

The dashboard will provide an operational overview of current orders.

Potential dashboard components include:

### Key Performance Indicators

* Total Active Orders
* Average Wait Time
* Longest Waiting Order
* Orders by Fulfillment Method
* High/Critical Priority Orders
* Average Items per Order

### Visualizations

* Orders by Fulfillment Method
* Orders by Priority Level
* Average Wait Time by Fulfillment Method
* Order Volume Over Time
* Distribution of Order Quantities
* Priority Score Distribution

### Order Queue

A central component of the dashboard will be a prioritized order queue.

Example:

| Order | Method   | Items | Wait Time | Priority Score | Priority    |
| ----- | -------- | ----: | --------: | -------------: | ----------- |
| #1042 | Mobile   |     3 |    14 min |             82 | 🔴 Critical |
| #1039 | Delivery |     5 |    11 min |             76 | 🟠 High     |
| #1045 | In-House |     2 |     8 min |             58 | 🟡 Moderate |
| #1047 | Mobile   |     1 |     3 min |             25 | 🟢 Low      |

This allows employees or managers to quickly identify which orders should receive attention.

---

# 🔄 Example Workflow

The proposed system follows this general process:

```text
Incoming Order
       ↓
Identify Fulfillment Method
       ↓
Calculate Order Age
       ↓
Determine Order Quantity
       ↓
Calculate Priority Score
       ↓
Assign Priority Level
       ↓
Display on Dashboard
       ↓
Employee Processes Highest-Priority Order
```

---

# 🗂️ Proposed Dataset

The project may use a dataset containing fields such as:

| Column               | Description                       |
| -------------------- | --------------------------------- |
| `order_id`           | Unique order identifier           |
| `order_time`         | Time the order was placed         |
| `fulfillment_method` | In-House, Mobile, or Delivery     |
| `delivery_platform`  | DoorDash, Uber Eats, etc.         |
| `item_quantity`      | Number of items in the order      |
| `order_status`       | Pending, In Progress, Completed   |
| `completion_time`    | Time the order was completed      |
| `wait_time`          | Time between order and completion |
| `priority_score`     | Calculated priority score         |
| `priority_level`     | Low, Moderate, High, or Critical  |

---

# 🛠️ Technologies

The project is intended to use data analytics and visualization tools such as:

* **Python**

  * Pandas
  * NumPy
  * Data cleaning
  * Data transformation
  * Priority-score calculations

* **SQL**

  * Data querying
  * Aggregations
  * Order analysis
  * KPI calculations

* **Dashboard / Visualization**

  * Power BI / Tableau / similar BI platform

* **Git & GitHub**

  * Version control
  * Project documentation
  * Collaboration

---

# ▶️ Running the Dashboard

The order queue in `beverage_order_prioritization_dashboard.html` loads orders from `cafe_pos_data.csv`. Browsers block that file from loading if you open the HTML directly (`file://`), so serve the project folder from a local server.

From the project directory, run:

```bash
python3 -m http.server 8765
```

Then open:

```text
http://127.0.0.1:8765/beverage_order_prioritization_dashboard.html
```

The dashboard should show **3,000 orders** and **6,681 line items** from the CSV. You can filter by channel, store location, day of week, delivery platform, payment method, category, item, items in order, date range, or search (order ID, customer, or item).

If you open the HTML file directly, use **Load CSV** and choose `cafe_pos_data.csv`.

---

# 📁 Project Structure

```text
beverage-order-prioritization/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── python/
│   ├── data_cleaning.py
│   ├── priority_scoring.py
│   └── analysis.py
│
├── sql/
│   ├── order_analysis.sql
│   └── kpi_queries.sql
│
├── dashboard/
│   └── dashboard_files/
│
├── documentation/
│   └── methodology.md
│
├── README.md
└── requirements.txt
```

---

# 🔍 Key Questions

The project will attempt to answer questions such as:

1. Which fulfillment method generates the most orders?
2. Which fulfillment method has the longest average wait time?
3. Does order quantity significantly affect preparation time?
4. Which orders are most likely to become overdue?
5. How does order volume affect average wait time?
6. How should orders be prioritized when multiple orders arrive simultaneously?
7. Does the proposed priority model improve the organization of the order queue?
8. How could the prioritization model be adjusted for different business environments?

---

# 🚀 Future Improvements

Potential future improvements include:

* Real-time order ingestion
* Automated priority recalculation
* Predictive wait-time modeling
* Machine learning-based prioritization
* Employee workload analysis
* Staffing recommendations based on order volume
* Peak-hour analysis
* Integration with point-of-sale systems
* Integration with delivery platforms
* Historical performance tracking

---

# 👥 Project Team

**Developers**

* [Your Name]
* [Friend's Name]

---

# 📌 Project Status

**Status:** 🚧 In Development

This project is currently being developed as a collaborative data analytics project. The prioritization methodology, dataset, and dashboard will be refined throughout development.

---

## 💡 Project Goal

The ultimate goal of this project is to demonstrate how **data can be transformed into an actionable operational tool**.

Rather than simply displaying historical order data, the dashboard is designed to help answer:

> **"Given the orders currently waiting, which order should receive attention next, and what data supports that prioritization?"**
