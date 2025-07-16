import pandas as pd

def score_wallet(row):
    score = 600

    # Reward: higher deposits and repayments
    score += row["deposit_count"] * 3
    score += row["repay_count"] * 4

    # Penalty: high liquidations
    score -= row["liquidation_count"] * 10

    # Reward: good repay-to-borrow ratio
    score += min(row["repay_borrow_ratio"] * 20, 40)

    # Penalize low avg gap (bot-like)
    if row["avg_time_gap"] < 60:
        score -= 50
    elif row["avg_time_gap"] < 3600:
        score -= 20

    # Normalize
    return int(min(max(score, 0), 1000))

def score_wallets(df):
    df["score"] = df.apply(score_wallet, axis=1)
    return df[["wallet_address", "score"]]
