# Estimating $\pi$ with the Monte Carlo method

## 1 - Objective

This is a simple, popular application of the Monte Carlo method to estimate the value of the mathematical constant $\pi$. It is purely pedagogical in purpose and serves as a visual aid to see the method in action.

The modulo `pi_estimator` produces a estimate for the value of the constant $\pi$, as well as animations of how the estimation evolves as the number of samples used in the method increases and a depiction of the sampling.

## 2 - Repo structure

## 3 - Module architecture

## 4 - Features

## 5 - The Monte Carlo method

The Monte Carlo method is a statistical method employed in may fields to perform simulations. In summary, the idea of the method is that we have a quantity of interest that can be expressed as a parameter characterizing some statistical population. The method works then to creating artificial samples of that population and using the sample to estimate that parameter.

The estimation of $\pi$ is a fun application of the Monte Carlo method, as it provides a very visual and intuitive way to see it in action. The constant $\pi$ has a very direct geometrical interpretation: it is the area of a circle with radius 1. Let us consider, then, the circle of radius 1 inscribed in a square of side 2. Taking our statistical population as the points inside the square, the area of the inscribed circle is proportional to $p$, the fraction of points inside the circle. Hence, in this case, finding a estimative for $\pi$ is equivalent to finding an estimative $\hat{p}$ for the populational proportion of the points inside the circle. Producing samples to that popuplation becomes as easy as randomly throwing imaginary darts to a board, and the estimative for the population propotion is simply given by

$$
\hat{p} = \frac{\text{number of throws in the circle}}{\text{number of throws}}.
$$

The estimative $\hat{\pi}$ for the constant $\pi$ is given by

$$
\hat{\pi} = A_{\rm square}\times \hat{p}.
$$


## 6 - Results

## 7 - Bibliography
