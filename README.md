# Toy Data Sets for Seminar on Manifold Learning

LMU, Winter Semester 2020/2021

# Datasets

## Clocks

Dataset consisting of a set of circles (_clocks_) with clock hands varying clockwise. A perfect model is able to learn the 2-dimensional manifold and embed the clocks according to the clockwise ordering.

Images look as follows:

![circle 0](circle_clockh_0.png)
![circle 1](circle_clockh_1.png)
![circle 2](circle_clockh_2.png)
![circle 3](circle_clockh_3.png)

Use the script `circle_2d.py` to generate them. You can play around with various command line args such as `nrows=127`, height and width of the image, `n=20` the amount of plots to create and `delta=150` to control the thickness of the clock hands. Running the script will create a folder `circle_plots` that contains a) the plots for each of the circles and b) a `rawdata_circles.csv` containing the rawdata as flattened vectors.

As label `y` we use the angle of the clock hand w.r.t to a reference clock hand at 9'o clock.

## Swiss Roll

**The** standard data set for manifold learning problems. The task is to embedd a 3-dimensional, convolved dataset in a smaller embedding space. We can control parameters `n=1000` and `noise=0.0`. The input data looks as follows:

!['swiss roll'](swiss_roll.png)

As label `y` we use the position according to the main dimension of each point on this manifold.

## ??

# Code

## Data Generation

## Evaluation the Manifold
