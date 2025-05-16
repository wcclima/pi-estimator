# Estimating $\pi$ with the Monte Carlo method

## 1 - Objective

This is a simple, popular application of the Monte Carlo method to estimate the value of the mathematical constant $\pi$. It is purely pedagogical in purpose and serves as a visual aid to see the method in action.

The modulo `pi_estimator` produces a estimate for the value of the constant $\pi$, as well as animations of how the estimation evolves as the number of samples used in the method increases and a depiction of the sampling.



## 2 - Repo organisation

**`pi_estimator/`: The $\pi$ estimator modules**
It contains the $\pi$ estimator module. See also Module architecture below.

**`pictures/:` Pictures produced by the module**
- `EstimationPi.gif`
- `MonteCarloPi.gif` 


## 3 - Module architecture

Description of the `pi_estimator` module architecture.

- `pi_estimator/__init__.py`
  - Initialises the module
  - Imports the PiEstmator class
  
- `pi_estimator/pi_estimator.py`: defines the `PiEstimator` class with the methods
  - `estimate`;
  - `plot_estimation`; 
  - `animate_sampling`;
  - `results`.
  
## 4 - Features

- The `PiEstimator` class:
  - estimates the value of the mathematical constant $\pi$ using the Monte Carlo method;
  - plots and animates the evolution of the estimation as the number of samples increases;
  - animates the sampling and the evolution of the normal distribution for the estimation;
  - has the following methods:
    - `estimate` performes the estimation,
    - `plot_estimation` plots the estimation versus the number of samples,
    - `animate_sampling` animates the sampling (only available for 2-d simulations),
    - `results` returns the final estimation and the confidence interval at 95% confidence level.

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

 - **2-d Simulation**


- **3-d Simulation**


## 7 - Bibliography

1. N. J. Giordano and H Nakanishi, *Computational Physics* (Pearson Prentice Hall, New Jersey, 2006).
2. R.H. Landau, M.J. Páez and C.C. Bordeianu, *Computation Physics: Problem Solving with Python* (Wiley-VCH, Weinheim, 2015).
