import pandas as pd
import numpy as np
from scipy import stats


class AuditService:
    @staticmethod
    def perform_statistical_audit(data_list):

        df = pd.DataFrame(data_list)

        df.replace(r"^\s*$", np.nan, regex=True, inplace=True)
        df.replace("", np.nan, inplace=True)
        missing = int(df.isnull().sum().sum())

        cols_to_check = [c for c in df.columns if c.lower() not in ["id", "sr", "no"]]
        duplicates = int(df.duplicated(subset=cols_to_check).sum())

        anomalies = []
        for col in df.columns:

            numeric_col = pd.to_numeric(df[col], errors="coerce")

            if numeric_col.notnull().sum() > 2:
                clean_data = numeric_col.dropna()
                z_scores = np.abs(stats.zscore(clean_data))

                outlier_indices = np.where(z_scores > 2.0)[0]

                if len(outlier_indices) > 0:
                    anomalies.append(
                        {
                            "column": col,
                            "count": len(outlier_indices),
                            "suggestion": f"Extreme value detected in '{col}'. Please verify if {clean_data.iloc[outlier_indices[0]]} is a typo.",
                        }
                    )

        total_issues = duplicates + missing + len(anomalies)
        health_score = max(
            0, 100 - (duplicates * 10) - (missing * 5) - (len(anomalies) * 20)
        )

        report = {
            "total_rows": len(df),
            "duplicates": duplicates,
            "missing_values": missing,
            "anomalies": anomalies,
            "health_score": health_score,
        }
# 
        return report, df.to_string()
