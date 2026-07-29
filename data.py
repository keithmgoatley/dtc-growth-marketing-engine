import numpy as np, pandas as pd

RNG = np.random.default_rng(42)

def get_channel_metrics():
    """Generates channel-level acquisition and unit economics data across DTC media stack."""
    return pd.DataFrame([
        {"Channel": "Meta Ads (FB/IG)", "Monthly_Spend": 45000, "Blended_CAC": 32.50, "AOV": 78.00, "12M_LTV": 142.00, "ROAS": 2.4, "Channel_MER": 0.28},
        {"Channel": "Google Search & Shopping", "Monthly_Spend": 30000, "Blended_CAC": 28.10, "AOV": 82.50, "12M_LTV": 155.00, "ROAS": 2.9, "Channel_MER": 0.19},
        {"Channel": "TikTok Ads", "Monthly_Spend": 15000, "Blended_CAC": 41.20, "AOV": 68.00, "12M_LTV": 110.00, "ROAS": 1.65, "Channel_MER": 0.45},
        {"Channel": "Klaviyo Email & SMS", "Monthly_Spend": 3500, "Blended_CAC": 4.80, "AOV": 85.00, "12M_LTV": 168.00, "ROAS": 17.7, "Channel_MER": 0.02},
        {"Channel": "Affiliate & Influencer", "Monthly_Spend": 8000, "Blended_CAC": 22.00, "AOV": 74.00, "12M_LTV": 130.00, "ROAS": 3.36, "Channel_MER": 0.12},
    ]).assign(
        Payback_Months=lambda x: round((x["Blended_CAC"] / (x["AOV"] * 0.55)), 1), # Assuming 55% Gross Margin
        LTV_CAC_Ratio=lambda x: round(x["12M_LTV"] / x["Blended_CAC"], 2)
    )

def get_ltv_cohort_curves():
    """Generates cumulative 12-month LTV progression across quarterly customer cohorts."""
    months = [f"M{i}" for i in range(1, 13)]
    cohorts = ["2025-Q1", "2025-Q2", "2025-Q3", "2025-Q4", "2026-Q1", "2026-Q2"]
    
    rows = []
    for c_idx, cohort in enumerate(cohorts):
        base_aov = 75.0 + (c_idx * 2.5) # Improving AOV over time
        cumulative_ltv = [base_aov]
        for m in range(1, 12):
            reorder_rate = 0.08 + (0.02 * (m % 3 == 0)) # Spikes on month 3, 6, 9
            cumulative_ltv.append(cumulative_ltv[-1] + (base_aov * reorder_rate))
        rows.append(cumulative_ltv)
        
    return pd.DataFrame(rows, columns=months, index=cohorts)

def get_ice_experiment_roadmap():
    """Hypothesis-led CRO, CRM, and Acquisition growth testing matrix with ICE scoring."""
    df = pd.DataFrame([
        {"Hypothesis": "Dynamic Bundle Recommendation on Cart Drawer", "Funnel_Pillar": "CRO", "Impact": 8, "Confidence": 9, "Ease": 7, "Owner": "Growth Manager", "Status": "In Testing"},
        {"Hypothesis": "Post-Purchase SMS Win-Back Sequence (Day 45)", "Funnel_Pillar": "Retention (CRM)", "Impact": 9, "Confidence": 7, "Ease": 9, "Owner": "CRM Lead", "Status": "Backlog"},
        {"Hypothesis": "TikTok UGC Angles targeting Gen-Z Skincare Needs", "Funnel_Pillar": "Acquisition", "Impact": 7, "Confidence": 6, "Ease": 8, "Owner": "Paid Social Specialist", "Status": "Active"},
        {"Hypothesis": "PDP Social Proof & Verified Review Badging", "Funnel_Pillar": "CRO", "Impact": 6, "Confidence": 9, "Ease": 9, "Owner": "Growth Manager", "Status": "Completed (+11% CVR)"},
        {"Hypothesis": "VIP Loyalty Tier with Exclusive Early Access", "Funnel_Pillar": "Retention (CRM)", "Impact": 8, "Confidence": 8, "Ease": 5, "Owner": "Growth Manager", "Status": "In Design"},
    ])
    df["ICE_Score"] = ((df["Impact"] + df["Confidence"] + df["Ease"]) / 3).round(1)
    return df.sort_values(by="ICE_Score", ascending=False)
