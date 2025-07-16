import argparse
import json
import pandas as pd
from tqdm import tqdm
from features import extract_features
from model import score_wallets

def load_and_group_data(json_path):
    with open(json_path, 'r') as f:
        tx_list = json.load(f)

    grouped = {}
    for tx in tx_list:
        wallet = tx.get("userWallet")
        if not wallet:
            continue
        if wallet not in grouped:
            grouped[wallet] = []
        grouped[wallet].append(tx)

    return grouped


def main(args):
    wallet_tx_map = load_and_group_data(args.input)

    wallet_features = []
    for wallet, txs in tqdm(wallet_tx_map.items(), desc="Processing wallets"):
        features = extract_features(wallet, txs)
        if features:
            wallet_features.append(features)

    df_features = pd.DataFrame(wallet_features)

    df_scored = score_wallets(df_features)
    df_scored.to_csv(args.output, index=False)
    print(f"Total wallets processed: {len(df_features)}")
    print(df_features.head())
    print(f"[✓] Wallet scores saved to: {args.output}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Path to input JSON file")
    parser.add_argument("--output", default="outputs/wallet_scores.csv", help="Path to output CSV file")
    args = parser.parse_args()
    main(args)
