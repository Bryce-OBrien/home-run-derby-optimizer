# 2025 Home Run Derby Optimizer

This is a fantasy baseball web app built using **Streamlit** and **PuLP** to help you draft your optimal team for the 2025 Home Run Derby competition.

## ⚾ Competition Rules
- Draft **8 MLB players** within a **163-point budget** (each point = HRs hit in 2024)
- Each month, **only your top 7 HR hitters** count toward your total
- Highest monthly HR total wins (with midseason and end-of-season prizes)

## 🔧 What the App Does
- Displays the player pool and default 2025 HR projections (from The Bat & The Bat X by Derek Carty via Fangraphs)
- Lets you customize any player's HR projection
- Offers two optimization strategies:
  - **Balanced Optimizer**: Maximize total projected HRs across all 8 players
  - **Top-Heavy Optimizer**: Maximize top 7 of 8 players to focus on peak scoring

## 🚀 How to Run
```bash
# From the root folder:
streamlit run app.py
```

## 📂 Folder Contents
```
home-run-derby-optimizer/
├── app.py                      # Main Streamlit web app
├── optimizer.py                # Optimizer logic
├── final_2025_combined_dataset.csv  # Editable dataset
├── requirements.txt            # Dependencies
└── README.md                   # This file
```
