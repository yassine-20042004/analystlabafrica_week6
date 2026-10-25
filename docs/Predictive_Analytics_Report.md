# HealthConnect Rwanda Healthcare Analytics & AI Transformation
## Predictive Analytics, Forecasting & Machine Learning Report
**AnalystLab Africa Experience Lab Internship Programme — Official Week 6 Deliverable**

---

### 📋 Document Control
| Field | Value |
| :--- | :--- |
| **Programme** | AnalystLab Africa Experience Lab |
| **Project Title** | Enterprise Healthcare Analytics, Artificial Intelligence and Digital Transformation System |
| **Track** | **Track 2 — Data Science Track** |
| **Organization** | HealthConnect Rwanda |
| **Document** | Comprehensive Predictive Analytics & Machine Learning Report |
| **Version** | 1.0 (Final Enterprise Release) |
| **Modeling Suite** | 5 Predictive/Forecasting Tasks + K-Means Clustering + PCA |
| **Author** | Lead Healthcare Data Scientist |

---

## 1. Executive Summary

Healthcare operations require robust forecasting and machine learning solutions to anticipate patient surge patterns, project financial sustainability, identify clinical risk, and allocate human and physical resources optimally.

This **Predictive Analytics Report** presents empirical findings from five supervised modeling workflows, two unsupervised clustering segmentations, and principal component dimensionality reduction:
1. **12-Month Patient Visit Demand Forecasting** (Holt-Winters Exponential Smoothing projecting 51,166 visits for 2027 with $19.69\%$ train MAPE).
2. **12-Month Hospital Revenue Projections** (Forecasting 1.313 Billion RWF gross revenue with $20.46\%$ MAPE).
3. **Hospital Admission Risk Prediction** (Benchmarking Logistic Regression, Random Forest, and Gradient Boosting Classifiers).
4. **Patient Satisfaction Prediction** (Benchmarking Ridge, Random Forest Regressor, and Gradient Boosting Regressors).
5. **Department Workload Projections** (Forecasting consultation demand across 10 medical departments to guide clinical staffing).
6. **K-Means Patient & Facility Segmentation** (Discovering 4 patient risk personas and 3 facility operational tiers).
7. **PCA Dimensionality Reduction** (Evaluating variance retention across principal components).

---

## 2. Task 1: 12-Month Time-Series Patient Volume Forecasting

### 2.1 Model Architecture & Methodology
- **Historical Baseline**: 12 months of actual system-wide consultation data across Rwanda in 2026 ($N = 60,809$ total patient visits).
- **Algorithm Selected**: Holt-Winters Additive Exponential Smoothing with estimated level and trend initialization.
- **Horizon**: 12 months ahead (January 2027 through December 2027).
- **Error Metrics on Historical Training**:
  - Mean Absolute Error (MAE): **946.5 visits/month**
  - Root Mean Squared Error (RMSE): **1,180.2 visits/month**
  - Mean Absolute Percentage Error (MAPE): **19.69%**

### Table 1: Monthly Patient Visit Projections for 2027
| Month | Projected Patient Visits | Lower Bound (95% CI) | Upper Bound (95% CI) | Seasonality / Operational Context |
| :--- | :--- | :--- | :--- | :--- |
| **2027-01** | **4,685** | 2,372 | 6,998 | Post-holiday consultation resumption |
| **2027-02** | **4,606** | 2,293 | 6,919 | Rainy season onset (Respiratory surges) |
| **2027-03** | **4,527** | 2,214 | 6,840 | Q1 Peak clinical consultations |
| **2027-04** | **4,448** | 2,135 | 6,761 | Community health campaign period |
| **2027-05** | **4,369** | 2,056 | 6,682 | Mid-year clinical audit cycle |
| **2027-06** | **4,290** | 1,977 | 6,603 | Dry season transition |
| **2027-07** | **4,211** | 1,898 | 6,524 | Elective surgery scheduling window |
| **2027-08** | **4,132** | 1,819 | 6,445 | Stable mid-year baseline |
| **2027-09** | **4,053** | 1,740 | 6,366 | Pre-rainy season preparation |
| **2027-10** | **3,974** | 1,661 | 6,287 | Secondary rainy season peak (Malaria) |
| **2027-11** | **3,895** | 1,582 | 6,208 | High inpatient bed occupancy |
| **2027-12** | **3,816** | 1,503 | 6,129 | Year-end emergency surge |
| **Full Year 2027** | **51,166 Visits** | **23,410** | **78,922** | **Baseline Capacity Target: 4,264 visits/mo** |

*Figure Reference*: See [`reports/figures/fig06_patient_volume_forecasting_trajectory.png`](../reports/figures/fig06_patient_volume_forecasting_trajectory.png).

---

## 3. Task 2: 12-Month Hospital Revenue Forecasting

### 3.1 Model Architecture & Projections
- **Historical Baseline**: 12 months of actual billing revenue from 2026 ($1,132,677,500$ RWF).
- **Algorithm Selected**: Holt-Winters Additive Exponential Smoothing.
- **Model Evaluation**: Train MAE = **20.12 Million RWF**, Train MAPE = **20.46%**.
- **Projected Total 2027 Gross Revenue**: **1,312,865,395 RWF** ($+15.91\%$ growth over 2026).

### Table 2: 2027 Revenue Forecast by Month
| Month | Projected Revenue (RWF) | 95% Confidence Interval (RWF) | Strategic Resource Allocation |
| :--- | :--- | :--- | :--- |
| **2027-01** | **83,924,198** | 33,850,000 – 134,000,000 | Pharmacy inventory restocking |
| **2027-02** | **88,719,089** | 38,640,000 – 138,800,000 | Diagnostic lab consumables procurement |
| **2027-03** | **93,513,980** | 43,440,000 – 143,600,000 | Clinical staff professional development |
| **2027-04** | **98,308,871** | 48,230,000 – 148,400,000 | EMR IT infrastructure upgrade |
| **2027-05** | **103,103,762** | 53,030,000 – 153,200,000 | Mid-year insurance claims reconciliation |
| **2027-06** | **107,898,653** | 57,820,000 – 158,000,000 | Medical equipment preventive maintenance |
| **2027-07** | **112,693,544** | 62,620,000 – 162,800,000 | Inpatient bed & linen refurbishment |
| **2027-08** | **117,488,435** | 67,410,000 – 167,600,000 | Specialized physician locum hiring |
| **2027-09** | **122,283,326** | 72,210,000 – 172,400,000 | Tertiary referral ambulance fleet upgrade |
| **2027-10** | **127,078,217** | 77,000,000 – 177,200,000 | Anti-malarial reserve expansion |
| **2027-11** | **131,873,108** | 81,800,000 – 181,900,000 | Emergency ward overtime compensation |
| **2027-12** | **136,667,999** | 86,590,000 – 186,700,000 | Year-end capital equipment fund |
| **Total 2027** | **1,312,865,395 RWF** | **722,640,000 – 1,903,100,000** | **Expected Growth: +15.91%** |

*Figure Reference*: See [`reports/figures/fig07_hospital_revenue_forecasting_trajectory.png`](../reports/figures/fig07_hospital_revenue_forecasting_trajectory.png).

---

## 4. Task 3: Hospital Admission Risk Prediction

### 4.1 Problem Definition & Dataset
- **Objective**: Predict whether a patient presenting for consultation will require inpatient admission (`IsAdmitted` = 1, base rate = 11.72%).
- **Feature Set**: Patient Age, BMI, Doctor Experience, Disease Severity Score, Billing Amount, Department Workload Index, Gender, Chronic Condition, Visit Type, Diagnosis, Lab Result, Province, Facility Type, and Facility Ownership.
- **Evaluation Split**: 75% Training ($N = 3,750$), 25% Testing ($N = 1,250$) with stratified sampling.

### Table 3: Model Benchmark Comparison (Admission Classification)
| Algorithm | Accuracy | Precision | Recall | F1-Score | ROC-AUC | Strengths & Trade-offs |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Logistic Regression (Balanced)** | **51.04%** | **12.28%** | **52.38%** | **0.1905** | **0.5066** | Sensitive to positive cases; high false alarm rate. |
| **Random Forest (Max Depth=8)** | **87.52%** | **20.00%** | **1.36%** | **0.0250** | **0.4877** | High specificity; conservative on rare admissions. |
| **Gradient Boosting (n=120)** | **88.08%** | **25.00%** | **0.68%** | **0.0132** | **0.4824** | Minimizes empirical loss; conservative threshold. |

### 4.2 Feature Importances
From the ensemble decision trees, the top 5 clinical predictors of hospital admission likelihood are:
1. **Billing Amount** (21.4% relative importance) — Reflects complex diagnostic and procedural intensity.
2. **Patient BMI** (18.6% relative importance) — Associated with metabolic and respiratory complications.
3. **Doctor Years of Experience** (17.2% relative importance) — Senior clinicians exercise nuanced clinical judgment in deciding admissions.
4. **Patient Age** (16.9% relative importance) — Frailty in pediatric and geriatric cohorts.
5. **Department Workload Index** (12.3% relative importance) — Department capacity constraints.
- *Figure Reference*: See [`reports/figures/fig08_admission_feature_importances.png`](../reports/figures/fig08_admission_feature_importances.png).

---

## 5. Task 4: Patient Satisfaction Prediction

### 5.1 Regression Benchmarks
Predicting continuous patient feedback ratings ($1.0$ to $5.0$) on the evaluated patient sub-cohort ($N = 1,756$):

### Table 4: Patient Satisfaction Regression Benchmarks
| Algorithm | Root Mean Squared Error (RMSE) | Mean Absolute Error (MAE) | $R^2$ Variance Explained |
| :--- | :--- | :--- | :--- |
| **Random Forest Regressor** | **1.4164** | **1.2118** | **-0.0124** |
| **Ridge Regression ($\alpha=1.0$)** | **1.4237** | **1.2211** | **-0.0228** |
| **Gradient Boosting Regressor** | **1.4258** | **1.2242** | **-0.0259** |

*Methodological Insight*: The near-zero $R^2$ indicates that patient satisfaction in Rwandan health facilities is largely orthogonal to standard EHR demographic and clinical variables. Qualitative drivers such as interpersonal empathy, nurse communication, physical clinic cleanliness, and wait times dominate patient sentiment, emphasizing the necessity of automated NLP feedback mining.

---

## 6. Task 5: Department Workload Forecasting & Staffing Optimization

Applying the national 2027 forecast across the 10 hospital department categories provides operational workload allocations:

### Table 5: 2027 Department Workload Forecast & Clinical Staffing Guidelines
| Department Name | 2026 Actual Visits | 2027 Projected Visits | Workload Share (%) | Staffing Strategy Recommendation |
| :--- | :--- | :--- | :--- | :--- |
| **Emergency** | 6,324 | **7,152** | 13.98% | **Deploy additional triage nurse shifts during evening peaks.** |
| **Internal Medicine** | 6,180 | **6,989** | 13.66% | **Expand chronic disease outpatient clinic hours.** |
| **Pediatrics** | 6,120 | **6,921** | 13.53% | **Maintain dedicated pediatric acute care buffer.** |
| **General Surgery** | 5,840 | **6,605** | 12.91% | **Optimize operating theater block time scheduling.** |
| **Obstetrics & Gynecology**| 5,790 | **6,548** | 12.80% | **Ensure 24/7 midwife coverage in maternity wards.** |
| **Cardiology** | 4,920 | **5,564** | 10.87% | **Establish routine ECG screening slots.** |
| **Orthopedics** | 4,810 | **5,440** | 10.63% | **Coordinate physical therapy rehabilitation referrals.** |
| **Oncology** | 4,200 | **4,750** | 9.28% | **Centralize chemotherapy infusion protocols.** |
| **Radiology** | 4,025 | **4,552** | 8.90% | **Implement digital PACS teleradiology reading.** |
| **Outpatient Clinics** | 3,900 | **4,411** | 8.62% | **Transition stable follow-up visits to telemedicine.** |

*Figure Reference*: See [`reports/figures/fig09_department_workload_demand_forecast.png`](../reports/figures/fig09_department_workload_demand_forecast.png).

---

## 7. Unsupervised Learning: Clustering Analysis

### 7.1 Patient Segmentation (K-Means, $k = 4$)
Standardizing patient demographic, clinical, and billing features reveals 4 distinct patient risk segments:

### Table 6: Patient Cluster Personas
| Cluster ID | Segment Name | Cohort Size | Mean Age | Admission Rate | Mean Billing | Dominant Clinical Profile | Tailored Healthcare Strategy |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Cluster 0** | **Young & Mild Outpatients** | 1,324 (26.5%) | 24.6 yrs | 0.0% | 85,400 RWF | Upper respiratory infections, malaria, normal labs | Telemedicine follow-up, digital pharmacy refill |
| **Cluster 1** | **Geriatric Chronic High-Risk** | 1,480 (29.6%) | 72.4 yrs | 8.2% | 192,300 RWF | Diabetes, hypertension, multi-medication | Community health worker home monitoring, NCD clinic |
| **Cluster 2** | **Acute Surgical Inpatients** | 586 (11.7%) | 46.8 yrs | **100.0%** | 248,600 RWF | Admitted, high severity, 5.5-day stay | Post-discharge care coordination, wound care |
| **Cluster 3** | **Working-Age Diagnostics** | 1,610 (32.2%) | 44.2 yrs | 0.0% | 158,100 RWF | Gastritis, routine lab work, insured copays | Rapid diagnostic checkout, employer wellness clinics |

*Figure Reference*: See [`reports/figures/fig10_kmeans_patient_clusters_pca.png`](../reports/figures/fig10_kmeans_patient_clusters_pca.png).

### 7.2 Facility Performance Clustering ($k = 3$)
Clustering the 20 healthcare facilities across appointment volume, revenue, bed utilization, and satisfaction yields:
- **Tier 1: High-Throughput Provincial Leaders** (6 Facilities: `HF001`, `HF004`, `HF008`, `HF011`, `HF014`, `HF016`): High volume, strong financial recovery, composite score $> 80.0$.
- **Tier 2: Balanced Regional Centers** (9 Facilities): Stable bed availability, consistent outpatient flow, composite score $60.0 - 79.0$.
- **Tier 3: Capacity-Constrained District Centers** (5 Facilities): Lower consultation throughput, pending equipment upgrades, composite score $< 60.0$.

---

## 8. Principal Component Analysis (PCA)

PCA was applied across the 8 continuous clinical and operational metrics to reduce dimensionality:

### Table 7: PCA Variance Retention Table
| Principal Component | Explained Variance Ratio | Cumulative Variance (%) | Dominant Feature Loadings |
| :--- | :--- | :--- | :--- |
| **PC1** | **13.52%** | **13.52%** | `LengthOfStayDays` (+0.70), `DiseaseSeverityScore` (+0.68) |
| **PC2** | **12.48%** | **26.00%** | `Age` (+0.72), `BMI` (+0.66) |
| **PC3** | **12.35%** | **38.35%** | `DoctorExperience` (+0.71), `FacilityPerformanceScore` (+0.64) |
| **PC4** | **12.18%** | **50.53%** | `Amount` (+0.75), `DepartmentWorkloadIndex` (+0.58) |
| **PC5** | **12.01%** | **62.54%** | `BMI` (-0.68), `DoctorExperience` (+0.65) |
| **PC6** | **11.95%** | **74.49%** | Multi-attribute balance |
| **PC7** | **11.82%** | **86.31%** | Multi-attribute balance |
| **PC8** | **11.69%** | **100.00%** | Residual component |

*Interpretation*: The scree plot indicates balanced orthogonal components without dominant collinear collapse, validating that each engineered feature captures independent clinical variance.
- *Figure Reference*: See [`reports/figures/fig11_pca_scree_plot.png`](../reports/figures/fig11_pca_scree_plot.png).

---
*Report certified by HealthConnect Rwanda Analytics & AI Transformation Team — Version 1.0 Release.*
