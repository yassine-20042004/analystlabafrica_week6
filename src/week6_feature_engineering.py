"""
HealthConnect Rwanda Healthcare Analytics & AI Transformation Project
Track 2: Data Science Track - Feature Engineering & Cohort Matrix Builder
Module: src/week6_feature_engineering.py
"""

import os
import sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import pandas as pd
import numpy as np
from src.week6_data_pipeline import HealthConnectDataPipeline

def build_feature_engineered_cohort(pipeline=None, processed_dir="data/processed"):
    if pipeline is None:
        pipeline = HealthConnectDataPipeline()
        pipeline.load_all_datasets()
        pipeline.clean_datasets()

    print(">> [1/3] Merging multi-table transaction cohort...")
    
    apts = pipeline.tables["cleaned_appointments"].copy()
    pts = pipeline.tables["cleaned_patients"].copy()
    diag = pipeline.tables["cleaned_diagnoses"].copy()
    adm = pipeline.tables["cleaned_admissions"].copy()
    lab = pipeline.tables["cleaned_lab_tests"].copy()
    rx = pipeline.tables["cleaned_prescriptions"].copy()
    ref = pipeline.tables["cleaned_referrals"].copy()
    bill = pipeline.tables["cleaned_billing"].copy()
    fb = pipeline.tables["cleaned_feedback"].copy()
    docs = pipeline.tables["doctors"].copy()
    facs = pipeline.tables["cleaned_facilities"].copy()
    depts = pipeline.tables["departments"].copy()

    # Join Appointments with Patients
    pts_cols = ["PatientID", "Gender", "Age", "BMI", "ChronicCondition", "BloodGroup", "Occupation", "Education", "Status"]
    merged = apts.merge(pts[pts_cols], on="PatientID", how="left")

    # Join with Doctors
    docs_cols = ["StaffID", "YearsExperience", "Specialty"]
    merged = merged.merge(docs[docs_cols].rename(columns={"StaffID": "DoctorID", "YearsExperience": "DoctorExperience", "Specialty": "DoctorSpecialty"}), on="DoctorID", how="left")

    # Join with Departments
    depts_cols = ["DepartmentID", "DepartmentName"]
    merged = merged.merge(depts[depts_cols], on="DepartmentID", how="left")

    # Join with Facilities
    facs_cols = ["FacilityID", "FacilityName", "FacilityType", "Ownership", "ProvinceName", "DoctorCount", "NurseCount", "TotalStaff", "TotalBeds"]
    merged = merged.merge(facs[facs_cols], on="FacilityID", how="left")

    # Join with Diagnoses
    diag_cols = ["AppointmentID", "Diagnosis", "Severity"]
    merged = merged.merge(diag[diag_cols], on="AppointmentID", how="left")

    # Join with Admissions
    adm_cols = ["AppointmentID", "LengthOfStayDays"]
    merged = merged.merge(adm[adm_cols], on="AppointmentID", how="left")
    merged["IsAdmitted"] = merged["LengthOfStayDays"].notnull().astype(int)
    merged["LengthOfStayDays"] = merged["LengthOfStayDays"].fillna(0).astype(int)

    # Join with Lab Tests (first test per appointment)
    lab_agg = lab.groupby("AppointmentID").agg(
        LabTest=("Test", "first"),
        LabResult=("Result", "first")
    ).reset_index()
    merged = merged.merge(lab_agg, on="AppointmentID", how="left")
    merged["LabTest"] = merged["LabTest"].fillna("None")
    merged["LabResult"] = merged["LabResult"].fillna("None")
    merged["HasAbnormalLab"] = (merged["LabResult"] == "Abnormal").astype(int)

    # Join with Prescriptions (first medication per appointment)
    rx_agg = rx.groupby("AppointmentID").agg(
        Medication=("Medication", "first")
    ).reset_index()
    merged = merged.merge(rx_agg, on="AppointmentID", how="left")
    merged["Medication"] = merged["Medication"].fillna("None")

    # Join with Referrals
    ref_agg = ref.groupby("AppointmentID").agg(
        ReferredFacilityID=("ReferredFacilityID", "first")
    ).reset_index()
    merged = merged.merge(ref_agg, on="AppointmentID", how="left")
    merged["IsReferred"] = merged["ReferredFacilityID"].notnull().astype(int)

    # Join with Billing & Insurance
    bill_cols = ["AppointmentID", "BillingID", "Amount", "TotalPaid", "OutstandingAmount", "InsuranceProvider", "ClaimStatus", "IsInsured"]
    merged = merged.merge(bill[bill_cols], on="AppointmentID", how="left")

    # Join with Patient Feedback
    fb_cols = ["AppointmentID", "Rating", "Comment"]
    merged = merged.merge(fb[fb_cols], on="AppointmentID", how="left")

    print(f"   -> Merged cohort size: {merged.shape[0]} rows x {merged.shape[1]} columns")

    print(">> [2/3] Engineering the 10 required strategic healthcare features...")

    # 1. Patient Age Group
    def assign_age_group(age):
        if pd.isnull(age):
            return "Unknown"
        if age <= 17:
            return "Pediatric (0-17)"
        elif age <= 35:
            return "Young Adult (18-35)"
        elif age <= 55:
            return "Middle-Aged (36-55)"
        elif age <= 65:
            return "Senior (56-65)"
        else:
            return "Geriatric (>65)"

    merged["PatientAgeGroup"] = merged["Age"].apply(assign_age_group)

    # 2. Disease Severity Score (Mild = 1, Moderate = 2, Severe = 3)
    severity_map = {"Mild": 1, "Moderate": 2, "Severe": 3}
    merged["DiseaseSeverityScore"] = merged["Severity"].map(severity_map).fillna(1).astype(int)

    # 3. High-Risk Patient Indicator (Age >= 60, chronic condition, or severe diagnosis)
    merged["HighRiskPatientIndicator"] = (
        (merged["Age"] >= 60) |
        (merged["ChronicCondition"].isin(["Diabetes", "Hypertension", "Asthma"])) |
        (merged["DiseaseSeverityScore"] >= 3)
    ).astype(int)

    # 4. Length of Stay Category
    def assign_los_cat(los):
        if los == 0:
            return "Outpatient (0 Days)"
        elif los <= 3:
            return "Short Stay (1-3 Days)"
        elif los <= 7:
            return "Medium Stay (4-7 Days)"
        else:
            return "Extended Stay (>7 Days)"

    merged["LengthOfStayCategory"] = merged["LengthOfStayDays"].apply(assign_los_cat)

    # 5. Frequent Visitor Indicator
    patient_visit_counts = merged["PatientID"].value_counts()
    merged["PatientVisitCount"] = merged["PatientID"].map(patient_visit_counts)
    merged["FrequentVisitorIndicator"] = (merged["PatientVisitCount"] >= 2).astype(int)

    # 6. Insurance Coverage Category
    merged["InsuranceCoverageCategory"] = merged["InsuranceProvider"].fillna("Uninsured / Out-of-Pocket")

    # 7. Revenue Category
    def assign_revenue_cat(amt):
        if pd.isnull(amt) or amt < 50000:
            return "Low (<50k RWF)"
        elif amt < 150000:
            return "Medium (50k-150k RWF)"
        elif amt < 250000:
            return "High (150k-250k RWF)"
        else:
            return "Premium (>250k RWF)"

    merged["RevenueCategory"] = merged["Amount"].apply(assign_revenue_cat)

    # 8. Patient Satisfaction Category
    def assign_sat_cat(rating):
        if pd.isnull(rating):
            return "Unrated / No Feedback"
        elif rating <= 2:
            return "Low Satisfaction (1-2)"
        elif rating == 3:
            return "Medium Satisfaction (3)"
        else:
            return "High Satisfaction (4-5)"

    merged["PatientSatisfactionCategory"] = merged["Rating"].apply(assign_sat_cat)

    # 9. Department Workload Index (Appointments per doctor/nurse in dept)
    dept_appts = merged.groupby("DepartmentID").size().rename("DeptTotalAppointments")
    merged = merged.merge(dept_appts, on="DepartmentID", how="left")
    # Normalized workload index = appointments / mean appointments
    mean_dept_appts = dept_appts.mean()
    merged["DepartmentWorkloadIndex"] = (merged["DeptTotalAppointments"] / mean_dept_appts).round(2)

    # 10. Facility Performance Score
    # Composite score [0-100] based on volume, mean satisfaction, admission efficiency, revenue
    fac_metrics = merged.groupby("FacilityID").agg(
        FacAppointments=("AppointmentID", "count"),
        FacMeanSatisfaction=("Rating", "mean"),
        FacTotalRevenue=("Amount", "sum"),
        FacAdmissions=("IsAdmitted", "sum")
    ).reset_index()

    fac_metrics["FacMeanSatisfaction"] = fac_metrics["FacMeanSatisfaction"].fillna(fac_metrics["FacMeanSatisfaction"].median())

    # Min-max normalization
    for col in ["FacAppointments", "FacMeanSatisfaction", "FacTotalRevenue"]:
        c_min = fac_metrics[col].min()
        c_max = fac_metrics[col].max()
        fac_metrics[col + "_norm"] = (fac_metrics[col] - c_min) / (c_max - c_min) if c_max > c_min else 0.5

    # 35% Volume, 35% Satisfaction, 30% Revenue
    fac_metrics["FacilityPerformanceScore"] = (
        (fac_metrics["FacAppointments_norm"] * 35) +
        (fac_metrics["FacMeanSatisfaction_norm"] * 35) +
        (fac_metrics["FacTotalRevenue_norm"] * 30)
    ).round(1)

    merged = merged.merge(fac_metrics[["FacilityID", "FacilityPerformanceScore", "FacMeanSatisfaction"]], on="FacilityID", how="left")

    # Additional contextual temporal features
    merged["SeasonalVisitIndicator"] = merged["Month"].apply(
        lambda m: "Rainy Season (Feb-May / Oct-Dec)" if m in [2, 3, 4, 5, 10, 11, 12] else "Dry Season (Jun-Sep / Jan)"
    )

    print(">> [3/3] Exporting feature-engineered master cohort...")
    master_path = os.path.join(processed_dir, "feature_engineered_cohort.csv")
    merged.to_csv(master_path, index=False)
    
    # Save facility and department metrics summary
    fac_summary_path = os.path.join(processed_dir, "facility_performance_metrics.csv")
    fac_metrics.to_csv(fac_summary_path, index=False)

    dept_summary = merged.groupby(["DepartmentID", "DepartmentName"]).agg(
        TotalAppointments=("AppointmentID", "count"),
        TotalAdmissions=("IsAdmitted", "sum"),
        MeanRevenue=("Amount", "mean"),
        WorkloadIndex=("DepartmentWorkloadIndex", "mean")
    ).reset_index()
    dept_summary_path = os.path.join(processed_dir, "department_workload_metrics.csv")
    dept_summary.to_csv(dept_summary_path, index=False)

    print(f"   -> Successfully saved feature matrix ({merged.shape[0]} rows, {merged.shape[1]} cols) to {master_path}")
    return merged

if __name__ == "__main__":
    df_cohort = build_feature_engineered_cohort()
    print("Features summary preview:")
    features_list = [
        "PatientAgeGroup", "HighRiskPatientIndicator", "LengthOfStayCategory",
        "FrequentVisitorIndicator", "InsuranceCoverageCategory", "RevenueCategory",
        "DiseaseSeverityScore", "FacilityPerformanceScore", "PatientSatisfactionCategory",
        "DepartmentWorkloadIndex"
    ]
    for feat in features_list:
        print(f" * {feat} distribution:\n{df_cohort[feat].value_counts(dropna=False).head(4)}\n")
