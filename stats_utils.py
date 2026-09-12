from scipy import stats



def check_significance(scores_a: list[float], scores_b: list[float], alpha: float = 0.05) -> dict:
    """
    Runs an independent two-sample t-test between version A and version B scores.
    Returns whether the difference is statistically significant at the given alpha.
    Needs a reasonable sample size per version (aim for 30+) before this is meaningful.
    """
    if len(scores_a) < 2 or len(scores_b) < 2:
        return {"p_value": None, "significant": False, "note": "Not enough data yet"}

    t_stat, p_value = stats.ttest_ind(scores_a, scores_b)
    return {
        "t_stat": t_stat,
        "p_value": p_value,
        "significant": p_value < alpha,
        "mean_a": sum(scores_a) / len(scores_a),
        "mean_b": sum(scores_b) / len(scores_b),
        "n_a": len(scores_a),
        "n_b": len(scores_b),
    }