# Airline Delay & Oil Price Scorer

A Python tool that analyzes airline delay data and oil price changes to provide a BUY, HOLD, or SELL recommendation for U.S. airlines.

---

## Features

- Parses airline delay CSV data  
- Calculates delay rates and scores  
- Integrates live oil prices from Yahoo Finance  
- Normalizes and adjusts airline scores based on oil price movement  
- Outputs clean tabular recommendations  

---

## Requirements

Install all required packages using:

```bash
pip install -r requirements.txt
```

---

## Usage

Run the script from your terminal:

```bash
python main.py
```

Make sure `Airline_Delay_Cause.csv` is in the same folder.

---

## Project Structure

```
airline-delay-oil-scorer/
├── main.py
├── Airline_Delay_Cause.csv
├── requirements.txt
└── README.md
```

---

## 📄 License

MIT License – feel free to use or modify.

---

## 👨‍💻 Author

Made by **Srikar Kalluri**  
Inspired by real-world airline data and macroeconomic signals.
