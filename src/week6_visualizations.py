"""
HealthConnect Rwanda Healthcare Analytics & AI Transformation Project
Track 2: Data Science Track - Publication-Grade Data Visualizations Generator
Module: src/week6_visualizations.py
"""

import os
import sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

# Set aesthetic style
plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
plt.rcParams["font.sans-serif"] = "DejaVu Sans"
plt.rcParams["axes.edgecolor"] = "#CBD5E1"
plt.rcParams["axes.linewidth"] = 0.8
plt.rcParams["grid.color"] = "#E2E8F0"
plt.rcParams["grid.linestyle"] = "--"
plt.rcParams["grid.alpha"] = 0.7

COLORS = {
    "primary": "#0284C7",    # Medical Blue
    "secondary": "#0D9488",  # Teal
    "accent": "#F59E0B",     # Amber
    "danger": "#EF4444",     # Coral / Red
    "dark": "#1E293B",       # Slate
    "light": "#F8FAFC",      # Off-white
    "success": "#10B981"     # Emerald Green
}

PALETTE = ["#0284C7", "#0D9488", "#10B981", "#F59E0B", "#EF4444", "#8B5CF6", "#EC4899", "#64748B"]

def generate_all_figures(output_dir="reports/figures"):
    os.makedirs(output_dir, exist_ok=True)
    df = pd.read_csv("data/processed/feature_engineered_cohort.csv")
    pts = pd.read_csv("data/processed/cleaned_patients.csv")
    facs = pd.read_csv("data/processed/cleaned_facilities.csv")
    rev_sum = pd.read_csv("data/raw/HC_Revenue_Summary.csv")
    forecast_visits = pd.read_csv("data/processed/forecast_patient_volume_12m.csv")
    forecast_rev = pd.read_csv("data/processed/forecast_hospital_revenue_12m.csv")
    
    print(f">> Generating publication-grade figures in {output_dir}...")

    # -------------------------------------------------------------
    # FIGURE 1: Patient Age & Gender Demographic Pyramid / Histogram
    # -------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(10, 5), dpi=300)
    sns.histplot(
        data=pts, x="Age", hue="Gender", multiple="stack",
        bins=30, palette=[COLORS["primary"], "#EC4899"], alpha=0.85, ax=ax
    )
    ax.axvline(pts["Age"].mean(), color=COLORS["dark"], linestyle="--", linewidth=1.5, label=f"Mean Age: {pts['Age'].mean():.1f} yrs")
    ax.set_title("HealthConnect Rwanda: Patient Age & Gender Distribution (N=20,000)", fontsize=13, weight="bold", pad=12)
    ax.set_xlabel("Patient Age (Years)", fontsize=11, labelpad=8)
    ax.set_ylabel("Patient Count", fontsize=11, labelpad=8)
    ax.legend(title="Demographics", frameon=True)
    plt.tight_layout()
    fig_path = os.path.join(output_dir, "fig01_patient_age_gender_distribution.png")
    plt.savefig(fig_path)
    plt.close()
    print("   -> Saved Fig 1: Patient Age & Gender Distribution")

    # -------------------------------------------------------------
    # FIGURE 2: Chronic Disease Prevalence & Severity Distribution
    # -------------------------------------------------------------
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5), dpi=300)
    chronic_counts = pts["ChronicCondition"].value_counts()
    ax1.pie(
        chronic_counts.values, labels=chronic_counts.index, autopct="%1.1f%%",
        startangle=140, colors=[COLORS["primary"], COLORS["secondary"], COLORS["accent"], "#94A3B8"],
        wedgeprops=dict(width=0.4, edgecolor="white", linewidth=2)
    )
    ax1.set_title("Chronic Disease Prevalence\n(Population Master)", fontsize=12, weight="bold")
    
    sns.countplot(
        data=df, x="Diagnosis", hue="Severity",
        palette=[COLORS["success"], COLORS["accent"], COLORS["danger"]], ax=ax2
    )
    ax2.set_title("Clinical Diagnosis Volume by Severity\n(Transaction Cohort)", fontsize=12, weight="bold")
    ax2.set_xlabel("Clinical Diagnosis", fontsize=10)
    ax2.set_ylabel("Appointment Count", fontsize=10)
    ax2.tick_params(axis="x", rotation=25)
    ax2.legend(title="Severity", frameon=True)
    plt.tight_layout()
    fig_path = os.path.join(output_dir, "fig02_chronic_disease_and_diagnoses_severity.png")
    plt.savefig(fig_path)
    plt.close()
    print("   -> Saved Fig 2: Chronic Disease & Clinical Severity")

    # -------------------------------------------------------------
    # FIGURE 3: Correlation Matrix Heatmap
    # -------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(10, 8), dpi=300)
    corr_df = pd.read_csv("data/processed/correlation_matrix.csv", index_col=0)
    sns.heatmap(
        corr_df, annot=True, fmt=".2f", cmap="Blues",
        cbar_kws={"label": "Pearson Correlation Coefficient"},
        linewidths=0.5, linecolor="white", ax=ax
    )
    ax.set_title("HealthConnect Rwanda: Healthcare Metrics Correlation Heatmap", fontsize=13, weight="bold", pad=14)
    plt.xticks(rotation=45, ha="right")
    plt.yticks(rotation=0)
    plt.tight_layout()
    fig_path = os.path.join(output_dir, "fig03_correlation_matrix_heatmap.png")
    plt.savefig(fig_path)
    plt.close()
    print("   -> Saved Fig 3: Correlation Heatmap")

    # -------------------------------------------------------------
    # FIGURE 4: Billing Amount Box Plot by Insurance Provider
    # -------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(10, 5), dpi=300)
    sns.boxplot(
        data=df, x="InsuranceCoverageCategory", y="Amount",
        palette=PALETTE[:5], ax=ax, flierprops=dict(marker="o", markersize=3, alpha=0.3)
    )
    ax.set_title("Healthcare Billing Amounts by Insurance Coverage Category", fontsize=13, weight="bold", pad=12)
    ax.set_xlabel("Insurance Provider / Coverage Status", fontsize=11, labelpad=8)
    ax.set_ylabel("Billing Amount (RWF)", fontsize=11, labelpad=8)
    ax.yaxis.set_major_formatter("{x:,.0f} RWF")
    plt.tight_layout()
    fig_path = os.path.join(output_dir, "fig04_billing_distribution_by_insurance.png")
    plt.savefig(fig_path)
    plt.close()
    print("   -> Saved Fig 4: Billing Boxplot by Insurance")

    # -------------------------------------------------------------
    # FIGURE 5: Violin Plot: Patient Satisfaction by Healthcare Facility Type
    # -------------------------------------------------------------
    rated_df = df.dropna(subset=["Rating"])
    fig, ax = plt.subplots(figsize=(10, 5), dpi=300)
    sns.violinplot(
        data=rated_df, x="FacilityType", y="Rating",
        palette=[COLORS["primary"], COLORS["secondary"], COLORS["accent"], "#8B5CF6"],
        inner="quartile", ax=ax
    )
    ax.set_title("Patient Satisfaction Rating Distribution Across Facility Tiers (N=1,756)", fontsize=13, weight="bold", pad=12)
    ax.set_xlabel("Healthcare Facility Tier", fontsize=11, labelpad=8)
    ax.set_ylabel("Satisfaction Rating (1 = Poor, 5 = Excellent)", fontsize=11, labelpad=8)
    ax.set_ylim(0.5, 5.5)
    plt.tight_layout()
    fig_path = os.path.join(output_dir, "fig05_satisfaction_violin_by_facility_type.png")
    plt.savefig(fig_path)
    plt.close()
    print("   -> Saved Fig 5: Satisfaction Violin Plot")

    # -------------------------------------------------------------
    # FIGURE 6: Time-Series Line Chart: 2026 Historical vs 2027 Forecasted Visits
    # -------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(12, 5), dpi=300)
    months_hist = rev_sum["Month"].tolist()
    visits_hist = rev_sum["Appointments"].tolist()
    months_fc = forecast_visits["Month"].tolist()
    visits_fc = forecast_visits["ForecastedVisits"].tolist()
    lower_fc = forecast_visits["LowerBound_95%"].tolist()
    upper_fc = forecast_visits["UpperBound_95%"].tolist()
    
    all_months = months_hist + months_fc
    x_hist = range(len(months_hist))
    x_fc = range(len(months_hist) - 1, len(months_hist) + len(months_fc))
    
    ax.plot(x_hist, visits_hist, marker="o", color=COLORS["primary"], linewidth=2.5, label="Historical Monthly Visits (2026)")
    # Connect last historical to first forecast
    fc_full_x = [len(months_hist) - 1] + list(range(len(months_hist), len(all_months)))
    fc_full_y = [visits_hist[-1]] + visits_fc
    ax.plot(fc_full_x, fc_full_y, marker="s", linestyle="--", color=COLORS["secondary"], linewidth=2.5, label="Holt-Winters Projected Visits (2027)")
    ax.fill_between(
        range(len(months_hist), len(all_months)), lower_fc, upper_fc,
        color=COLORS["secondary"], alpha=0.2, label="95% Confidence Interval"
    )
    
    ax.set_xticks(range(len(all_months)))
    ax.set_xticklabels(all_months, rotation=45, ha="right", fontsize=9)
    ax.set_title("HealthConnect Rwanda: 24-Month Patient Visit Trajectory & 2027 Forecast", fontsize=13, weight="bold", pad=12)
    ax.set_ylabel("Monthly Patient Visits", fontsize=11, labelpad=8)
    ax.yaxis.set_major_formatter("{x:,.0f}")
    ax.legend(frameon=True, loc="upper right")
    plt.tight_layout()
    fig_path = os.path.join(output_dir, "fig06_patient_volume_forecasting_trajectory.png")
    plt.savefig(fig_path)
    plt.close()
    print("   -> Saved Fig 6: Time-Series Patient Visits Forecast")

    # -------------------------------------------------------------
    # FIGURE 7: Time-Series Line Chart: 2026 Historical vs 2027 Forecasted Revenue
    # -------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(12, 5), dpi=300)
    rev_hist = (rev_sum["Revenue"] / 1e6).tolist()
    rev_fc = (forecast_rev["ForecastedRevenue_RWF"] / 1e6).tolist()
    rev_lower = (forecast_rev["LowerBound_95%_RWF"] / 1e6).tolist()
    rev_upper = (forecast_rev["UpperBound_95%_RWF"] / 1e6).tolist()
    
    ax.plot(x_hist, rev_hist, marker="o", color=COLORS["success"], linewidth=2.5, label="Historical Revenue (2026)")
    fc_full_rev_y = [rev_hist[-1]] + rev_fc
    ax.plot(fc_full_x, fc_full_rev_y, marker="D", linestyle="--", color=COLORS["accent"], linewidth=2.5, label="Forecasted Revenue (2027)")
    ax.fill_between(
        range(len(months_hist), len(all_months)), rev_lower, rev_upper,
        color=COLORS["accent"], alpha=0.2, label="95% Confidence Interval"
    )
    
    ax.set_xticks(range(len(all_months)))
    ax.set_xticklabels(all_months, rotation=45, ha="right", fontsize=9)
    ax.set_title("HealthConnect Rwanda: 24-Month Revenue Trajectory & 2027 Projections", fontsize=13, weight="bold", pad=12)
    ax.set_ylabel("Monthly Revenue (Million RWF)", fontsize=11, labelpad=8)
    ax.yaxis.set_major_formatter("{x:,.0f}M RWF")
    ax.legend(frameon=True, loc="upper left")
    plt.tight_layout()
    fig_path = os.path.join(output_dir, "fig07_hospital_revenue_forecasting_trajectory.png")
    plt.savefig(fig_path)
    plt.close()
    print("   -> Saved Fig 7: Time-Series Revenue Forecast")

    # -------------------------------------------------------------
    # FIGURE 8: Hospital Admission Likelihood & Feature Importances
    # -------------------------------------------------------------
    rf_imp = pd.read_csv("data/processed/admission_feature_importances.csv").head(10)
    fig, ax = plt.subplots(figsize=(10, 5), dpi=300)
    sns.barplot(
        data=rf_imp, x="Importance", y="Feature",
        palette="crest", ax=ax
    )
    ax.set_title("Random Forest: Top 10 Drivers of Hospital Admission Likelihood", fontsize=13, weight="bold", pad=12)
    ax.set_xlabel("Relative Feature Importance (Gini Impurity Reduction)", fontsize=11, labelpad=8)
    ax.set_ylabel("Clinical / Operational Predictor", fontsize=11, labelpad=8)
    plt.tight_layout()
    fig_path = os.path.join(output_dir, "fig08_admission_feature_importances.png")
    plt.savefig(fig_path)
    plt.close()
    print("   -> Saved Fig 8: Admission Feature Importances")

    # -------------------------------------------------------------
    # FIGURE 9: Department Workload Demand & Staffing Distribution
    # -------------------------------------------------------------
    dept_forecast = pd.read_csv("data/processed/forecast_department_workload_2027.csv")
    fig, ax = plt.subplots(figsize=(11, 5), dpi=300)
    bar_width = 0.35
    x_idx = np.arange(len(dept_forecast))
    
    ax.bar(x_idx - bar_width/2, dept_forecast["Current_2026_Visits"], width=bar_width, label="2026 Actual Visits", color=COLORS["primary"])
    ax.bar(x_idx + bar_width/2, dept_forecast["Forecasted_2027_Visits"], width=bar_width, label="2027 Forecasted Visits", color=COLORS["secondary"])
    
    ax.set_xticks(x_idx)
    ax.set_xticklabels(dept_forecast["Department"], rotation=30, ha="right", fontsize=9)
    ax.set_title("Clinical Department Patient Demand: 2026 Actual vs 2027 Projected", fontsize=13, weight="bold", pad=12)
    ax.set_ylabel("Annual Patient Visits", fontsize=11, labelpad=8)
    ax.yaxis.set_major_formatter("{x:,.0f}")
    ax.legend(frameon=True)
    plt.tight_layout()
    fig_path = os.path.join(output_dir, "fig09_department_workload_demand_forecast.png")
    plt.savefig(fig_path)
    plt.close()
    print("   -> Saved Fig 9: Department Workload Forecast")

    # -------------------------------------------------------------
    # FIGURE 10: Patient Clusters in PCA Feature Space (Unsupervised Learning)
    # -------------------------------------------------------------
    pt_clust_df = pd.read_csv("data/processed/patient_cluster_profiles.csv")
    num_features = ["Age", "BMI", "DoctorExperience", "DiseaseSeverityScore", "Amount", "LengthOfStayDays", "HighRiskPatientIndicator"]
    X_scaled = StandardScaler().fit_transform(df[num_features])
    pca = PCA(n_components=2, random_state=42)
    coords = pca.fit_transform(X_scaled)
    df["PC1"] = coords[:, 0]
    df["PC2"] = coords[:, 1]
    
    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
    cluster_labels = {
        0: "Cluster 0: Mild / Young Outpatients",
        1: "Cluster 1: Geriatric Chronic High-Risk",
        2: "Cluster 2: Moderate Surgical Inpatients",
        3: "Cluster 3: Acute Emergency / High-Cost"
    }
    # Add cluster column if not present
    from sklearn.cluster import KMeans
    if "PatientCluster" not in df.columns:
        df["PatientCluster"] = KMeans(n_clusters=4, random_state=42).fit_predict(X_scaled)
    
    df["ClusterDescription"] = df["PatientCluster"].map(cluster_labels)
    sns.scatterplot(
        data=df, x="PC1", y="PC2", hue="ClusterDescription",
        palette=[COLORS["primary"], COLORS["danger"], COLORS["secondary"], COLORS["accent"]],
        alpha=0.6, s=25, ax=ax
    )
    ax.set_title("K-Means Patient Segmentation Mapped to Principal Components (k=4)", fontsize=13, weight="bold", pad=12)
    ax.set_xlabel(f"Principal Component 1 ({pca.explained_variance_ratio_[0]*100:.1f}% Variance)", fontsize=11)
    ax.set_ylabel(f"Principal Component 2 ({pca.explained_variance_ratio_[1]*100:.1f}% Variance)", fontsize=11)
    ax.legend(title="Patient Clusters", frameon=True, loc="upper right")
    plt.tight_layout()
    fig_path = os.path.join(output_dir, "fig10_kmeans_patient_clusters_pca.png")
    plt.savefig(fig_path)
    plt.close()
    print("   -> Saved Fig 10: K-Means Patient Clusters in PCA Space")

    # -------------------------------------------------------------
    # FIGURE 11: PCA Scree Plot & Cumulative Explained Variance
    # -------------------------------------------------------------
    pca_df = pd.read_csv("data/processed/pca_explained_variance.csv")
    fig, ax1 = plt.subplots(figsize=(9, 5), dpi=300)
    ax2 = ax1.twinx()
    
    x_pcs = range(len(pca_df))
    ax1.bar(x_pcs, pca_df["Explained_Variance_Ratio"] * 100, color=COLORS["primary"], alpha=0.75, label="Individual Variance (%)")
    ax2.plot(x_pcs, pca_df["Cumulative_Variance_Ratio"] * 100, color=COLORS["danger"], marker="o", linewidth=2, label="Cumulative Variance (%)")
    
    ax1.set_xticks(x_pcs)
    ax1.set_xticklabels(pca_df["Principal_Component"], fontsize=10)
    ax1.set_title("PCA Scree Plot: Feature Dimension Reduction & Variance Retention", fontsize=13, weight="bold", pad=12)
    ax1.set_xlabel("Principal Components", fontsize=11, labelpad=8)
    ax1.set_ylabel("Individual Variance Ratio (%)", fontsize=11, color=COLORS["primary"])
    ax2.set_ylabel("Cumulative Variance (%)", fontsize=11, color=COLORS["danger"])
    ax2.set_ylim(0, 105)
    plt.tight_layout()
    fig_path = os.path.join(output_dir, "fig11_pca_scree_plot.png")
    plt.savefig(fig_path)
    plt.close()
    print("   -> Saved Fig 11: PCA Scree Plot")

    # -------------------------------------------------------------
    # FIGURE 12: Healthcare Facility Performance Score Leaderboard
    # -------------------------------------------------------------
    fac_metrics = pd.read_csv("data/processed/facility_performance_metrics.csv")
    fac_metrics = fac_metrics.sort_values(by="FacilityPerformanceScore", ascending=True)
    fig, ax = plt.subplots(figsize=(10, 7), dpi=300)
    norm = plt.Normalize(fac_metrics["FacilityPerformanceScore"].min(), fac_metrics["FacilityPerformanceScore"].max())
    colors = plt.cm.viridis(norm(fac_metrics["FacilityPerformanceScore"]))
    
    ax.barh(fac_metrics["FacilityID"], fac_metrics["FacilityPerformanceScore"], color=colors, height=0.65)
    ax.set_title("HealthConnect Rwanda: 20 Facility Composite Performance Ranking", fontsize=13, weight="bold", pad=12)
    ax.set_xlabel("Composite Performance Score (0 - 100 Index)", fontsize=11, labelpad=8)
    ax.set_ylabel("Healthcare Facility ID", fontsize=11, labelpad=8)
    for i, v in enumerate(fac_metrics["FacilityPerformanceScore"]):
        ax.text(v + 1, i, f"{v:.1f}", va="center", fontsize=9, weight="bold", color=COLORS["dark"])
    ax.set_xlim(0, 115)
    plt.tight_layout()
    fig_path = os.path.join(output_dir, "fig12_facility_performance_leaderboard.png")
    plt.savefig(fig_path)
    plt.close()
    print("   -> Saved Fig 12: Facility Performance Leaderboard")

    # -------------------------------------------------------------
    # FIGURE 13: Geographic Patient Volume by Province & Facility Type
    # -------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(10, 5), dpi=300)
    prov_summary = df.groupby(["ProvinceName", "FacilityType"]).size().unstack(fill_value=0)
    prov_summary.plot(kind="bar", stacked=True, colormap="mako", ax=ax, edgecolor="white")
    ax.set_title("Patient Consultation Volume by Province & Facility Classification", fontsize=13, weight="bold", pad=12)
    ax.set_xlabel("Rwanda Province", fontsize=11, labelpad=8)
    ax.set_ylabel("Patient Appointment Count", fontsize=11, labelpad=8)
    plt.xticks(rotation=0)
    ax.legend(title="Facility Classification", frameon=True)
    plt.tight_layout()
    fig_path = os.path.join(output_dir, "fig13_province_patient_distribution.png")
    plt.savefig(fig_path)
    plt.close()
    print("   -> Saved Fig 13: Geographic Patient Distribution")

    # -------------------------------------------------------------
    # FIGURE 14: Hospital Admission Density by Age & Chronic Condition
    # -------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(10, 5), dpi=300)
    sns.kdeplot(
        data=df[df["IsAdmitted"] == 1], x="Age", hue="ChronicCondition",
        common_norm=False, palette=[COLORS["primary"], COLORS["danger"], COLORS["accent"], COLORS["secondary"]],
        fill=True, alpha=0.3, ax=ax
    )
    ax.set_title("Age Density of Admitted Inpatients by Chronic Condition Cohort", fontsize=13, weight="bold", pad=12)
    ax.set_xlabel("Patient Age (Years)", fontsize=11, labelpad=8)
    ax.set_ylabel("Kernel Density Estimate", fontsize=11, labelpad=8)
    ax.legend(title="Chronic Condition", frameon=True)
    plt.tight_layout()
    fig_path = os.path.join(output_dir, "fig14_admission_age_density_by_chronic.png")
    plt.savefig(fig_path)
    plt.close()
    print("   -> Saved Fig 14: Admission Age Density")

    # -------------------------------------------------------------
    # FIGURE 15: Pairwise Scatter Matrix: Department Workload vs Patient Satisfaction
    # -------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(9, 5), dpi=300)
    sns.regplot(
        data=rated_df, x="DepartmentWorkloadIndex", y="Rating",
        scatter_kws={"alpha": 0.35, "color": COLORS["primary"], "s": 30},
        line_kws={"color": COLORS["danger"], "linewidth": 2}, ax=ax
    )
    ax.set_title("Correlation Analysis: Department Workload Index vs Patient Satisfaction", fontsize=13, weight="bold", pad=12)
    ax.set_xlabel("Department Workload Index (Normalized Appointments/Staff)", fontsize=11, labelpad=8)
    ax.set_ylabel("Patient Satisfaction Rating (1 to 5)", fontsize=11, labelpad=8)
    ax.set_ylim(0.5, 5.5)
    plt.tight_layout()
    fig_path = os.path.join(output_dir, "fig15_workload_vs_satisfaction_regression.png")
    plt.savefig(fig_path)
    plt.close()
    print("   -> Saved Fig 15: Workload vs Satisfaction Regression")

    print(f"All 15 publication-grade figures successfully generated in {output_dir}/")

if __name__ == "__main__":
    generate_all_figures()
