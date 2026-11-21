"""
NEXAPAY Explainable AI (XAI) Engine
Calculates feature attribution and Shapley-inspired contribution weights 
to provide human-understandable explanations for risk scores.
"""

from typing import Dict, List, Any


class ExplainabilityEngine:
    @staticmethod
    def calculate_attributions(
        base_risk: float, 
        feature_impacts: List[Dict[str, Any]], 
        max_score: float = 100.0
    ) -> Dict[str, Any]:
        """
        Computes normalized Shapley-like feature attribution weights for explainable AI.
        
        Args:
            base_risk: Baseline prior risk score (e.g. 5.0).
            feature_impacts: List of dicts, each with 'feature', 'impact' (points added), 'desc', 'category'.
            max_score: Upper bound for risk score (100.0).
            
        Returns:
            Dict containing total_score, risk_level, breakdown, and top_reasons.
        """
        raw_total = base_risk + sum(item.get("impact", 0.0) for item in feature_impacts)
        clamped_score = max(0.0, min(max_score, raw_total))
        
        # Calculate percentage contribution for each triggered risk factor
        total_positive_impact = sum(max(0.0, item.get("impact", 0.0)) for item in feature_impacts)
        
        breakdown = []
        for item in feature_impacts:
            impact = item.get("impact", 0.0)
            if total_positive_impact > 0:
                pct = round((max(0.0, impact) / total_positive_impact) * 100, 1)
            else:
                pct = 0.0
                
            breakdown.append({
                "feature": item.get("feature", "Indicator"),
                "impact_points": round(impact, 1),
                "contribution_pct": pct,
                "description": item.get("desc", ""),
                "severity": "CRITICAL" if impact >= 30 else ("HIGH" if impact >= 20 else "MODERATE")
            })
            
        # Sort by impact points descending
        breakdown.sort(key=lambda x: x["impact_points"], reverse=True)
        
        # Determine risk level
        if clamped_score < 25.0:
            risk_level = "SAFE"
            badge_color = "#10B981"  # Emerald
            summary = "No significant fraud or security threats detected."
        elif clamped_score < 60.0:
            risk_level = "CAUTION"
            badge_color = "#F59E0B"  # Amber
            summary = "Suspicious patterns detected. Exercise caution and verify independently."
        elif clamped_score < 85.0:
            risk_level = "HIGH_RISK"
            badge_color = "#EA580C"  # Orange/Red
            summary = "High probability of deceptive or fraudulent activity detected."
        else:
            risk_level = "CRITICAL"
            badge_color = "#DC2626"  # Red
            summary = "Severe threat detected. Highly likely to be a targeted scam or credential theft!"
            
        return {
            "risk_score": round(clamped_score, 1),
            "risk_level": risk_level,
            "badge_color": badge_color,
            "summary": summary,
            "baseline_risk": base_risk,
            "features_analyzed": len(feature_impacts),
            "attributions": breakdown,
            "key_takeaways": [b["description"] for b in breakdown[:3] if b["impact_points"] > 0]
        }
