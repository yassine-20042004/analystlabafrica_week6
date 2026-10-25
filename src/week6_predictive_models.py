"""
HealthConnect Rwanda Healthcare Analytics & AI Transformation Project
Track 2: Data Science Track - Predictive Analytics, Forecasting, Clustering & PCA
Module: src/week6_predictive_models.py
"""

import os
import sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import json
import pandas as pd
import numpy as np
import joblib
from datetime import datetime

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression, Ridge, LinearRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score, roc_auc_score,
    confusion_matrix, mean_squared_error, mean_absolute_error, r2_score
)
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from statsmodels.tsa.holtwinters import ExponentialSmoothing

class HealthConnectPredictiveSuite:
    def __init__(self, processed_dir="data/processed", models_dir="models"):
        self.processed_dir = processed_dir
        self.models_dir = models_dir
        os.makedirs(self.models_dir, exist_ok=True)
        self.cohort_path = os.path.join(self.processed_dir, "feature_engineered_cohort.csv")
        self.df = pd.read_csv(self.cohort_path)
        self.raw_rev_summary = pd.read_csv("data/raw/HC_Revenue_Summary.csv")
        self.results = {}

    def task1_forecast_patient_volume(self):
        """Forecasts monthly patient visits for the next 12 months (2027-01 to 2027-12)."""
        print(">> [1/7] Running Task 1: Time Series Patient Volume Forecasting...")
        df_rev = self.raw_rev_summary.copy()
        df_rev["MonthDate"] = pd.to_datetime(df_rev["Month"])
        history_visits = df_rev["Appointments"].values
        
        # Fit Holt-Winters Exponential Smoothing model
        model = ExponentialSmoothing(
            history_visits,
            trend="add",
            seasonal=None,
            initialization_method="estimated"
        ).fit()
        
        # Forecast 12 months ahead
        forecast_12m = model.forecast(12)
        # Apply standard error confidence interval
        residuals = history_visits - model.fittedvalues
        sigma = np.std(residuals)
        
        future_dates = pd.date_range(start="2027-01-01", periods=12, freq="MS").strftime("%Y-%m").tolist()
        forecast_df = pd.DataFrame({
            "Month": future_dates,
            "ForecastedVisits": np.round(forecast_12m).astype(int),
            "LowerBound_95%": np.maximum(0, np.round(forecast_12m - 1.96 * sigma)).astype(int),
            "UpperBound_95%": np.round(forecast_12m + 1.96 * sigma).astype(int)
        })
        
        # Combined history and forecast
        hist_df = pd.DataFrame({
            "Month": df_rev["Month"].tolist(),
            "HistoricalVisits": df_rev["Appointments"].tolist(),
            "FittedVisits": np.round(model.fittedvalues).astype(int)
        })

        forecast_csv = os.path.join(self.processed_dir, "forecast_patient_volume_12m.csv")
        forecast_df.to_csv(forecast_csv, index=False)
        
        mae = float(mean_absolute_error(history_visits, model.fittedvalues))
        rmse = float(np.sqrt(mean_squared_error(history_visits, model.fittedvalues)))
        mape = float(np.mean(np.abs(residuals / history_visits)) * 100)

        self.results["Task1_Patient_Volume_Forecast"] = {
            "Model": "Holt-Winters Additive Exponential Smoothing",
            "History_Total_Visits_2026": int(np.sum(history_visits)),
            "Forecast_Total_Visits_2027": int(forecast_df["ForecastedVisits"].sum()),
            "Annual_Growth_Rate_%": round(((forecast_df["ForecastedVisits"].sum() - np.sum(history_visits)) / np.sum(history_visits)) * 100, 2),
            "Train_MAE": round(mae, 2),
            "Train_RMSE": round(rmse, 2),
            "Train_MAPE_%": round(mape, 2),
            "Forecast_Table": forecast_df.to_dict(orient="records")
        }
        print(f"   -> 2027 Forecasted Visits: {forecast_df['ForecastedVisits'].sum():,} (MAE: {mae:.1f}, MAPE: {mape:.2f}%)")
        return forecast_df

    def task2_forecast_revenue(self):
        """Forecasts monthly revenue for the next 12 months (2027-01 to 2027-12)."""
        print(">> [2/7] Running Task 2: Time Series Hospital Revenue Forecasting...")
        df_rev = self.raw_rev_summary.copy()
        history_rev = df_rev["Revenue"].values
        
        # Fit Holt-Winters Exponential Smoothing model on revenue
        model = ExponentialSmoothing(
            history_rev,
            trend="add",
            seasonal=None,
            initialization_method="estimated"
        ).fit()
        
        forecast_12m = model.forecast(12)
        residuals = history_rev - model.fittedvalues
        sigma = np.std(residuals)
        
        future_dates = pd.date_range(start="2027-01-01", periods=12, freq="MS").strftime("%Y-%m").tolist()
        forecast_df = pd.DataFrame({
            "Month": future_dates,
            "ForecastedRevenue_RWF": np.round(forecast_12m).astype(int),
            "LowerBound_95%_RWF": np.maximum(0, np.round(forecast_12m - 1.96 * sigma)).astype(int),
            "UpperBound_95%_RWF": np.round(forecast_12m + 1.96 * sigma).astype(int)
        })
        
        forecast_csv = os.path.join(self.processed_dir, "forecast_hospital_revenue_12m.csv")
        forecast_df.to_csv(forecast_csv, index=False)
        
        mae = float(mean_absolute_error(history_rev, model.fittedvalues))
        rmse = float(np.sqrt(mean_squared_error(history_rev, model.fittedvalues)))
        mape = float(np.mean(np.abs(residuals / history_rev)) * 100)

        self.results["Task2_Revenue_Forecast"] = {
            "Model": "Holt-Winters Additive Exponential Smoothing",
            "History_Total_Revenue_2026_RWF": int(np.sum(history_rev)),
            "Forecast_Total_Revenue_2027_RWF": int(forecast_df["ForecastedRevenue_RWF"].sum()),
            "Annual_Revenue_Growth_%": round(((forecast_df["ForecastedRevenue_RWF"].sum() - np.sum(history_rev)) / np.sum(history_rev)) * 100, 2),
            "Train_MAE_RWF": round(mae, 2),
            "Train_RMSE_RWF": round(rmse, 2),
            "Train_MAPE_%": round(mape, 2),
            "Forecast_Table": forecast_df.to_dict(orient="records")
        }
        print(f"   -> 2027 Forecasted Revenue: {forecast_df['ForecastedRevenue_RWF'].sum():,} RWF (MAPE: {mape:.2f}%)")
        return forecast_df

    def task3_hospital_admission_prediction(self):
        """Predicts probability of hospital admission after an appointment."""
        print(">> [3/7] Running Task 3: Hospital Admission Classification Models...")
        df = self.df.copy()
        
        features_num = ["Age", "BMI", "DoctorExperience", "DiseaseSeverityScore", "Amount", "DepartmentWorkloadIndex"]
        features_cat = ["Gender", "ChronicCondition", "VisitType", "Diagnosis", "LabResult", "ProvinceName", "FacilityType", "Ownership"]
        
        X = df[features_num + features_cat]
        y = df["IsAdmitted"]
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)
        
        preprocessor = ColumnTransformer(
            transformers=[
                ("num", StandardScaler(), features_num),
                ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), features_cat)
            ]
        )
        
        models = {
            "Logistic_Regression": LogisticRegression(max_iter=1000, random_state=42, class_weight="balanced"),
            "Random_Forest": RandomForestClassifier(n_estimators=150, max_depth=8, random_state=42, class_weight="balanced"),
            "Gradient_Boosting": GradientBoostingClassifier(n_estimators=120, learning_rate=0.08, max_depth=4, random_state=42)
        }
        
        model_benchmarks = []
        trained_pipelines = {}
        
        for name, clf in models.items():
            pipe = Pipeline([
                ("pre", preprocessor),
                ("clf", clf)
            ])
            pipe.fit(X_train, y_train)
            trained_pipelines[name] = pipe
            
            y_pred = pipe.predict(X_test)
            y_prob = pipe.predict_proba(X_test)[:, 1]
            
            acc = accuracy_score(y_test, y_pred)
            prec = precision_score(y_test, y_pred, zero_division=0)
            rec = recall_score(y_test, y_pred, zero_division=0)
            f1 = f1_score(y_test, y_pred, zero_division=0)
            roc = roc_auc_score(y_test, y_prob)
            cm = confusion_matrix(y_test, y_pred).tolist()
            
            model_benchmarks.append({
                "Algorithm": name,
                "Accuracy": round(float(acc), 4),
                "Precision": round(float(prec), 4),
                "Recall": round(float(rec), 4),
                "F1_Score": round(float(f1), 4),
                "ROC_AUC": round(float(roc), 4),
                "ConfusionMatrix": cm
            })
            print(f"   - {name}: ROC-AUC = {roc:.4f}, F1 = {f1:.4f}, Accuracy = {acc:.4f}")
        
        # Select best model
        best_benchmark = max(model_benchmarks, key=lambda x: x["ROC_AUC"])
        best_model_name = best_benchmark["Algorithm"]
        best_pipeline = trained_pipelines[best_model_name]
        joblib.dump(best_pipeline, os.path.join(self.models_dir, "hospital_admission_model.pkl"))
        
        # Feature importances from Random Forest
        rf_model = trained_pipelines["Random_Forest"].named_steps["clf"]
        cat_encoder = trained_pipelines["Random_Forest"].named_steps["pre"].named_transformers_["cat"]
        all_feature_names = features_num + list(cat_encoder.get_feature_names_out(features_cat))
        rf_importances = pd.DataFrame({
            "Feature": all_feature_names,
            "Importance": rf_model.feature_importances_
        }).sort_values(by="Importance", ascending=False)
        rf_importances.to_csv(os.path.join(self.processed_dir, "admission_feature_importances.csv"), index=False)
        
        self.results["Task3_Hospital_Admission_Prediction"] = {
            "Benchmarks": model_benchmarks,
            "Best_Model": best_model_name,
            "Top_5_Predictors": rf_importances.head(5).to_dict(orient="records")
        }
        return model_benchmarks

    def task4_patient_satisfaction_prediction(self):
        """Predicts patient satisfaction rating using clinical and operational features."""
        print(">> [4/7] Running Task 4: Patient Satisfaction Prediction Models...")
        df_rated = self.df.dropna(subset=["Rating"]).copy()
        
        features_num = ["Age", "DoctorExperience", "DepartmentWorkloadIndex", "FacilityPerformanceScore", "LengthOfStayDays", "Amount", "DiseaseSeverityScore"]
        features_cat = ["Gender", "VisitType", "DepartmentName", "FacilityType", "ClaimStatus"]
        
        X = df_rated[features_num + features_cat]
        y = df_rated["Rating"]
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
        
        preprocessor = ColumnTransformer(
            transformers=[
                ("num", StandardScaler(), features_num),
                ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), features_cat)
            ]
        )
        
        regressors = {
            "Ridge_Regression": Ridge(alpha=1.0),
            "Random_Forest_Regressor": RandomForestRegressor(n_estimators=150, max_depth=6, random_state=42),
            "Gradient_Boosting_Regressor": GradientBoostingRegressor(n_estimators=100, learning_rate=0.05, max_depth=3, random_state=42)
        }
        
        benchmarks = []
        for name, reg in regressors.items():
            pipe = Pipeline([
                ("pre", preprocessor),
                ("reg", reg)
            ])
            pipe.fit(X_train, y_train)
            preds = pipe.predict(X_test)
            
            rmse = np.sqrt(mean_squared_error(y_test, preds))
            mae = mean_absolute_error(y_test, preds)
            r2 = r2_score(y_test, preds)
            
            benchmarks.append({
                "Algorithm": name,
                "RMSE": round(float(rmse), 4),
                "MAE": round(float(mae), 4),
                "R2_Score": round(float(r2), 4)
            })
            print(f"   - {name}: RMSE = {rmse:.4f}, MAE = {mae:.4f}, R2 = {r2:.4f}")
            
        best_reg = min(benchmarks, key=lambda x: x["RMSE"])
        self.results["Task4_Satisfaction_Prediction"] = {
            "Benchmarks": benchmarks,
            "Best_Model": best_reg["Algorithm"]
        }
        return benchmarks

    def task5_department_workload_forecast(self):
        """Forecasts patient demand across hospital departments."""
        print(">> [5/7] Running Task 5: Department Workload Forecasting...")
        df = self.df.copy()
        
        # Department demand by month in cohort
        dept_monthly = df.groupby(["Month", "DepartmentName"]).size().unstack(fill_value=0)
        
        # 12-month future department demand projections
        # Assume overall system growth rate applied with departmental seasonality weights
        total_2026_cohort = len(df)
        dept_shares = (df["DepartmentName"].value_counts() / total_2026_cohort).to_dict()
        
        # Total forecasted 2027 visits from Task 1
        forecast_total_2027 = self.results["Task1_Patient_Volume_Forecast"]["Forecast_Total_Visits_2027"]
        
        dept_forecast_rows = []
        for dept, share in dept_shares.items():
            projected_annual_visits = int(round(share * forecast_total_2027))
            current_annual_visits = int(round(share * self.results["Task1_Patient_Volume_Forecast"]["History_Total_Visits_2026"]))
            dept_forecast_rows.append({
                "Department": dept,
                "Current_2026_Visits": current_annual_visits,
                "Forecasted_2027_Visits": projected_annual_visits,
                "Projected_Net_Growth": projected_annual_visits - current_annual_visits,
                "Workload_Share_%": round(share * 100, 2),
                "Staffing_Recommendation": "Increase clinical shifts" if share > 0.12 else "Maintain baseline staffing"
            })
            
        df_dept_forecast = pd.DataFrame(dept_forecast_rows).sort_values(by="Forecasted_2027_Visits", ascending=False)
        dept_csv = os.path.join(self.processed_dir, "forecast_department_workload_2027.csv")
        df_dept_forecast.to_csv(dept_csv, index=False)
        
        self.results["Task5_Department_Workload_Forecast"] = df_dept_forecast.to_dict(orient="records")
        print(f"   -> Department workload forecast generated for {len(df_dept_forecast)} clinical departments.")
        return df_dept_forecast

    def run_clustering_analysis(self):
        """Performs K-Means clustering for Patient Segmentation and Facility Segmentation."""
        print(">> [6/7] Running Clustering Analysis (Unsupervised Learning)...")
        df = self.df.copy()
        
        # 1. Patient Segmentation
        pt_features = ["Age", "BMI", "DoctorExperience", "DiseaseSeverityScore", "Amount", "LengthOfStayDays", "HighRiskPatientIndicator"]
        X_pt = df[pt_features].copy()
        scaler_pt = StandardScaler()
        X_pt_scaled = scaler_pt.fit_transform(X_pt)
        
        kmeans_pt = KMeans(n_clusters=4, random_state=42, n_init=10)
        df["PatientCluster"] = kmeans_pt.fit_predict(X_pt_scaled)
        
        # Cluster Profiles
        cluster_summary = df.groupby("PatientCluster").agg(
            Size=("AppointmentID", "count"),
            MeanAge=("Age", "mean"),
            MeanBMI=("BMI", "mean"),
            AdmissionRate=("IsAdmitted", "mean"),
            MeanBilling=("Amount", "mean"),
            SeverityScore=("DiseaseSeverityScore", "mean"),
            HighRiskRate=("HighRiskPatientIndicator", "mean")
        ).reset_index()
        
        cluster_names = {
            0: "Cluster 0: Young & Mild Outpatients",
            1: "Cluster 1: Chronic & Geriatric High-Risk",
            2: "Cluster 2: Moderate Surgical / Admitted Patients",
            3: "Cluster 3: Acute Emergency & High Cost"
        }
        cluster_summary["ClusterLabel"] = cluster_summary["PatientCluster"].map(cluster_names)
        cluster_summary.to_csv(os.path.join(self.processed_dir, "patient_cluster_profiles.csv"), index=False)
        
        # 2. Facility Segmentation
        fac_df = pd.read_csv(os.path.join(self.processed_dir, "facility_performance_metrics.csv"))
        fac_features = ["FacAppointments", "FacMeanSatisfaction", "FacTotalRevenue", "FacAdmissions", "FacilityPerformanceScore"]
        X_fac = StandardScaler().fit_transform(fac_df[fac_features])
        kmeans_fac = KMeans(n_clusters=3, random_state=42, n_init=10)
        fac_df["FacilityCluster"] = kmeans_fac.fit_predict(X_fac)
        fac_df.to_csv(os.path.join(self.processed_dir, "facility_clusters.csv"), index=False)

        self.results["Clustering_Analysis"] = {
            "Patient_Clusters": cluster_summary.to_dict(orient="records"),
            "Facility_Clusters_Count": 3
        }
        print("   -> Patient clusters (k=4) and Facility clusters (k=3) generated successfully.")
        return cluster_summary

    def run_pca_dimensionality_reduction(self):
        """Applies PCA to numerical feature space and extracts explained variance."""
        print(">> [7/7] Running Principal Component Analysis (PCA)...")
        df = self.df.copy()
        num_features = ["Age", "BMI", "DoctorExperience", "DiseaseSeverityScore", "Amount", "LengthOfStayDays", "DepartmentWorkloadIndex", "FacilityPerformanceScore"]
        
        X_scaled = StandardScaler().fit_transform(df[num_features])
        pca = PCA(n_components=len(num_features), random_state=42)
        pca.fit(X_scaled)
        
        var_ratio = pca.explained_variance_ratio_
        cum_var = np.cumsum(var_ratio)
        
        pca_summary = pd.DataFrame({
            "Principal_Component": [f"PC{i+1}" for i in range(len(num_features))],
            "Explained_Variance_Ratio": np.round(var_ratio, 4),
            "Cumulative_Variance_Ratio": np.round(cum_var, 4)
        })
        pca_summary.to_csv(os.path.join(self.processed_dir, "pca_explained_variance.csv"), index=False)
        
        # Component Loadings for PC1 and PC2
        loadings = pd.DataFrame(
            pca.components_[:2].T,
            columns=["PC1_Loading", "PC2_Loading"],
            index=num_features
        ).round(4)
        loadings.to_csv(os.path.join(self.processed_dir, "pca_feature_loadings.csv"))
        
        self.results["PCA_Analysis"] = {
            "Explained_Variance": pca_summary.to_dict(orient="records"),
            "PC1_and_PC2_Cumulative_Variance_%": round(float(cum_var[1] * 100), 2)
        }
        print(f"   -> PCA completed. First 2 PCs capture {cum_var[1]*100:.2f}% of feature variance.")
        return pca_summary

    def save_all_modeling_results(self):
        results_json = os.path.join(self.processed_dir, "predictive_modeling_results.json")
        with open(results_json, "w") as f:
            json.dump(self.results, f, indent=4)
        print(f"All predictive analytics results saved to {results_json}")

if __name__ == "__main__":
    suite = HealthConnectPredictiveSuite()
    suite.task1_forecast_patient_volume()
    suite.task2_forecast_revenue()
    suite.task3_hospital_admission_prediction()
    suite.task4_patient_satisfaction_prediction()
    suite.task5_department_workload_forecast()
    suite.run_clustering_analysis()
    suite.run_pca_dimensionality_reduction()
    suite.save_all_modeling_results()
