import numpy as np
import pandas as pd
from collections import Counter
from datetime import datetime

def extract_features(address, txs):
    if not txs or len(txs) == 0:
        return None

    actions = []
    timestamps = []
    amounts = []

    for tx in txs:
        action = tx.get("action")
        if not action:
            continue

        timestamp = tx.get("timestamp", 0)

        # Extract from actionData
        action_data = tx.get("actionData", {})
        raw_amount = action_data.get("amount", "0")
        try:
            amount = float(raw_amount)
        except:
            amount = 0.0

        actions.append(action.lower())
        timestamps.append(timestamp)
        amounts.append(amount)

    if not actions:
        return None

    df = pd.DataFrame({
        "action": actions,
        "timestamp": timestamps,
        "amount": amounts
    }).sort_values(by="timestamp")

    from collections import Counter
    import numpy as np

    counts = Counter(df["action"])
    total = len(df)

    time_gaps = np.diff(df["timestamp"].values)
    avg_gap = np.mean(time_gaps) if len(time_gaps) > 0 else 0

    repay = counts.get("repay", 0)
    borrow = counts.get("borrow", 0)
    deposit = counts.get("deposit", 0)
    liquidation = counts.get("liquidationcall", 0)

    repay_borrow_ratio = repay / borrow if borrow else 0
    borrow_deposit_ratio = borrow / deposit if deposit else 0

    return {
        "wallet_address": address,
        "total_actions": total,
        "deposit_count": deposit,
        "borrow_count": borrow,
        "repay_count": repay,
        "redeem_count": counts.get("redeemunderlying", 0),
        "liquidation_count": liquidation,
        "repay_borrow_ratio": repay_borrow_ratio,
        "borrow_deposit_ratio": borrow_deposit_ratio,
        "avg_time_gap": avg_gap
    }
