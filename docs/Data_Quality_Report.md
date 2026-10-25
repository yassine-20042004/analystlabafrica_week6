# HealthConnect Rwanda Healthcare Analytics & AI Transformation
## Enterprise Data Quality, Validation & Governance Report
**AnalystLab Africa Experience Lab Internship Programme — Official Week 6 Deliverable**

---

### 📋 Document Control
| Field | Value |
| :--- | :--- |
| **Programme** | AnalystLab Africa Experience Lab |
| **Project Title** | Enterprise Healthcare Analytics, Artificial Intelligence and Digital Transformation System |
| **Track** | **Track 2 — Data Science Track** |
| **Client** | HealthConnect Rwanda (Ministry of Health & Partner Network) |
| **Document** | Comprehensive Data Quality & Validation Audit Report |
| **Version** | 1.0 (Production Release) |
| **Audited Datasets** | 27 Interconnected Enterprise Tables & Sheets |
| **Lead Auditor** | Senior Healthcare Data Scientist |

---

## 1. Executive Summary

Healthcare operations and clinical decision support depend fundamentally on high-integrity, referentially sound clinical and financial data. HealthConnect Rwanda manages an interconnected healthcare analytics network spanning 20 medical facilities across Rwanda's 5 provinces.

This **Data Quality Report** documents the systematic audit, cleaning, normalization, and validation of HealthConnect Rwanda's **27 enterprise datasets**, comprising patient demographics, clinical journey transactions (appointments, diagnoses, lab tests, prescriptions, admissions, referrals), operational staffing, facilities, room and bed inventory, billing, payment processing, insurance claims, and patient feedback surveys.

### Key Audit Highlights:
- **Total Enterprise Records Audited**: Over **250,000 transaction records** across 27 tables.
- **Foreign Key Referential Integrity**: **100.0% integrity** across all relational joins linking Appointments to Patients (`PAT...`), Doctors (`DO...`), Facilities (`HF...`), and Clinical Departments (`DEP...`).
- **Primary Key Uniqueness**: Zero duplicate primary keys detected in Patients (`PatientID`), Appointments (`AppointmentID`), or Invoicing (`BillingID`).
- **Data Hygiene Fixes**: Imputed missing `ChronicCondition` attributes (25.35% unrecorded, safely classified as `"None"`), standardized 5 distinct billing payment channels, verified BMI calculations against physical height/weight metrics, and normalized datetime fields to ISO 8601 (`YYYY-MM-DD`).
- **Intentional Synthetic Anomalies Identified**: Detected **19,990 repeated phone numbers** in the patient registration database (synthetic placeholder artifact flagged for data governance remediation).

---

## 2. Enterprise Relational Database Inventory

HealthConnect Rwanda's database architecture is organized into four core functional domains:

```
HEALTHCONNECT RWANDA RELATIONAL TOPOLOGY
========================================================================================
[1. GEOGRAPHY & MASTER]       [2. FACILITIES & OPERATIONS]    [3. CLINICAL TRANSACTIONS]
   HCCountries (1)               Health Facilities (20)          Appointments (5,000 cohort)
   HC_Provinces (5)              HC_Departments (200)            Diagnoses (60,000 full / 5k)
   HC_Districts (30)             HC_Medical_Specialties (200)    Laboratory Tests (5,000)
   HC_Sectors (120)              HC_Services (400)               Prescriptions (5,000)
   HC_Villages (480)             HC_Rooms (400)                  Admissions (5,000 full / 586)
   HC_Ownership_Types (4)        HC_Beds (2,000)                 Referrals (4,708 full / 415)
                                 Staff Master (1,250):           
                                   - Doctors (350)            [4. FINANCIAL & FEEDBACK]
                                   - Nurses (700)                HC_Billing (60,000)
                                   - Lab Scientists (40)         HC_Payments (60,000)
                                   - Pharmacists (50)            Insurance Claims (42,036)
                                   - Radiographers (30)          HC_Revenue_Summary (12)
                                   - Admin Staff (80)            HC_Patient_Feedback (21,064)
========================================================================================
```

### Table 1: Comprehensive Dataset Inventory & Audit Metrics
| Domain | Dataset / Table Name | Source Format | Records | Attribute Count | Primary Key | Foreign Keys | Missing Rate |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Geographic** | `HCCountries` | CSV | 1 | 6 | `CountryID` | None | 0.0% |
| **Geographic** | `HC_Provinces` | CSV | 5 | 3 | `ProvinceID` | `CountryID` | 0.0% |
| **Geographic** | `HC_Districts` | CSV | 30 | 3 | `DistrictID` | `ProvinceID` | 0.0% |
| **Geographic** | `HC_Sectors` | CSV | 120 | 3 | `SectorID` | `DistrictID` | 0.0% |
| **Geographic** | `HC_Villages` | CSV | 480 | 3 | `VillageID` | `SectorID` | 0.0% |
| **Master** | `HC_Ownership_Types` | CSV | 4 | 2 | `OwnershipID`| None | 0.0% |
| **Facility** | `HC_Departments` | CSV / XLSX | 200 | 3 | `DepartmentID`| `FacilityID` | 0.0% |
| **Facility** | `HC_Medical_Specialties` | CSV / XLSX | 200 | 3 | `SpecialtyID` | `DepartmentID` | 0.0% |
| **Facility** | `HC_Services` | CSV / XLSX | 400 | 3 | `ServiceID` | `DepartmentID` | 0.0% |
| **Facility** | `HC_Medical_Equipment` | CSV / XLSX | 200 | 4 | `EquipmentID` | `DepartmentID`, `FacilityID` | 0.0% |
| **Facility** | `HC_Rooms` | CSV / XLSX | 400 | 4 | `RoomID` | `DepartmentID`, `FacilityID` | 0.0% |
| **Facility** | `HC_Beds` | CSV / XLSX | 2,000 | 3 | `BedID` | `RoomID` | 0.0% |
| **Staff** | `HC_Doctor` | CSV | 350 | 10 | `StaffID` | `FacilityID`, `DepartmentID` | 0.0% |
| **Staff** | `HC_Nurse` | CSV | 700 | 10 | `StaffID` | `FacilityID`, `DepartmentID` | 0.0% |
| **Staff** | `HC_Administrative_Staff` | CSV | 80 | 10 | `StaffID` | `FacilityID`, `DepartmentID` | 0.0% |
| **Staff** | `HC_Radiographer` | CSV | 30 | 10 | `StaffID` | `FacilityID`, `DepartmentID` | 0.0% |
| **Staff** | `Laboratory_Scientist` | CSV | 40 | 10 | `StaffID` | `FacilityID`, `DepartmentID` | 0.0% |
| **Staff** | `Pharmacist` | CSV | 50 | 10 | `StaffID` | `FacilityID`, `DepartmentID` | 0.0% |
| **Demographics**| `HC_Patients` | CSV | 20,000 | 19 | `PatientID` | `VillageID`, `InsuranceID` | 25.35% (Chronic) |
| **Clinical** | `Appointments` | XLSX | 5,000 | 7 | `AppointmentID`| `PatientID`, `DoctorID`, `FacilityID` | 0.0% |
| **Clinical** | `Diagnoses` | XLSX / CSV | 60,000 | 4 | `DiagnosisID` | `AppointmentID` | 0.0% |
| **Clinical** | `Laboratory_Tests` | XLSX | 5,000 | 4 | `LabID` | `AppointmentID` | 0.0% |
| **Clinical** | `Prescriptions` | XLSX | 5,000 | 4 | `PrescriptionID`| `AppointmentID` | 0.0% |
| **Clinical** | `Admissions` | XLSX | 5,000 | 3 | `AdmissionID` | `AppointmentID` | 0.0% |
| **Clinical** | `Referrals` | XLSX | 4,708 | 3 | `ReferralID` | `AppointmentID`, `ReferredFacilityID` | 0.0% |
| **Financial** | `HC_Billing` | CSV | 60,000 | 4 | `BillingID` | `AppointmentID` | 0.0% |
| **Financial** | `HC_Payments` | CSV | 60,000 | 4 | `PaymentID` | `BillingID` | 0.0% |
| **Financial** | `Insurance_Claims` | CSV | 42,036 | 5 | `ClaimID` | `BillingID` | 0.0% |
| **Financial** | `HC_Revenue_Summary` | CSV | 12 | 3 | Month | None | 0.0% |
| **Experience** | `HC_Patient_Feedback` | CSV | 21,064 | 4 | `FeedbackID` | `AppointmentID` | 0.0% |

---

## 3. Data Cleaning & Preprocessing (Task 2 Audit)

### 3.1 Missing Value Treatment
- **Chronic Condition Incompleteness**: In `HC_Patients.csv`, 5,071 records (25.35%) contained null values in `ChronicCondition`. In clinical documentation, a blank chronic illness field indicates that the patient has no documented history of long-term morbidities. Rather than dropping records or imputing with the mode, these entries were imputed with `"None"`.
- **Patient Survey Coverage**: In `HC_Patient_Feedback.csv`, 21,064 patients completed satisfaction evaluations out of 60,000 total hospital encounters (35.12% response rate in the clinical cohort). Non-responses were preserved as `'Unrated / No Feedback'` to prevent response bias in satisfaction modeling.
- **Insurance Claims Null Values**: In `Insurance_Claims.csv`, exactly 17,964 billing records did not have associated insurance claims. Cross-validation with payment methods confirmed that these patients paid via out-of-pocket channels (Cash, Mobile Money, Debit/Credit Card). These were mapped to `"Uninsured / Out-of-Pocket"`.

### 3.2 Data Type Conversions & Standardizations
- **Datetime Normalization**: All temporal columns (`DateOfBirth`, appointment `Date`, billing invoice cycles) were cast to standard pandas `datetime64[ns]` formats. From these, operational variables (`Month`, `Quarter`, `DayOfWeek`, `SeasonalVisitIndicator`) were derived.
- **Clinical Categorical Standardization**:
  - `Severity` mapped to ordinal scores: `Mild` $\rightarrow 1$, `Moderate` $\rightarrow 2$, `Severe` $\rightarrow 3$.
  - `Gender`: Trimmed whitespace and standardized title casing (`Male`: 10,090, `Female`: 9,910).
  - `BloodGroup`: Cleaned string encodings (`A+`, `A-`, `B+`, `B-`, `AB+`, `AB-`, `O+`, `O-`).
- **Physical Metrics Validation**: Verified body mass index using the formula $\text{BMI} = \frac{\text{Weight (kg)}}{(\text{Height (m)})^2}$. Recomputed missing or rounded values to 1 decimal place.

---

## 4. Referential Integrity & Validation Findings (Task 3 Audit)

### Table 2: Foreign Key Integrity Audit Results
| Relationship Verified | Parent Key | Child Key | Expected Match | Actual Validated Match | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `Appointments` $\rightarrow$ `Patients` | `Patients.PatientID` | `Appointments.PatientID` | 100.0% | **100.00%** (5,000 / 5,000) | **PASS** |
| `Appointments` $\rightarrow$ `Doctors` | `Doctor.StaffID` | `Appointments.DoctorID` | 100.0% | **100.00%** (5,000 / 5,000) | **PASS** |
| `Appointments` $\rightarrow$ `Facilities` | `Facilities.FacilityID` | `Appointments.FacilityID` | 100.0% | **100.00%** (5,000 / 5,000) | **PASS** |
| `Appointments` $\rightarrow$ `Departments`| `Departments.DepartmentID`| `Appointments.DepartmentID`| 100.0% | **100.00%** (5,000 / 5,000) | **PASS** |
| `Cohort Appointments` $\rightarrow$ `Billing` | `Appointments.AppointmentID`| `Billing.AppointmentID` | 100.0% | **100.00%** (5,000 / 5,000) | **PASS** |
| `Cohort Appointments` $\rightarrow$ `Diagnoses` | `Appointments.AppointmentID`| `Diagnoses.AppointmentID` | 100.0% | **100.00%** (5,000 / 5,000) | **PASS** |
| `Billing` $\rightarrow$ `Payments` | `Billing.BillingID` | `Payments.BillingID` | 100.0% | **100.00%** (60,000 / 60,000) | **PASS** |
| `Billing` $\rightarrow$ `Claims` | `Billing.BillingID` | `Insurance_Claims.BillingID`| ~70.0% | **70.06%** (42,036 / 60,000) | **PASS** |

### 4.1 Value Constraint & Anomaly Verification
1. **Impossible Ages Check**: 
   - Rule: $0 \le \text{Age} \le 120$.
   - Result: Min Age = 0 years (pediatric neonatal), Max Age = 90 years. **Zero impossible age records detected.**
2. **Invalid Billing Amounts Check**:
   - Rule: $\text{Amount} > 0$.
   - Result: Min Billing = 10,002 RWF, Max Billing = 299,998 RWF. Mean = 155,156.70 RWF. **Zero negative or zero billing records detected.**
3. **Primary Key Collision Check**:
   - `PatientID`: Exactly 20,000 unique records for 20,000 rows. **Zero duplicates.**
   - `AppointmentID`: Exactly 5,000 unique records in cohort. **Zero duplicates.**
   - `BillingID`: Exactly 60,000 unique records. **Zero duplicates.**
4. **Duplicate Phone Numbers Anomaly**:
   - Investigation revealed that only 10 unique phone numbers were repeated across 20,000 patients (19,990 repeated entries).
   - **Root Cause Analysis**: Identified as a synthetic placeholder artifact in the patient registration database generator where default prefix strings were repeated.
   - **Remediation Recommendation**: Implement an input validation mask on the Electronic Medical Records (EMR) intake portal requiring a unique, verified 10-digit Rwandan mobile number (`+250 78...`).

---

## 5. Data Governance & Security Safeguards

To ensure ethical, responsible, and compliant clinical data usage, HealthConnect Rwanda must adhere to:

1. **Rwandan Law on Data Protection (Law No. 058/2021)**:
   - Implement de-identification and pseudonymization of Patient Health Information (PHI) before clinical data is ingested into downstream predictive pipelines.
2. **Role-Based Access Control (RBAC)**:
   - Restrict access to raw patient identifiers (`FirstName`, `LastName`, `Phone`, `EmergencyContact`) to attending physicians and registered intake clerks. Data science pipelines operate exclusively on anonymized tokens (`PAT...`).
3. **Automated Continuous Schema Auditing**:
   - Integrate automated referential constraint verification scripts into CI/CD pipelines to prevent orphaned records during EHR syncs.

---
*Report certified by HealthConnect Rwanda Analytics & AI Transformation Team — Version 1.0 Release.*