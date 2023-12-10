# Sentiment Analysis for Customer Reviews in E-commerce

## Overview

This project implements a sentiment analysis model for e-commerce customer reviews. The goal is to categorize reviews into positive or negative sentiments using machine learning techniques.

## Requirements

- Python 3.12
- Required Python packages: numpy, pandas, scikit-learn, matplotlib, seaborn

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/your-repository.git
    ```

2. Install the required packages:

    ```bash
    pip install scikit-learn
    ```

## Usage

1. Navigate to the project directory:

    ```bash
    cd mlProject
    cd src
    ```

2. Run the sentiment analysis script:

    ```bash
    python sentiment.py
    ```

3. Either use the dataset provided in the data folder or put in your own dataset and change line 10 to your file name:

    ```bash
    df = pd.read_csv('../data/amazon.csv')
    ```

## Project Structure

- `data/`: Contains the dataset used for sentiment analysis.
- `src/`: Holds the source code for sentiment analysis.

## Results

After running the sentiment analysis script, you can find the results, including accuracy, confusion matrix, and visualizations, in the `results/` directory.

## Acknowledgements

- This project uses scikit-learn for machine learning functionalities.

## Issues and Contributions

Feel free to open issues if you encounter problems or have suggestions for improvements. Contributions are welcome!

