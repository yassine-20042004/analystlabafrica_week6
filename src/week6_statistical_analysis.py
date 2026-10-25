"""
HealthConnect Rwanda Healthcare Analytics & AI Transformation Project
Track 2: Data Science Track - Statistical Analysis & Hypothesis Testing
Module: src/week6_statistical_analysis.py
"""

import os
import sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import json
import pandas as pd
import numpy as np
from scipy import stats

def run_statistical_analysis(cohort_path="data/processed/feature_engineered_cohort.csv", output_dir="data/processed"):
    print(">> [1/3] Running descriptive statistics on numerical variables...")
    df = pd.read_csv(cohort_path)
    
    num_cols = [
        "Age", "BMI", "DoctorExperience", "LengthOfStayDays",
        "Amount", "TotalPaid", "OutstandingAmount", "Rating",
        "DiseaseSeverityScore", "DepartmentWorkloadIndex", "FacilityPerformanceScore"
    ]
    
    desc_rows = []
    for col in num_cols:
        series = df[col].dropna()
        mode_val = series.mode().iloc[0] if not series.empty else np.nan
        desc_rows.append({
            "Variable": col,
            "Count": int(series.count()),
            "Mean": float(round(series.mean(), 2)),
            "Median": float(round(series.median(), 2)),
            "Mode": float(round(mode_val, 2)),
            "StdDev": float(round(series.std(), 2)),
            "Variance": float(round(series.var(), 2)),
            "Q1_25%": float(round(series.quantile(0.25), 2)),
            "Q2_50%": float(round(series.quantile(0.50), 2)),
            "Q3_75%": float(round(series.quantile(0.75), 2)),
            "IQR": float(round(series.quantile(0.75) - series.quantile(0.25), 2)),
            "P10%": float(round(series.quantile(0.10), 2)),
            "P90%": float(round(series.quantile(0.90), 2)),
            "P95%": float(round(series.quantile(0.95), 2)),
            "Min": float(round(series.min(), 2)),
            "Max": float(round(series.max(), 2)),
            "Skewness": float(round(series.skew(), 3)),
            "Kurtosis": float(round(series.kurtosis(), 3))
        })
    df_desc = pd.DataFrame(desc_rows)
    desc_csv = os.path.join(output_dir, "descriptive_statistics.csv")
    df_desc.to_csv(desc_csv, index=False)
    print(f"   -> Descriptive statistics saved to {desc_csv}")

    print(">> [2/3] Computing correlation matrix & pairwise relationship coefficients...")
    corr_cols = [
        "Age", "BMI", "DoctorExperience", "DiseaseSeverityScore",
        "LengthOfStayDays", "IsAdmitted", "Amount", "IsInsured",
        "Rating", "DepartmentWorkloadIndex", "FacilityPerformanceScore"
    ]
    corr_matrix = df[corr_cols].corr(method="pearson").round(4)
    corr_csv = os.path.join(output_dir, "correlation_matrix.csv")
    corr_matrix.to_csv(corr_csv)
    print(f"   -> Correlation matrix saved to {corr_csv}")

    # Specific pairwise correlations requested:
    # 1. Age and Hospital Admissions
    corr_age_adm, p_age_adm = stats.pointbiserialr(df["IsAdmitted"], df["Age"])
    # 2. Age and Billing Amount
    corr_age_bill, p_age_bill = stats.pearsonr(df["Age"], df["Amount"])
    # 3. Disease Severity and Length of Stay (for admitted)
    admitted_df = df[df["IsAdmitted"] == 1]
    corr_sev_los, p_sev_los = stats.spearmanr(admitted_df["DiseaseSeverityScore"], admitted_df["LengthOfStayDays"])
    # 4. Department Workload and Satisfaction
    rated_df = df.dropna(subset=["Rating"])
    corr_dept_sat, p_dept_sat = stats.pearsonr(rated_df["DepartmentWorkloadIndex"], rated_df["Rating"])
    # 5. Facility Revenue and Patient Volume
    fac_summary = df.groupby("FacilityID").agg(Volume=("AppointmentID", "count"), Revenue=("Amount", "sum"))
    corr_rev_vol, p_rev_vol = stats.pearsonr(fac_summary["Volume"], fac_summary["Revenue"])

    pairwise_results = {
        "Age_vs_Admission": {"Correlation": round(corr_age_adm, 4), "P_Value": round(p_age_adm, 5), "Type": "Point-Biserial"},
        "Age_vs_Billing": {"Correlation": round(corr_age_bill, 4), "P_Value": round(p_age_bill, 5), "Type": "Pearson"},
        "Severity_vs_LengthOfStay": {"Correlation": round(corr_sev_los, 4), "P_Value": round(p_sev_los, 5), "Type": "Spearman (Admitted)"},
        "DepartmentWorkload_vs_Satisfaction": {"Correlation": round(corr_dept_sat, 4), "P_Value": round(p_dept_sat, 5), "Type": "Pearson"},
        "FacilityRevenue_vs_PatientVolume": {"Correlation": round(corr_rev_vol, 4), "P_Value": round(p_rev_vol, 5), "Type": "Pearson"}
    }

    print(">> [3/3] Executing 3 inferential hypothesis tests...")
    hypothesis_tests = {}

    # -------------------------------------------------------------
    # TEST 1: Two-Sample Welch's T-Test (Insured vs Uninsured Billing)
    # -------------------------------------------------------------
    insured_billing = df[df["IsInsured"] == 1]["Amount"]
    uninsured_billing = df[df["IsInsured"] == 0]["Amount"]
    
    t_stat, t_pval = stats.ttest_ind(insured_billing, uninsured_billing, equal_var=False)
    u_stat, u_pval = stats.mannwhitneyu(insured_billing, uninsured_billing)
    
    insured_mean = float(insured_billing.mean())
    uninsured_mean = float(uninsured_billing.mean())
    insured_std = float(insured_billing.std())
    uninsured_std = float(uninsured_billing.std())
    cohen_d = (insured_mean - uninsured_mean) / np.sqrt(((insured_std ** 2) + (uninsured_std ** 2)) / 2)

    hypothesis_tests["Hypothesis_Test_1"] = {
        "Name": "Two-Sample Welch's T-Test: Insured vs Uninsured Patient Billing Amounts",
        "Business_Question": "Do insured patients incur different healthcare billing amounts compared to uninsured patients?",
        "H0": "Mean billing amount for insured patients is equal to uninsured patients (mu_insured = mu_uninsured)",
        "H1": "Mean billing amount for insured patients differs significantly from uninsured patients (mu_insured != mu_uninsured)",
        "Sample_Size_Insured": int(len(insured_billing)),
        "Sample_Size_Uninsured": int(len(uninsured_billing)),
        "Mean_Insured_RWF": round(insured_mean, 2),
        "Mean_Uninsured_RWF": round(uninsured_mean, 2),
        "Difference_RWF": round(insured_mean - uninsured_mean, 2),
        "Test_Statistic_t": round(float(t_stat), 4),
        "P_Value": float(t_pval),
        "Degrees_of_Freedom": round(float(stats.ttest_ind(insured_billing, uninsured_billing, equal_var=False).df), 2) if hasattr(stats.ttest_ind(insured_billing, uninsured_billing, equal_var=False), 'df') else "Welch Approx",
        "Mann_Whitney_U_Stat": float(u_stat),
        "Mann_Whitney_P_Value": float(u_pval),
        "Effect_Size_Cohen_d": round(float(cohen_d), 4),
        "Alpha": 0.05,
        "Reject_H0": bool(t_pval < 0.05),
        "Interpretation": "Statistically significant difference detected" if t_pval < 0.05 else "Fail to reject H0: No statistically significant difference in billing amounts between insured and uninsured cohorts at alpha = 0.05."
    }

    # -------------------------------------------------------------
    # TEST 2: One-Way ANOVA: Patient Satisfaction across 20 Facilities
    # -------------------------------------------------------------
    fac_groups = [group["Rating"].dropna().values for _, group in rated_df.groupby("FacilityID")]
    f_stat, anova_pval = stats.f_oneway(*fac_groups)
    kw_stat, kw_pval = stats.kruskal(*fac_groups)

    hypothesis_tests["Hypothesis_Test_2"] = {
        "Name": "One-Way ANOVA: Patient Satisfaction Across 20 Health Facilities",
        "Business_Question": "Does patient satisfaction rating differ significantly across the 20 healthcare facilities in Rwanda?",
        "H0": "Mean patient satisfaction is identical across all 20 healthcare facilities (mu_1 = mu_2 = ... = mu_20)",
        "H1": "At least one healthcare facility has a statistically significantly different mean patient satisfaction rating",
        "Total_Rated_Appointments": int(len(rated_df)),
        "Number_of_Facilities": len(fac_groups),
        "F_Statistic": round(float(f_stat), 4),
        "P_Value": float(anova_pval),
        "ANOVA_P_Value": float(anova_pval),
        "Kruskal_Wallis_H_Stat": round(float(kw_stat), 4),
        "Kruskal_Wallis_P_Value": float(kw_pval),
        "Alpha": 0.05,
        "Reject_H0": bool(anova_pval < 0.05),
        "Interpretation": "Statistically significant facility-level variation in patient satisfaction detected (p < 0.05)" if anova_pval < 0.05 else "Fail to reject H0: Patient satisfaction ratings are statistically homogeneous across all 20 facilities (p >= 0.05)."
    }

    # -------------------------------------------------------------
    # TEST 3: Chi-Square Test of Independence: Admission Rates by Age Group
    # -------------------------------------------------------------
    contingency_table = pd.crosstab(df["PatientAgeGroup"], df["IsAdmitted"])
    chi2_stat, chi2_pval, dof, expected = stats.chi2_contingency(contingency_table)
    cramers_v = np.sqrt(chi2_stat / (len(df) * (min(contingency_table.shape) - 1)))

    hypothesis_tests["Hypothesis_Test_3"] = {
        "Name": "Chi-Square Test of Independence: Hospital Admission Rates Across Patient Age Groups",
        "Business_Question": "Is the likelihood of requiring hospital admission significantly dependent on patient age group?",
        "H0": "Hospital admission is independent of patient age group (P(Admitted | Age Group) = P(Admitted))",
        "H1": "Hospital admission is significantly dependent on patient age group",
        "Contingency_Table": contingency_table.to_dict(),
        "Chi2_Statistic": round(float(chi2_stat), 4),
        "Degrees_of_Freedom": int(dof),
        "P_Value": float(chi2_pval),
        "Cramers_V": round(float(cramers_v), 4),
        "Alpha": 0.05,
        "Reject_H0": bool(chi2_pval < 0.05),
        "Interpretation": "Statistically significant relationship: Hospital admissions are significantly dependent on patient age group (p < 0.05)." if chi2_pval < 0.05 else "Fail to reject H0: Admission rates do not exhibit statistically significant dependency on age group."
    }

    # Save complete statistical summary to JSON
    full_stats_report = {
        "Pairwise_Correlations": pairwise_results,
        "Hypothesis_Tests": hypothesis_tests
    }
    json_path = os.path.join(output_dir, "statistical_analysis_results.json")
    with open(json_path, "w") as f:
        json.dump(full_stats_report, f, indent=4)
    print(f"   -> Statistical test results successfully saved to {json_path}")
    
    return df_desc, corr_matrix, full_stats_report

if __name__ == "__main__":
    desc, corr, results = run_statistical_analysis()
    print("\n=== HYPOTHESIS TEST SUMMARY ===")
    for k, v in results["Hypothesis_Tests"].items():
        print(f"\n[{k}] {v['Name']}:")
        print(f" * P-Value: {v['P_Value']}")
        print(f" * Reject H0: {v['Reject_H0']}")
        print(f" * Conclusion: {v['Interpretation']}")
