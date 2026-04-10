# Master's Thesis: Probabilistic Electricity Price Forecasting

This repository contains the code, data, and results for my Master's thesis on probabilistic electricity price forecasting. The project utilizes the [EPF Toolbox](https://github.com/jeslago/epftoolbox), an open-access library for electricity price forecasting research.

## Overview

The thesis focuses on forecasting day-ahead electricity prices for Spain and Germany using LASSE-Estimated Autoregressive models (LEAR) for point forecasts and Quantile Regression Averaging (QRA) to obtain probabilistic forecasts. Key components include:

- **Data Acquisition**: Downloading historical electricity prices, load forecasts, and renewable energy forecasts from ENTSOE API.
- **Data Processing**: Cleaning, merging, and transforming raw data into suitable formats for modeling.
- **Modeling**: Implementing the LEAR model for point predictions and QRA for probabilistic forecasts.
- **Evaluation**: Assessing forecast accuracy using metrics like MAE, RMSE, and statistical tests.
- **Visualization**: Generating plots and heatmaps to analyze results.

## Repository Structure

- `data/`: Contains raw, processed, and forecast data
  - `raw/`: Scripts for downloading data from ENTSOE
  - `processed/`: Data cleaning and preprocessing scripts
  - `forecasts/`: Generated point and probabilistic forecasts
  - `residuals/`: Model residuals and error metrics
  - `qra/`: Quantile regression averaging results
- `epftoolbox/`: The EPF Toolbox library (submodule or local copy)
- `helpers/`: Utility functions for data handling, visualization, etc.
- `models/`: Model implementations (LEAR, benchmarks)
- `results/`: Output figures and tables
- `tests/`: Evaluation scripts
- `visualization/`: Plotting and visualization scripts

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/benrodion/prob-electricity-price-forecasting.git
   cd prob-electricity-price-forecasting
   ```

2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Install the project in editable mode:
   ```bash
   pip install -e .
   ```

## Setup

Before running the scripts, you need to obtain an API key from [ENTSOE](https://transparency.entsoe.eu/) for downloading electricity market data.

Create a `.env` file in the `config/` directory (create the directory if it doesn't exist) with your API key:
```
API_KEY=your_entsoe_api_key_here
```

## Usage

The project is structured as a pipeline. Run the scripts in the following order:

1. **Download Data**:
   ```bash
   python data/raw/download_spain.py
   python data/raw/download_germany.py
   ```

2. **Process Data**:
   ```bash
   python data/processed/cleaning.py
   python data/processed/preprocessing.py
   ```

3. **Generate Forecasts**:
   ```bash
   python data/forecasts/point_pred.py
   python data/forecasts/qra.py # CAREFUL: this will take very long. Be sure to check that the setting 'workers=10' does not exceed your devices computing power
   ```

4. **Evaluate Results**:
   ```bash
   python tests/lear_eval.py
   python tests/qra_eval.py
   ```

5. **Visualize Results**:
   ```bash
   python visualization/descriptive_viz.py
   python visualization/point_pred_viz.py
   python visualization/qra_viz.py
   ```

Note: Some scripts may take significant time to run, especially model training and forecasting.

## Results

The results of the analysis are stored in:
- `data/forecasts/`: Forecast files for Spain (es_*) and Germany (ger_*)
- `results/figures/`: Visualization plots
- `results/tables/`: Summary tables and metrics

## Dependencies

Key dependencies include:
- epftoolbox: Electricity price forecasting library
- pandas, numpy: Data manipulation
- scikit-learn: Machine learning
- tensorflow: Deep learning
- matplotlib, seaborn: Visualization
- entsoe-py: ENTSOE API client

See `requirements.txt` for the full list.

## Citation

If you use this code in your research, please cite the EPF Toolbox paper:

Lago, J., Marcjasz, G., De Schutter, B., & Weron, R. (2021). Forecasting day-ahead electricity prices: A review of state-of-the-art algorithms, best practices and an open-access benchmark. *Applied Energy*, 293, 116983.

## License

This project is licensed under the AGPL-3.0 License (inherited from EPF Toolbox).
