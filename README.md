
# Airport Machine Learning Models

This repository provides machine learning models and tools designed to predict meteorological variables as reported in METARs. The repository includes two types of algorithms: those based on the scikit-learn library (deployed via airport_ml.py) and algorithms leveraging large language models (LLMs), which are deployed using mlmetar_forecast.py. The models are trained on meteorological data specific to each airport, identified by its ICAO code.

## Repository Structure

```bash
.
├── README.md                 # Project documentation (this file)
├── airport_ml.py             # Script for running ML models based on the scikit-learn library
├── help_functions.py         # Helper functions used across different scripts
├── mlmetar_forecast.py       # Script for METAR forecasting leveraging large language models (LLMs)
├── requirements.txt          # Python packages and dependencies required
├── ICAO/                     # Files and models related to ICAO code airport
│   ├── algorithms/           # Pre-trained model files (.al) for ICAO code airport
│   ├── input_files/          # Input data files for training models for ICAO code airport
│   └── notebooks/            # Jupyter notebooks for training and testing models for ICAO code airport

```

## Usage

### Training Models

The models are trained using Jupyter notebooks located in the respective airport directories (e.g., `LEST/notebooks/`). Each notebook is specific to an airport and contains the steps for training and evaluating machine learning models.

To train a model:

1. Navigate to the notebook directory for the desired airport (e.g., `LEST/notebooks/`).
2. Open the desired notebook in Jupyter Notebook or Jupyter Lab.
3. Follow the steps in the notebook to preprocess the data, train the model, and save the trained model to the `algorithms/` directory.

### Input Files


### Running the Main Script

The main script `airport_ml.py` integrates the trained models for predicting SPECI issuance. To run the script:

```bash
python airport_ml.py
```

### METAR Forecasting

The `mlmetar_forecast.py` script provides functionalities to forecast METAR data using the trained models. It uses the data and models from the respective airport directories.

```bash
python mlmetar_forecast.py
```

### Dependencies

The required Python packages and dependencies are listed in the `requirements.txt` file. To install them, run:

```bash
pip install -r requirements.txt
```

## Contributing

Contributions to the project are welcome! Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Commit your changes and push the branch to your fork.
4. Open a Pull Request with a detailed description of your changes.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.
