# MiRh

**MiRh** is a living collection of mathematical knowledge translated into algorithms and computer graphics. What began as a simple project for convolution and image processing in Python has evolved into a broader repository of experiments, drafts, and working solutions that reflect my journey in computational mathematics and graphics.

## ✨ Project Philosophy

This project is not just a showcase of what works, but also a record of what didn’t—every attempt, whether successful or not, has value as part of the learning process. The structure is divided into sections, each containing both working algorithms and drafts or experiments that may not have found a clear purpose yet, but still represent meaningful steps in my development.

## 📁 Structure

- **convolucao/**: Convolution, heat simulation, and related numerical methods
- **deconvolucao/**: Blind deconvolution and Sylvester matrix experiments
- **computacao_grafica/**: Computer graphics, 3D engines, and surface rendering
- **Computer Vision/**: (local only) Computer vision experiments and drafts
- **src/**: Main scripts and utilities
- **examples/**, **exemplos/**: Input and output images, results

## 🚀 Features

- Numerical simulations (heat, diffusion, etc.)
- Image processing and restoration
- Computer graphics and 3D rendering
- Drafts, failed attempts, and experimental code

## 🛠️ Technologies

- Python, NumPy, SciPy, Matplotlib, Pillow

## 📚 Motivation & Evolution

As I advanced in my studies, this project grew with me. It is a reflection of my evolving understanding of mathematics, algorithms, and computer graphics. Every script, even those without a clear purpose, is a part of my journey and has its own value.

---

## 📖 Project Motivation & Evolution

This project started as an attempt to solve the heat equation in a 2D space using computational methods. Initially, loops were used, but as an optimization exercise, the calculations were later converted to matrix operations. However, in some cases, the solution became unstable.

At this point, my advisor, Ralph, explained to me that what I had just implemented was equivalent to applying a convolution with a specific kernel on a matrix representing the 2D space. He also introduced me to the **Von Neumann stability condition** and the **Crank-Nicholson method**, developed by John Crank and Phyllis Nicolson, which solves this differential equation in an implicit and stable way.

However, the book I was referencing (**EDP - Um curso de Graduação** by Valeria Iório) described the algorithm in one dimension. Extending it to two dimensions would lead to an exponential growth in the matrix size that needed to be solved, even when using sparse matrix techniques.

That's when I thought of a solution that would break the problem into alternating directional steps. After some research, I discovered the **Alternating Direction Implicit (ADI) method**, which is not only implicit (thus stable) but also takes advantage of sparse matrices to optimize the solution of the Sylvester matrix equation **(AX + XB = C)**.
