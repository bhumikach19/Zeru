# Zeru Aave V2 Wallet Scoring

## Overview
This project analyzes and scores Ethereum wallets based on their activity and behavior in the Aave V2 protocol. The goal is to provide a quantitative assessment of wallets, which can be used for further analysis or downstream applications.

## Method Chosen
The scoring method is based on extracting relevant features from user transaction data, such as deposit/borrow/repay/withdraw events, transaction frequency, and other behavioral metrics. These features are then processed and combined using a scoring model (e.g., weighted sum, machine learning, or rule-based logic) to assign a final score to each wallet.

## Architecture
- **Data Source:** Raw transaction data is stored in `data/user_transactions.json`.
- **Feature Extraction:** The `src/features.py` script processes the raw data to extract meaningful features for each wallet.
- **Scoring:** The `src/score_wallets.py` and `src/model.py` scripts compute scores for each wallet based on the extracted features.
- **Output:** Results are saved in `outputs/wallet_scores.csv` and `outputs/scored_wallets_gui.csv`.
- **GUI:** An optional GUI for visualization and interaction is provided in `src/gui_app.py`.

## Processing Flow
1. **Data Ingestion:** Load transaction data from `data/user_transactions.json`.
2. **Feature Engineering:** Use `features.py` to extract features such as transaction counts, amounts, and behavioral patterns.
3. **Scoring:** Apply the scoring logic/model in `score_wallets.py` and `model.py` to compute a score for each wallet.
4. **Output Generation:** Save the scored wallets to CSV files in the `outputs/` directory.
5. **Analysis & Visualization:** Use the results for further analysis or visualization (see `analysis.md`).

## Requirements
Install dependencies with:
```bash
pip install -r requirements.txt
```

## Running the Project
1. Prepare the data in `data/user_transactions.json`.
2. Run the feature extraction and scoring scripts:
   ```bash
   python src/score_wallets.py
   ```
3. View the results in the `outputs/` directory.
4. (Optional) Launch the GUI:
   ```bash
   python src/gui_app.py
   ```

## Notes
- The scoring logic can be customized in `model.py`.
- For detailed analysis, see `analysis.md` after running the scoring process. 
