import yfinance as yf
import numpy as np
import pandas as pd
from hmmlearn.hmm import GaussianHMM
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split

# Step 1: Data Collection and Preprocessing

def download_stock_data(ticker, start_date, end_date):
    data = yf.download(ticker, start=start_date, end=end_date)
    data['Returns'] = data['Adj Close'].pct_change().dropna()
    return data.dropna()

# Step 2: Gaussian HMM Model

def fit_hmm(returns, n_hidden_states=2):
    model = GaussianHMM(n_components=n_hidden_states, covariance_type="diag", n_iter=1000)
    model.fit(returns.reshape(-1, 1))  # Reshape the returns for HMM
    hidden_states = model.predict(returns.reshape(-1, 1))
    return model, hidden_states

# Step 3: Visualization and Analysis

def plot_hidden_states(data, hidden_states, stock_name):
    plt.figure(figsize=(12, 6))
    plt.plot(data.index, data['Adj Close'], label=f"{stock_name} Adjusted Close Price")
    plt.scatter(data.index, hidden_states, c=hidden_states, cmap='viridis', label="Hidden States", marker='o', alpha=0.6)
    plt.title(f"Hidden States in {stock_name} Price (HMM)")
    plt.xlabel("Date")
    plt.ylabel("Stock Price")
    plt.legend()
    plt.show()

def plot_return_states(data, hidden_states, stock_name):
    plt.figure(figsize=(12, 6))
    plt.plot(data.index, data['Returns'], label=f"{stock_name} Returns")
    plt.scatter(data.index, hidden_states, c=hidden_states, cmap='coolwarm', label="Hidden States", marker='o', alpha=0.6)
    plt.title(f"Hidden States in {stock_name} Returns (HMM)")
    plt.xlabel("Date")
    plt.ylabel("Daily Returns")
    plt.legend()
    plt.show()

# Step 4: Transition Matrix Analysis

def analyze_transition_matrix(model):
    print("Transition Matrix between Hidden States:")
    print(model.transmat_)

# Step 5: Main Function to Execute the Analysis

def main():
    stock = 'AAPL'  # Choose the stock symbol (Apple as an example)
    start_date = '2010-01-01'
    end_date = '2023-01-01'

    # Step 1: Download and preprocess stock data
    data = download_stock_data(stock, start_date, end_date)

    # Step 2: Fit the HMM model with 2 hidden states (bull and bear markets)
    model, hidden_states = fit_hmm(data['Returns'].values, n_hidden_states=2)

    # Step 3: Visualization of the hidden states on stock price and returns
    plot_hidden_states(data, hidden_states, stock)
    plot_return_states(data, hidden_states, stock)

    # Step 4: Analyze the transition matrix
    analyze_transition_matrix(model)

    # Step 5: Output the means and variances of the hidden states
    print("\nMeans and variances of each hidden state:")
    for i in range(model.n_components):
        print(f"Hidden State {i}: Mean = {model.means_[i][0]:.5f}, Variance = {np.diag(model.covars_[i])[0]:.5f}")

if __name__ == "__main__":
    main()
