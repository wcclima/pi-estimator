# Estimating $\pi$ with the Monte Carlo method

## 1 - Objective

This is a simple, popular application of the Monte Carlo method to estimate the value of the mathematical constant $\pi$. It is purely pedagogical in purpose and serves as a visual aid to see the method in action.

The modulo `pi_estimator` generates an estimate for the value of the constant $\pi$, as well as animations of how the estimation evolves as the number of samples used in the method increases and of the sampling procedure.



## 2 - Repo organisation

**`pi_estimator/`: The $\pi$ estimator modules**
It contains the $\pi$ estimator module. See also Module architecture below.

**`pictures/:` Pictures produced by the module**
- `EstimationPi2D.gif`
- `MonteCarloPi2D.gif` 


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
    - `results` returns the number of dimensions and samples used, the final estimation and the confidence interval at 95% confidence level.
   
  Note: the confidence interval is computed using the maximum of the Bernoulli's distribution variance (i.e. $\sigma = 1/2$, the "pessimistic approach"). Thus, the sample error is simply given by $1.96/(2\times \sqrt{N_{\rm samples}})$.

## 5 - The Monte Carlo method

The Monte Carlo method is a popular statistical tool employed in may fields to perform simulations. In summary, the idea of the method is that we have a quantity of interest that can be expressed as a parameter characterizing some statistical population. The method works then creating artificial samples of that population and using the sample to estimate the parameter.

The estimation of $\pi$ is a fun application of the Monte Carlo method, as it provides a very visual and intuitive way to see it in action. The reason is that the constant $\pi$ has a very direct geometrical interpretation: it is the area of a circle with radius 1. Thus, consider the circle of radius 1 inscribed in a square of side 2. Taking our statistical population as the points inside the square, the area of the inscribed circle is proportional to $p$, the fraction of points inside the circle. Hence, in this case, finding a estimative for $\pi$ is equivalent to finding an estimative $\hat{p}$ for the populational proportion of the points inside the circle. 

Producing samples to that popuplation then becomes as easy as randomly throwing independent imaginary darts to a board, hitting the board at points $P = (x, y)$. The coordinates $x,\ y$ are independent, uniformely distributuded random variables in the range $[-1, 1]$ (as the center of the circle is at the origin). The darts hit the circle when they land at points satisfying $x^2 + y^2 \le 1$. The estimative for the population propotion is then simply given by

$$
\hat{p} = \frac{\text{number of throws in the circle}}{\text{number of throws}}.
$$

The estimative $\hat{\pi}$ for the constant $\pi$ is given by

$$
\hat{\pi} = A_{\rm square}\times \hat{p}.
$$

## 6 - Results

Here we present estimations of $\pi$ in 2- and 10-dimensional spaces, so we can compare the convergence of the estimative.

It is clear from Figures 1 and 3 that the convergence is better in lower dimensions. The reason is the so-called "curse of dimensionality": the fact that as the number of dimensions increase, the volume of the n-sphere inscribed in the n-cube lowers with respect to the volume total volume of the n-cube. Hence we need to throw more darts to be able sample the the n-sphere with the same accuracy as the number of dimensions increases.

 - **2-d Simulation**

<div align="center">
  
|       quantity      |      value       |
|:-------------------:|:----------------:|
|      dimension      |        2         |
|       samples       |       6000       |
|          π          |      3.1493      |
| conf. interval @95% | [3.1404, 3.1583] |

*Table 1: Results in 2 dimensions.*

</div>
<br><br>

<div align="center">

![plot](https://github.com/wcclima/pi-estimator/blob/main/pictures/EstimationPi2D.gif)
  
*Figure 1: Estimative for Pi in 2-d using a total of 6000 samples.*

</div>
<br><br>

![plot](https://github.com/wcclima/pi-estimator/blob/main/pictures/MonteCarloPi2D.gif)
<div align="center">
  
*Figure 2: (On the left) Sampling of points within a square of side 2 with a inscribe circle of radius 1. (On the right) Normal distribution for the estimative and the corresponding confidence interval at 95% confidence level.*

</div>
<br><br>


- **10-d Simulation**

<div align="center">
  
|       quantity      |      value      |
|:-------------------:|:---------------:|
|      dimension      |        10       |
|       samples       |       6000      |
|          π          |      2.9549     |
| conf. interval @95% | [2.946, 2.9639] |

*Table 2: Results in 10 dimensions.*

</div>
<br><br>


<div align="center">
  
![plot](https://github.com/wcclima/pi-estimator/blob/main/pictures/EstimationPi10D.gif)
  
*Figure 3: Estimative for Pi in 10-d using a total of 6000 samples.*

</div>
<br><br>


## 7 - Bibliography

1. N. J. Giordano and H Nakanishi, *Computational Physics* (Pearson Prentice Hall, New Jersey, 2006).
2. R.H. Landau, M.J. Páez and C.C. Bordeianu, *Computation Physics: Problem Solving with Python* (Wiley-VCH, Weinheim, 2015).
