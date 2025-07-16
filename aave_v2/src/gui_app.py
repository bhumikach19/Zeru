import gradio as gr
import pandas as pd
import json
import os
import traceback

from features import extract_features
from model import score_wallets

OUTPUT_PATH = "outputs/scored_wallets_gui.csv"

def score_wallets_from_json(json_file):
    try:
        print(f"Received file: {json_file}")  # Add this line
        with open(json_file.name, 'r') as f:
            content = json.load(f)

        if not isinstance(content, list):
            return "❌ Invalid JSON structure: must be a list of transactions", None

        # Group transactions by wallet
        wallet_map = {}
        for tx in content:
            wallet = tx.get("userWallet")
            if not wallet:
                continue
            wallet_map.setdefault(wallet, []).append(tx)

        if not wallet_map:
            return "❌ No valid wallets found in the file", None

        # Extract features
        wallet_features = []
        for wallet, txs in wallet_map.items():
            features = extract_features(wallet, txs)
            if features:
                wallet_features.append(features)

        if not wallet_features:
            return "❌ No wallet features could be extracted", None

        df_features = pd.DataFrame(wallet_features)
        df_scored = score_wallets(df_features)

        os.makedirs("outputs", exist_ok=True)
        df_scored.to_csv(OUTPUT_PATH, index=False)

        return df_scored, OUTPUT_PATH

    except Exception as e:
        error_msg = f"❌ Error: {str(e)}\n\n{traceback.format_exc()}"
        print(error_msg)
        return error_msg, None


with gr.Blocks(title="Aave V2 Credit Scoring") as demo:
    gr.Markdown("**Aave V2 Wallet Credit Scoring App**")

    with gr.Row():
        json_input = gr.File(label="Upload user_transactions.json", file_types=[".json"])
    
    with gr.Row():
        score_btn = gr.Button("Score Wallets", variant="primary")

    with gr.Row():
        output_table = gr.Dataframe(label="Wallet Scores")
        download_btn = gr.File(label="Download CSV")

    def run_scoring(file):
        df, path = score_wallets_from_json(file)
        if isinstance(df, pd.DataFrame):
            return df, path
        else:
            return gr.update(value=df), None

    score_btn.click(fn=run_scoring, inputs=[json_input], outputs=[output_table, download_btn])

demo.launch(share=True)
