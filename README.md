# Analysing heat distributions in 2D homogenous materials 
Analysing temperature profiles of complex 2D shapes with defined temperature on the boundaries (Dirichlet boundary conditions) and homogeneous diffusivity ('rate of spread of heat').

## Background 

The 2 dimensional heat equation is given as\
$$\frac{\partial T}{\partial t} = C \left( \frac{\partial T^2}{\partial^2 x} + \frac{\partial T^2}{\partial^2 y} \right) $$
Which, when solved with the finite difference method, yield the values of `T` at `(x,y)` as



