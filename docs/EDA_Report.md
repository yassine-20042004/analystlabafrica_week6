# HealthConnect Rwanda Healthcare Analytics & AI Transformation
## Exploratory Data Analysis (EDA) Report
**AnalystLab Africa Experience Lab Internship Programme — Official Week 6 Deliverable**

---

### 📋 Document Control
| Field | Value |
| :--- | :--- |
| **Programme** | AnalystLab Africa Experience Lab |
| **Project Title** | Enterprise Healthcare Analytics, Artificial Intelligence and Digital Transformation System |
| **Track** | **Track 2 — Data Science Track** |
| **Organization** | HealthConnect Rwanda |
| **Document** | Comprehensive Exploratory Data Analysis (EDA) Report |
| **Version** | 1.0 (Final Enterprise Release) |
| **Datasets Analyzed** | 27 Interconnected Enterprise Tables (Demographics, Clinical, Operations, Finance, Feedback) |
| **Author** | Lead Healthcare Data Scientist |

---

## 1. Executive Overview

This report provides an in-depth exploratory data analysis of HealthConnect Rwanda's national healthcare system. Operating 20 hospitals and specialized care centers across all 5 provinces of Rwanda, HealthConnect Rwanda recorded **60,809 patient visits** and generated **1.132 Billion RWF** in gross billing revenue during 2026.

Our exploratory analysis investigates five strategic operational dimensions:
1. **Patient Population Demographics**: Profiling 20,000 registered citizens across age, gender, blood group, geography, and chronic disease morbidities.
2. **Clinical Journeys & Service Utilization**: Tracing 5,000 detailed patient encounters across consultations, diagnostic evaluations, lab investigations, pharmacy dispensing, inpatient admissions, and tertiary referrals.
3. **Operational Resources & Staffing**: Assessing clinical workload across 1,250 healthcare workers (350 doctors, 700 nurses, 200 allied staff), 2,000 inpatient beds, and 200 medical departments.
4. **Financial Performance & Invoicing**: Analyzing 60,000 billing transactions, payment channels, and 42,036 insurance claims.
5. **Patient Experience & Sentiment**: Analyzing 21,064 patient feedback evaluations to identify systemic drivers of satisfaction and operational friction.

---

## 2. Patient Demographics & Population Health Profile

### 2.1 Age and Gender Structure
- **Population Size**: 20,000 registered patients in the national master index.
- **Gender Balance**: The patient population displays near-perfect parity with **10,090 males (50.45%)** and **9,910 females (49.55%)**.
- **Age Distribution**: 
  - Mean Patient Age: **45.03 years** ($\pm 26.26$ years standard deviation).
  - Median Age: **45.00 years** (Range: 0 to 90 years).
  - Age Cohort Breakdown:
    - *Pediatric (0–17 years)*: 3,880 patients (19.40%)
    - *Young Adults (18–35 years)*: 3,736 patients (18.68%)
    - *Middle-Aged (36–55 years)*: 4,552 patients (22.76%)
    - *Seniors (56–65 years)*: 2,232 patients (11.16%)
    - *Geriatric (>65 years)*: 5,600 patients (28.00%)
- *Figure Reference*: See [`reports/figures/fig01_patient_age_gender_distribution.png`](../reports/figures/fig01_patient_age_gender_distribution.png) for the demographic pyramid and histogram.

### 2.2 Physical Health Indicators & BMI
- Mean Body Mass Index (BMI): **30.04 kg/m²** ($\pm 10.43$, range: 11.10 to 61.20).
- In accordance with World Health Organization (WHO) classifications, approximately 46.8% of adult patients present with elevated BMI values ($\ge 30.0$), indicating an elevated epidemiological risk for metabolic and cardiovascular complications.

### 2.3 Chronic Disease Burden
Out of 20,000 registered citizens, **14,929 patients (74.65%)** present with at least one documented chronic morbidity:
- **Asthma**: 4,996 patients (24.98%)
- **Hypertension**: 4,988 patients (24.94%)
- **Type 2 Diabetes**: 4,945 patients (24.73%)
- **No Documented Chronic Morbidity**: 5,071 patients (25.35%)
- *Clinical Insight*: The uniform tripartite spread across asthma, hypertension, and diabetes reflects widespread non-communicable disease (NCD) prevalence across Rwanda, underscoring the urgent necessity of standardized community health screening and outpatient disease management programs.
- *Figure Reference*: See [`reports/figures/fig02_chronic_disease_and_diagnoses_severity.png`](../reports/figures/fig02_chronic_disease_and_diagnoses_severity.png).

### 2.4 Geographic Distribution Across Rwanda
Patient registrations are distributed across all 5 provinces, 30 districts, 120 sectors, and 480 villages:
- **Kigali City**: 4,028 patients (20.14%) — highest consultation intensity per capita.
- **Eastern Province**: 3,982 patients (19.91%)
- **Western Province**: 4,015 patients (20.08%)
- **Northern Province**: 3,991 patients (19.95%)
- **Southern Province**: 3,984 patients (19.92%)
- *Figure Reference*: See [`reports/figures/fig13_province_patient_distribution.png`](../reports/figures/fig13_province_patient_distribution.png).

---

## 3. Clinical Workflow & Patient Journey Analysis

Analyzing the 5,000 clinical cohort encounters reveals the following clinical pathway metrics:

```
[Patient Arrival] ──> [Consultation / Triage] ──> [Lab Investigations (45.4%)]
                                │                               │
                                ├──> [Pharmacy Dispensing (80.1%)]
                                │
                                ├──> [Inpatient Admission (11.7%)] ──> Mean Stay: 5.49 Days
                                │
                                └──> [Tertiary Referral (8.3%)] ───> Inter-Facility Transfer
```

### 3.1 Top Clinical Diagnoses & Severity
Across the clinical cohort, five principal conditions account for primary clinical encounters:
1. **Hypertension**: 1,059 cases (21.18%)
2. **Type 2 Diabetes**: 1,012 cases (20.24%)
3. **Upper Respiratory Infection**: 988 cases (19.76%)
4. **Malaria**: 976 cases (19.52%)
5. **Gastritis**: 965 cases (19.30%)

Clinical severity breakdown:
- **Mild**: 1,682 encounters (33.64%) — managed via routine outpatient protocols.
- **Moderate**: 1,696 encounters (33.92%) — required diagnostic lab tests or specialist consultations.
- **Severe**: 1,622 encounters (32.44%) — primary candidates for immediate hospital admission.

### 3.2 Laboratory Test Utilization & Positivity Rates
- **Lab Request Rate**: 2,272 out of 5,000 appointments (**45.44%**) included formal diagnostic laboratory orders.
- **Most Requested Laboratory Tests**:
  1. *Malaria Rapid / Smear*: 1,272 tests (55.99% of all ordered tests)
  2. *Complete Blood Count (CBC)*: 498 tests (21.92%)
  3. *Urinalysis*: 262 tests (11.53%)
  4. *Blood Glucose / HbA1c*: 240 tests (10.56%)
- **Positivity / Abnormal Rate**: **50.3% of tests returned abnormal findings**, validating strong physician diagnostic acumen at initial triage.

### 3.3 Prescription & Medication Patterns
- **Prescription Rate**: 4,003 out of 5,000 appointments (**80.06%**) resulted in pharmacological dispensing.
- **Top 5 Prescribed Medications**:
  1. *Amlodipine* (Anti-hypertensive): 1,068 prescriptions (26.68%)
  2. *Amoxicillin* (Broad-spectrum antibiotic): 998 prescriptions (24.93%)
  3. *Metformin* (Anti-diabetic): 984 prescriptions (24.58%)
  4. *Artemether-Lumefantrine* (Anti-malarial): 485 prescriptions (12.12%)
  5. *Omeprazole* (Proton-pump inhibitor): 468 prescriptions (11.69%)

### 3.4 Inpatient Admissions & Length of Stay (LOS)
- **Admission Rate**: 586 out of 5,000 encounters (**11.72%**) required formal inpatient admission.
- **Length of Stay**:
  - Inpatient Mean Stay: **5.49 days** ($\pm 2.87$ days, range: 1 to 10 days).
  - Outpatient Care: 4,414 encounters (88.28%, 0 bed days).
  - Short Stay (1–3 days): 155 admissions (3.10%).
  - Medium Stay (4–7 days): 245 admissions (4.90%).
  - Extended Stay (>7 days): 186 admissions (3.72%).
- *Figure Reference*: See [`reports/figures/fig14_admission_age_density_by_chronic.png`](../reports/figures/fig14_admission_age_density_by_chronic.png).

### 3.5 Inter-Facility Referral Patterns
- **Referral Rate**: 415 appointments (**8.30%**) required patient referral to external facilities.
- **Destination Facilities**: Referral distribution was evenly dispersed across regional referral centers (top recipients: `HF014`, `HF007`, `HF006`, and `HF019`), reflecting balanced geographic referral networks.

---

## 4. Operational Analysis & Clinical Workforce Capacity

### 4.1 Healthcare Workforce Distribution
HealthConnect Rwanda employs a total clinical and operational staff of **1,250 personnel**:
- **Doctors**: 350 licensed physicians (Mean experience: 13.02 years, range: 1 to 25 years).
- **Nurses**: 700 registered nurses (Mean experience: 13.15 years).
- **Allied Healthcare Professionals**:
  - *Administrative Staff*: 80 personnel
  - *Pharmacists*: 50 licensed pharmacists
  - *Laboratory Scientists*: 40 medical technologists
  - *Radiographers*: 30 imaging specialists
- **Clinical Staffing Ratios**:
  - Doctor-to-Nurse Ratio: **1 : 2.0** (meeting national minimum guidelines).
  - Staff-to-Patient Consultation Ratio: 1 full-time clinical staff member per 48.6 annual appointments.

### 4.2 Facility Capacity & Bed Utilization
- **Total Facilities**: 20 medical centers (`HF001` to `HF020`).
- **Bed Capacity**: 2,000 total inpatient beds across 400 hospital rooms (100 beds per facility).
- **Bed Availability**: System-wide bed availability averages 62.4%, with peak admissions occurring during rainy season months (February–May and October–November).
- *Figure Reference*: See [`reports/figures/fig12_facility_performance_leaderboard.png`](../reports/figures/fig12_facility_performance_leaderboard.png) for composite facility performance scores.

---

## 5. Financial Performance & Revenue Cycle Analysis

### 5.1 System-Wide Revenue Generation
- **Total Gross Revenue (2026)**: **1,132,677,500 RWF** across 60,809 visits.
- **Average Revenue per Consultation**: **18,627 RWF** (system-wide aggregate) and **155,156.70 RWF** (for complex encounters involving diagnostic investigations and inpatient admissions).
- **Monthly Revenue Seasonality**:
  - Peak Revenue Months: September (145.76M RWF) and May (134.09M RWF).
  - Lowest Revenue Months: December (66.69M RWF) and August (69.84M RWF).

### 5.2 Billing Status & Outstanding Receivables
Across the 60,000 billing transactions:
- **Paid**: 20,145 invoices (**33.58%**) — 3.12 Billion RWF settled.
- **Partially Paid**: 19,971 invoices (**33.28%**) — 1.54 Billion RWF outstanding balance.
- **Pending**: 19,884 invoices (**33.14%**) — 3.08 Billion RWF pending settlement.
- *Critical Operational Risk*: Over **4.62 Billion RWF** in gross receivables remain unsettled due to extended reimbursement review windows by insurance payers.

### 5.3 Insurance Claim Processing & Payment Methods
- **Insurance Coverage Rate**: **70.06% of patients** are covered under health insurance schemes (42,036 claims).
- **Insurance Provider Market Share**:
  1. *Radiant Insurance*: 10,644 claims (25.32%)
  2. *RSSB (Rwanda Social Security Board / Mutuelle)*: 10,511 claims (25.00%)
  3. *Private Insurers*: 10,508 claims (25.00%)
  4. *MMI (Military Medical Insurance)*: 10,373 claims (24.68%)
- **Claim Approval Velocity**: Exactly 21,008 claims (49.98%) are marked as `Approved`, while 21,028 claims (50.02%) remain `Pending`.
- **Payment Method Distribution**:
  - *Card (POS / Debit)*: 25.24%
  - *Mobile Money (MoMo / Airtel Money)*: 25.03%
  - *Direct Insurance Billing*: 24.91%
  - *Cash*: 24.82%
- *Figure Reference*: See [`reports/figures/fig04_billing_distribution_by_insurance.png`](../reports/figures/fig04_billing_distribution_by_insurance.png).

---

## 6. Patient Experience & Satisfaction Telemetry

### 6.1 Feedback Volume & Rating Profile
- **Feedback Survey Volume**: 21,064 evaluations recorded in the system.
- **Mean Satisfaction Rating**: **3.01 / 5.00** ($\pm 1.41$).
- **Rating Distribution**:
  - ⭐ 1 Star (Poor): 4,280 reviews (20.32%)
  - ⭐⭐ 2 Stars (Fair): 4,339 reviews (20.60%)
  - ⭐⭐⭐ 3 Stars (Good): 4,634 reviews (22.00%)
  - ⭐⭐⭐⭐ 4 Stars (Very Good): 3,901 reviews (18.52%)
  - ⭐⭐⭐⭐⭐ 5 Stars (Excellent): 3,910 reviews (18.56%)

### 6.2 Key Drivers of Patient Dissatisfaction
Natural language processing on patient survey comments identified three recurrent complaints:
1. **Extended Consultation Waiting Times**: Correlated with department workload spikes in Emergency and Internal Medicine.
2. **Pharmacy Stockouts**: Delays in dispensing chronic medication refills (Amlodipine and Metformin).
3. **Billing Clearance Bottlenecks**: Delays at checkout counters reconciling pending insurance copays.
- *Figure Reference*: See [`reports/figures/fig05_satisfaction_violin_by_facility_type.png`](../reports/figures/fig05_satisfaction_violin_by_facility_type.png) and [`reports/figures/fig15_workload_vs_satisfaction_regression.png`](../reports/figures/fig15_workload_vs_satisfaction_regression.png).

---
*Report certified by HealthConnect Rwanda Analytics & AI Transformation Team — Version 1.0 Release.*
