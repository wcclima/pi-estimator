import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.gridspec as gridspec
import seaborn as sns
from scipy.special import erfinv
from scipy.stats import norm
from math import factorial
from prettytable import PrettyTable


__all__ = ["PiEstimator"]

class PiEstimator(object):
    """
    Estimates the value of the number Pi using the Monte Carlo method.

    PiEstimator computes the number Pi by sampling points in n-dimensional
    Euclidean space and using them to estimate the volume of n-sphere of
    radius 1.

    Attributes:
        n_dimensions (int, default = 2): 
            The number dimensions of the space.
        
        n_samples (int): 
            The number of random points 
        
        pi (np.ndarray): array of shape (n_samples,).
            The estimate value of Pi at each draw.

        error (np.ndarray): array of shape (n_samples,).
            The confidence interval @ 95% confidence level
            at each draw.
        
        samples (np.ndarray): array of shape (n_samples, n_dimensions + 1).
            It stores the x_1, ..., x_n_dim coordinates of the sample points in
            the first n_dimensions columns. The last column is a bool leable 
            where True means the point is inside the n-sphere.

            
    Methods:

        estimate(n_samples, n_dimensions):    
            Estimate the value of Pi using Monte Carlo sampling in n-dimensional space.

        plot_estimation(save_as_animation):
            Produces and saves a plot of the estimation of Pi versus the number of drwaings
            to display the convergence of the estimation. If save_as_animation = True, the method
            saves the plot as a gif showing the evolution of the convergence.


        animate_sampling():
            Produces and saves an animation of the evolution of the drawing of points used in
            the estimation and the evolution of the confidence interval. This method is only
            available when the estimation is done in 2 dimensions.

        results():
            Generate a summary table of the final area estimation results.

    """

    def __init__(self):
        """
        Initialises the EstimatePi class.

        """
        self.n_dimensions = None
        self.n_samples = None
        self.pi = None
        self.error = None
        self.samples = None


    def _1st2_sign_figs(self, number):
        """
        Returns the position of the first two significan figures of a real number.

        Keyword arguments:
            number (float):
                The {x/y}-coordinate of the polygon vertices.


        Returns: 
            i (int): 
                The index of the second significant fgure in number.
        """

        for i, elem in enumerate(str(number)):
            if elem not in ['0', '.']:
                break

        return i
    

    def _animate_estimate(
            self, 
            frame, 
            plot
            ):
        """
        Animation update function for visualizing the estimation plot at each frame.

        Keyword arguments:
            frame (int):
                The frame currently being updated.

            plot: list of matplotlib.lines.Line2D
                 A list of Line2D objects (as returned by `ax.plot(...)`) 
                 to be updated in each animation frame.

        """

        plot.set_data(np.linspace(1, frame, frame), self.pi[:frame])

    
    def _animate_sampling(self, frame, suptitle, x, ax, data, dist_plot, scatter_plot, shade_plot):
        """
        Animation update function for visualizing sampling and distribution estimation.

        This function is intended to be used with `matplotlib.animation.FuncAnimation`. 
        It updates the plot elements for a given frame, including:
        - the scatterplot of new points,
        - the estimated probability distribution,
        - and the shaded confidence interval region.

        Keyword arguments:
        
            frame (int):
                The current frame number in the animation.

            suptitle (matplotlib.text.Text):
                The suptitle text object to update with the current frame count.

            x (np.ndarray): array-like of shape (400,)
                The x-axis values for plotting the estimated distribution.

            ax (matplotlib.axes.Axes)
                The axes object where the scatter plot is drawn.

            dist_plot (matplotlib.lines.Line2D):
                Line2D object representing the estimated distribution curve to be updated.
            
            scatter_plot (list of matplotlib.collections.PathCollection):
                The current scatter plot artists to be updated with new sample points.
            
            shade_plot (matplotlib.patches.Polygon):
                Polygon object representing the shaded area under the confidence interval.

        """

        suptitle.set_text(f"{frame} throws")
        scatter_plot = sns.scatterplot(x = data[:frame,0], y = data[:frame,1], 
                        hue = data[:frame,2], style = data[:frame,2], 
                        color = ['green', 'red'], legend = False, 
                        palette = {True: 'green', False: 'red'}, 
                        markers = {True: 'o', False: 'o'}, s = 8, 
                        linewidth=0.1, ax = ax
                    )
        
        y_new = norm.pdf(x, self.pi[frame], 1 / np.sqrt(4*frame)) / np.sqrt(4*frame)
        dist_plot.set_ydata(y_new)

        new_xmin = self.pi[frame] - self.error[frame]
        new_xmax = self.pi[frame] + self.error[frame]

        new_vertices = [
            [new_xmin, 0.],
            [new_xmin, 1.],
            [new_xmax, 1.],
            [new_xmax, 0.],
            [new_xmin, 0.]
        ]
        shade_plot.set_xy(new_vertices)


    def _frames(self):
        """
        Generate a list of frame indices for use in matplotlib.animation.FuncAnimation.

        This method determines which sample indices should be used as frames in the animation,
        based on the total number of samples (`self.n_samples`). It adapts the frame frequency 
        according to the sample size.

        Returns:
            list[int]: A list of integer frame indices to be used for animation.
        
        Frame selection logic:
            - For n_samples ≤ 100: include all frames starting from 2.
            - For 100 < n_samples ≤ 1000: include all from 2 to 99, then every 25th sample.
            - For 1000 < n_samples ≤ 10000: include early frames densely (2–99), 
            then every 25th up to 1000, and every 50th up to n_samples.
            - For n_samples > 10000: similar strategy, with added every 100th frame beyond 10000.

        """
        
        if self.n_samples <= 100:
            frame_list = [i for i in range(2, self.n_samples)]
            
        elif (self.n_samples > 100)&(self.n_samples <= 1000):
            frame_list = [i for i in range(2, 100)]
            frame_list += [i for i in range(100, self.n_samples, 25)]

        elif (self.n_samples > 1000)&(self.n_samples <= 10000):
            frame_list = [i for i in range(2, 100)]
            frame_list += [i for i in range(100, 1000, 25)]
            frame_list += [i for i in range(1000, self.n_samples, 50)]

        elif (self.n_samples > 10000):
            frame_list = [i for i in range(2, 100)]
            frame_list += [i for i in range(100, 1000, 25)]
            frame_list += [i for i in range(1000, 10000, 50)]
            frame_list += [i for i in range(10000, self.n_samples, 100)]

        return frame_list
    

    def _random_projection(self, seed=42):
        """
        Projects high-dimensional data with labels to 2D using a random linear projection.

        Keyword arguments:
            points_with_label: np.ndarray of shape (n_samples, n_dimensions + 1)
                The last column is a boolean indicating whether the point is inside the n-sphere.

        Returns:
            proj_points: np.ndarray of shape (n_samples, 3)
        """
        np.random.seed(seed)
        points = self.samples[:, :self.n_dimensions]
        labels = self.samples[:, -1]

        # Create a random projection matrix: shape (n_dims, 2)
        random_matrix = np.random.randn(self.n_dimensions, 2)
        random_matrix /= np.linalg.norm(random_matrix, axis=0)  # normalize columns

        v0, v1 = random_matrix[:,0].reshape(1, -1), random_matrix[:,1].reshape(1, -1)
        cos_gamma = (v0*v1).sum()
        v1 = (v1 - cos_gamma*v0)/np.sqrt(1 - cos_gamma**2)
        random_matrix[:, 1] = v1        

        # Project to 2D
        proj_points = points @ random_matrix

        proj_points = np.hstack((proj_points, labels.reshape(-1,1)))

        return proj_points


    def estimate(self, n_samples, n_dimensions = 2):
        """
        Estimate the value of Pi using Monte Carlo sampling in n-dimensional space.

        This method generates `n_samples` uniformly random points within the n-dimensional 
        cube [-1, 1]^n and determines the fraction that fall inside the n-dimensional 
        unit hypersphere. The method also computes an error estimate and prints a summary 
        table of the results.

        Keyword arguments:
        
        n_samples (int):
            The number of samples to draw.
        n_dimensions (int, default=2):
            The number of dimensions to perform the estimation in. Must be ≥ 1.


        Notes:

        - The final Pi estimate is rounded to the first two significant figures of the error.
        """

        self.n_dimensions = n_dimensions
        self.n_samples = n_samples

        v = 2.*np.random.rand(self.n_samples, self.n_dimensions) - 1.
        self.samples = np.hstack((v, ((v**2).sum(axis=1) <= 1.).reshape(-1,1)))

        if self.n_dimensions % 2:
            k = int((self.n_dimensions - 1)/2)
            f = 2.**self.n_dimensions*factorial(2*k + 1)/(2.*factorial(k))
            self.pi = 1/4.*(f*self.samples[:,self.n_dimensions].cumsum()/np.ones(self.n_samples).cumsum())**(1/k)

        else:
            k = int(self.n_dimensions/2)
            f = 2.**self.n_dimensions*factorial(k)
            self.pi = (f*self.samples[:,self.n_dimensions].cumsum()/np.ones(self.n_samples).cumsum())**(1/k)    

        self.error = erfinv(0.95)/np.sqrt(4.*np.ones(n_samples).cumsum())


    def results(self):
        """
        Generate a summary table of the final Pi estimation results.

        This method compiles and returns a PrettyTable summarizing key information from the 
        Monte Carlo Pi estimation performed in n dimensions. It includes the number of dimensions, 
        number of samples, the most recent estimate of Pi, and the corresponding 95% confidence interval.

        Returns
        -------
        PrettyTable
            A formatted summary table containing:
                - Dimension of the space
                - Number of samples used
                - Final estimate of Pi
                - 95% confidence interval around the estimate

        Notes
        -----
        This method assumes that the `estimate` method has already been called.
        """

        error_message = "Estimation has not been performed. Please call `estimate` before `results`."
        if self.pi is None or self.error is None:
            raise ValueError(error_message)

        sig_figs = self._1st2_sign_figs(self.error[-1])

        estimation_table = PrettyTable(["quantity", "value"])
        estimation_table.add_row(["dimension", self.n_dimensions])
        estimation_table.add_row(["samples", self.n_samples])
        estimation_table.add_row([f"samples in {self.n_dimensions}-sphere", int(self.samples[:,self.n_dimensions].sum())])
        estimation_table.add_row(["π", np.round(self.pi[-1], sig_figs)])
        estimation_table.add_row(["conf. interval @95%", f'[{np.round(self.pi[-1] - self.error[-1], sig_figs)}, {np.round(self.pi[-1] + self.error[-1], sig_figs)}]'])

        return estimation_table



    def plot_estimation(self, save_as_animation = False, file_name = 'EstimationPi.gif'):
        """
        Visualize the convergence of the Monte Carlo estimate of Pi with respect to sample size.

        This method creates a line plot showing the estimated value of Pi versus the number of Monte Carlo samples.
        It optionally generates and saves an animated GIF that illustrates how the estimate converges over time.

        Keyword arguments:
        
        save_as_animation (bool, default=False):
            If True, generates and saves an animated GIF named 'EstimationPi.gif' that shows the evolution of the π estimate
            over increasing sample sizes. If False, a static plot is shown instead.

        file_name (str, default = 'EstimationPi.gif'):
            The name of the exit file for the animated plot.

        Returns: None
            Displays a matplotlib plot or saves an animated GIF showing the estimation process.

        Notes
        
        - The static plot includes a dashed horizontal line representing the true value of Pi.
        - The animated version reveals the progressive convergence of the estimate to Pi as sample size increases.
        - The saved GIF is named 'EstimationPi.gif' and uses PillowWriter for animation output.
        """

        error_message = "Estimation has not been performed. Please call `estimate` before `plot_estimation`."
        if self.pi is None or self.error is None:
            raise ValueError(error_message)

        plt.figure(figsize=(8,5))
        plt.plot(np.linspace(1,self.n_samples,self.n_samples),self.pi)
        plt.title(f'Estimated $\\pi$ vs. number of samples in {self.n_dimensions}-d')
        plt.hlines(y=np.pi, xmin=1, xmax=self.n_samples, linestyles= '--', colors = 'black', label = r'Real $\pi$')
        plt.xlabel('Number of samples')
        plt.ylabel(r'Estimated $\pi$')
        plt.legend()
        plt.xlim((-0.04*self.n_samples, 1.04*self.n_samples))
        plt.ylim((self.pi.min() - 0.5, self.pi.max() + 0.5))
        plt.show()

        if save_as_animation:
            fig, ax = plt.subplots(figsize=(8,5))
            fig.suptitle(f'Estimated $\\pi$ vs. number of samples in {self.n_dimensions}-d')
            est_plot = ax.plot(np.linspace(1,1,1),self.pi[:1])
            ax.hlines(y=np.pi, xmin=1, xmax=self.n_samples, linestyles= '--', colors = 'black', label = r'Real $\pi$')
            ax.set_xlabel('Number of samples')
            ax.set_ylabel(r'Estimated $\pi$')
            ax.set_xlim((-0.04*self.n_samples, 1.04*self.n_samples))
            ax.set_ylim((self.pi.min() - 0.5, self.pi.max() + 0.5))
            ax.legend()

            frm = self._frames()

            ani = animation.FuncAnimation(fig, self._animate_estimate, frames=frm, fargs=(est_plot), repeat=False)

            writer = animation.PillowWriter(fps=int(250/15.))
            ani.save(file_name, writer=writer)
            plt.close()


    def animate_sampling(self, file_name = 'MonteCarloPi.gif'):
        """
        Animate the Monte Carlo sampling process used to estimate Pi in 2D space.

        This method creates and saves an animated GIF illustrating the convergence of the Pi estimate using
        Monte Carlo sampling in two dimensions. The animation consists of two subplots:

        - Left: A scatter plot showing sampled points within the square [-1, 1] x [-1, 1], with points inside
        the unit circle highlighted in green and those outside in red.
        - Right: A probability density function (PDF) plot of the estimated value of Pi, updated over time,
        with a shaded region indicating the 95% confidence interval.

        The animation demonstrates how the Pi estimate stabilizes as the number of samples increases.

        Keyword arguments:
            file_name (str, default = 'MonteCarloPi.gif'):
                The name of the exit file for the animated plot.

        Returns: None
            Saves an animated GIF named 'MonteCarloPi.gif'.

        Notes:
        
        - This method only supports 2-dimensional estimation. If called with n_dimensions ≠ 2,
        a message will be printed and no animation will be created.
        """

        error_message = "Estimation has not been performed. Please call `estimate` before `animate_sampling`."
        if self.pi is None or self.error is None:
            raise ValueError(error_message)
        

        if self.n_dimensions == 2:
            sample_points = self.samples

        else:
            sample_points = self._random_projection()


        x = np.linspace(0.,4., 400)
        theta = np.linspace(0.,2.*np.pi,100).reshape(-1,1)
        circle = np.hstack((np.cos(theta), np.sin(theta)))
                
        fig = plt.figure(figsize=(12, 3.6))  # total figure size
        gs = gridspec.GridSpec(1, 2, width_ratios=[1, 2])  # custom ratios

        suptitle = fig.suptitle("1 throw", fontsize=16)

        # Make a square plot (1x1 block)
        ax1 = fig.add_subplot(gs[0, 0])  # top-left
        ax1.set_aspect('equal')  # force square
                
        # 1st frame
        scatter = sns.scatterplot(x = sample_points[:1,0], y = sample_points[:1,1], 
                        hue = sample_points[:1,2], style = sample_points[:1,2], 
                        color = ['green', 'red'], legend = False, 
                        palette = {True: 'green', False: 'red'}, 
                        markers = {True: 'o', False: 'o'}, s = 8, 
                        linewidth=0.1, ax = ax1
                    )
        ax1.set_xlim((-1.,1))
        ax1.set_ylim((-1.,1))
        ax1.set_xticks([-1., 0., 1.])
        ax1.set_yticks([-1., 0., 1.])
        ax1.set_xlabel('Samples')
        ax1.plot(circle[:,0], circle[:, 1], color='black')
                
        # Make a rectangular plot (2x1 block)
        ax2 = fig.add_subplot(gs[:, 1])  # right column (span rows)
                
        dist_plot, = ax2.plot(x, norm.pdf(x,self.pi[1],1/np.sqrt(4))/np.sqrt(4))
        ax2.vlines(x=np.pi, ymin=0., ymax=.5,linestyles='--', colors = 'black', label = r'Real $\pi$')
        shade_plot = ax2.axvspan(self.pi[1] - self.error[1], self.pi[1] + self.error[1], alpha=0.2, facecolor='red', label = '95% Confidence Level')
        ax2.set_xlim((0.,4.))
        ax2.set_ylim(0.,0.5)
        ax2.set_xticks([0., 1., 2., 3., 4.])
        ax2.set_yticks([])
        ax2.set_xlabel(r'Estimated $\pi$')
        ax2.legend(loc='upper left')
                
        plt.tight_layout()

        frm = self._frames()

        ani = animation.FuncAnimation(
            fig, 
            self._animate_sampling, 
            frames=frm, 
            fargs=(suptitle, x, ax1, sample_points, dist_plot, scatter, shade_plot), 
            repeat=False
            )

        writer = animation.PillowWriter(fps=int(250/30.))
        ani.save(file_name, writer=writer)
        plt.close()
