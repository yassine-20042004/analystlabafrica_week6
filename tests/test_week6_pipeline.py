"""
Unit and Integration Tests for Week 6 HealthConnect Rwanda Data Science Pipeline
File: tests/test_week6_pipeline.py
"""

import os
import pytest
import pandas as pd
import numpy as np

def test_processed_files_exist():
    """Verify that all cleaned and engineered datasets have been exported."""
    required_files = [
        "cleaned_patients.csv",
        "cleaned_appointments.csv",
        "cleaned_billing.csv",
        "cleaned_staff_master.csv",
        "cleaned_facilities.csv",
        "feature_engineered_cohort.csv",
        "descriptive_statistics.csv",
        "correlation_matrix.csv",
        "forecast_patient_volume_12m.csv",
        "forecast_hospital_revenue_12m.csv",
        "patient_cluster_profiles.csv",
        "pca_explained_variance.csv"
    ]
    for fname in required_files:
        path = os.path.join("data/processed", fname)
        assert os.path.exists(path), f"Missing expected processed file: {path}"

def test_feature_engineered_cohort_integrity():
    """Verify feature engineered cohort shape, columns, and value constraints."""
    df = pd.read_csv("data/processed/feature_engineered_cohort.csv")
    assert len(df) == 5000, f"Expected 5,000 cohort appointments, got {len(df)}"
    
    expected_features = [
        "PatientAgeGroup",
        "HighRiskPatientIndicator",
        "LengthOfStayCategory",
        "FrequentVisitorIndicator",
        "InsuranceCoverageCategory",
        "RevenueCategory",
        "DiseaseSeverityScore",
        "FacilityPerformanceScore",
        "PatientSatisfactionCategory",
        "DepartmentWorkloadIndex"
    ]
    for feat in expected_features:
        assert feat in df.columns, f"Missing required feature: {feat}"
        assert df[feat].notnull().all(), f"Found unexpected null values in feature: {feat}"

def test_hypothesis_test_results():
    """Verify hypothesis testing JSON schema and outputs."""
    import json
    json_path = "data/processed/statistical_analysis_results.json"
    assert os.path.exists(json_path), f"Missing {json_path}"
    with open(json_path) as f:
        data = json.load(f)
    
    assert "Hypothesis_Tests" in data
    ht = data["Hypothesis_Tests"]
    assert "Hypothesis_Test_1" in ht
    assert "Hypothesis_Test_2" in ht
    assert "Hypothesis_Test_3" in ht
    
    # Check p-value validity
    for k, test_data in ht.items():
        assert 0.0 <= test_data["P_Value"] <= 1.0, f"P-value out of bounds for {k}"
        assert isinstance(test_data["Reject_H0"], bool), f"Reject_H0 must be bool for {k}"

def test_forecast_outputs():
    """Verify 12-month projections are non-negative and properly indexed."""
    fc_visits = pd.read_csv("data/processed/forecast_patient_volume_12m.csv")
    fc_rev = pd.read_csv("data/processed/forecast_hospital_revenue_12m.csv")
    
    assert len(fc_visits) == 12, "Patient volume forecast must have 12 months"
    assert len(fc_rev) == 12, "Revenue forecast must have 12 months"
    assert (fc_visits["ForecastedVisits"] > 0).all(), "Visits forecast must be strictly positive"
    assert (fc_rev["ForecastedRevenue_RWF"] > 0).all(), "Revenue forecast must be strictly positive"

def test_publication_figures_exist():
    """Verify that all 15 publication-grade figures exist in reports/figures/."""
    figures_dir = "reports/figures"
    fig_files = [f"fig{i:02d}" for i in range(1, 16)]
    existing_files = os.listdir(figures_dir) if os.path.exists(figures_dir) else []
    
    for prefix in fig_files:
        matches = [f for f in existing_files if f.startswith(prefix) and f.endswith(".png")]
        assert len(matches) > 0, f"Missing figure with prefix {prefix} in {figures_dir}"
