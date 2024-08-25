
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

### Notebooks

The models are trained using Jupyter notebooks located in the respective airport directories (e.g., `LEST/notebooks/`). Each notebook is specific to an airport and contains the steps for training and evaluating machine learning models.

To train a model:

1. Navigate to the notebook directory for the desired airport (e.g., `LEST/notebooks/`).
2. Open the desired notebook in Jupyter Notebook or Jupyter Lab.
3. Follow the steps in the notebook to preprocess the data, train the model, and save the trained model to the `algorithms/` directory.

### Input Files

1. get_metar_ICAO-code.ipynb: notebook file to get METAR raports from IOWA STATE UNIVERSITY
2. ICAO-codeY2018Y2022.csv: csv file with meteorological variables observed in METAR raports. Output file from get_metar_ICAO-code.ipynb
3. get_wrf_4k.ipynb: notebook file to get historical meteorological WRF models from METEOGALICIA
4. distan_lat(a)lon(b)p(c)R(d)Km.csv: file with the coordinates of the c nearest points (distance between model point d Km) from airport coordinates (latitude a and longitude b). Output file from the script get_wrf_4k.ipynb.
5. lat(a)lon(b)p(c)R(d)Km.kml: kml file with points file above. Output file from the script get_wrf_4k.ipynb.
6. lat(a)lon(b)p(c)R(d)KmD(e)Y(f).csv: csv file with forecasted meteorological variables (forecast range Day (e) from Year (f)). Variables with subindex 0 belong to the nearest point from lat(a)lon(b) point (airport coordinates) and so on. Distance between forecasted points (d). Output file from the script get_wrf_4k.ipynb.





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
