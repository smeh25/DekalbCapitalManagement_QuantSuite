import yfinance as yf
import pandas as pd
import numpy as np


# stocks must be a list of strings where each string is a ticker
# start and end must be strings of dates formatted as such YYYY-MM-DD
# This returns a np array as well as a pd dataframe 

def getTimeMatrix(stocks, start, end):
    X = yf.download(stocks[0], start = start, end=end)["Close"]
    for tckr in stocks[1:]:
        X = X.join(yf.download(tckr, start = start, end=end)["Close"], how="inner")

    return X.values.transpose(), X.transpose()


# normalizes stock data to mean of 0 and stdev of 1
def normalizeStockData(X):
    # Subtract mean
    X_centered = X - X.mean(axis=1, keepdims=True)

    # Divide by standard deviation
    X_std = X_centered / X_centered.std(axis=1, keepdims=True)

    return X_std

# returns m, and Shat which is the sample covariance
def getMeanAndSampleCovariance(X):
    # Note that X is N x T so each row is what we want
    m = np.mean(X, axis = 1)
    N, T = X.shape
    SHat = np.zeros((N,N))
    for i in range(len(X[0])):
        x_t = (X[:,i] - m)[:, np.newaxis] # The slice makes it a 1D array with shape (N,) so I reshaped with np.newaxis to a column vector (Nx1)
        SHat += x_t @ x_t.transpose()  # (N x 1) @ (1 x N) => N x N
    SHat /= T
    
    return m, SHat



# glasso algorithm here. It uses sklearn's lasso for the subproblem (inner loop)

from sklearn.linear_model import Lasso

def glasso(X, m, coVar, l1=0.03):
    initialization_scalar = 0.01
    conv_threshold = 1e-4
    maxIter = 100

    N = coVar.shape[0]
    W = initialization_scalar * np.eye(N) + coVar # Sparse matrix
    # W = np.eye(N)

    iter = 1
    rel_diff = conv_threshold + 1

    while ((rel_diff > conv_threshold) and (iter < maxIter)):
        W_old = W.copy()
        for i in range(N):
            W11 = np.delete(W, i, axis=0)  # remove row i
            W11 = np.delete(W11, i, axis=1)  # remove col i
            w12 = np.delete(W[:, i], i)
            s12 = np.delete(coVar[:, i], i)

            # Lasso subproblem
            lasso = Lasso(alpha=l1, fit_intercept=False, max_iter=1000)
            lasso.fit(W11, s12)
            beta = lasso.coef_

            # Update new elements of W
            w12 = W11 @ beta
            indices = np.arange(N) != i
            W[i, indices] = w12
            W[indices, i] = w12
            W[i, i] = 1.0 / (coVar[i, i] - s12 @ beta)

        # Frobenius norm to check convergence. Frobeneus norm of matrix A is sqrt(trace(A^T*A))
        diff = np.linalg.norm(W - W_old, ord='fro')
        rel_diff = diff / np.linalg.norm(W_old, ord='fro')
        iter +=1
    
    return W


# Method that brings it all together
def estimateSparseCovariance(tickers, start, end, l1=0.03, normalize=True):
    X = getTimeMatrix(stocks=tickers, start=start, end=end)[0]
    if normalize: X = normalizeStockData(X)
    m, coVar = getMeanAndSampleCovariance(X)
    return glasso(X, m, coVar, l1)
