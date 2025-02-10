# MiRh

**MiRh** is an experimental project that explores the application of numerical methods to simulate differential equations, specifically focusing on heat distribution in a 2D plate. The main idea is to use calculus concepts, such as differential equations and approximation methods, to create interactive visual representations, simulating physical phenomena using colors.

## 🧮 Objective

The goal of **MiRh** is to learn various numerical and programming concepts while demonstrating the versatility of numerical methods in solving complex problems. The primary application explored so far involves simulating heat propagation in images, represented by color changes.

## 🚀 Features

- Simulations based on numerical methods.
- Graphical representation of value propagation (such as heat) over a pixel matrix.
- Conversion of numerical results into visual transformations, using colors to represent different states.

## 📂 Project Structure

```plaintext
MiRh/
├── src/         
│   ├── adi_simulation.py          # Alternating Directions Implicit - Most optimized implicit method so far
│   ├── conv_FFT_simulation.py     # Convolution optimization using Fast Fourier Transform
│   ├── conv_simulation.py         # Differential equation solving using convolution and kernel
│   ├── heat_simulation.py         # Python version of the optimized MATLAB simulation
│   ├── heat_spread_sim_otim.m     # Optimization using matrix operations instead of loops
│   ├── heat_spread_sim.m          # Heat propagation simulation in a matrix with MATLAB
│   ├── main.py                    # Main script
│   ├── metodo_implicito.py        # Implicit methods from Valeria’s book
│   └── utils.py                    # Auxiliary functions
├── examples/
│   ├── example_image.jpg          # Sample image for simulation
│   └── heat_simulation_output.png # Simulation result
├── README.md                      # Project documentation
├── requirements.txt               # Project dependencies
└── LICENSE                        # Project license
```

## 🛠️ Technologies Used

- **Python**: Main language for calculations and simulations.
- **NumPy**: For efficient matrix operations.
- **Matplotlib**: For plotting and visualizing results.
- **Pillow (PIL)**: For image processing.

## 📦 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Miuguel/MiRh
   cd MiRh
   ```

2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## 📊 How to Use

1. Make sure you have an image in `.jpg` or `.png` format for the simulation.
2. Run the main script:
   ```bash
   python src/heat_spread_simulation.py --image examples/example_image.jpg
   ```
3. The output will be saved in the `examples/` folder, showing how "heat" spreads over the image.

## 🌟 Examples

### Original Image:
![Original Image](examples/example_image.png)

### Result:
![Result](examples/heat_simulation_output.png)

## 🧠 Next Steps

- Implement new numerical methods for other simulations.
- Add support for more physical phenomena (e.g., wave propagation).
- Improve the visual interface.
- Create an interactive panel to adjust simulation parameters.

## 🤝 Contributing

Contributions are welcome! Feel free to open issues or submit pull requests. For more details, check the `CONTRIBUTING.md` file.

## 📜 License

This project is licensed under the [MIT License](LICENSE).

---

## 📖 Project Motivation & Evolution

This project started as an attempt to solve the heat equation in a 2D space using computational methods. Initially, loops were used, but as an optimization exercise, the calculations were later converted to matrix operations. However, in some cases, the solution became unstable.

At this point, my advisor, Ralph, explained to me that what I had just implemented was equivalent to applying a convolution with a specific kernel on a matrix representing the 2D space. He also introduced me to the **Von Neumann stability condition** and the **Crank-Nicholson method**, developed by John Crank and Phyllis Nicolson, which solves this differential equation in an implicit and stable way.

However, the book I was referencing (**EDP - Um curso de Graduação** by Valeria Iório) described the algorithm in one dimension. Extending it to two dimensions would lead to an exponential growth in the matrix size that needed to be solved, even when using sparse matrix techniques.

That’s when I thought of a solution that would break the problem into alternating directional steps. After some research, I discovered the **Alternating Direction Implicit (ADI) method**, which is not only implicit (thus stable) but also takes advantage of sparse matrices to optimize the solution of the Sylvester matrix equation **(AX + XB = C)**.
```
