# MiRh: Deconvolution and Heat Simulation Algorithms

## Description
This project implements heat simulation (ADI) and blind image deconvolution (BID) algorithms, based on scientific papers, including the use of the Sylvester resultant matrix. The goal is to study and demonstrate image processing and restoration techniques.

- Image blurring using the ADI (Alternating Direction Implicit) method
- Blind Image Deconvolution (BID) based on Sylvester
- Examples with classic images (e.g., cameraman)

---

## Installation

1. Clone the repository:
   ```bash
   git clone <repo-url>
   cd MiRh
   ```
2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # or 'Scripts/activate' on Windows
   pip install -r requirements.txt
   ```





---

## Project Structure

- `src/` — Main code
- `old/` — Old or reference code
- `examples/` — Input and output images
- `requirements.txt` — Dependencies

---

## Algorithms
- **ADI:** Heat simulation for image blurring
- **BID:** Blind deconvolution based on Sylvester matrix

Main references:
- Winkler, The Sylvester resultant matrix and image
- Other papers cited in the code

---

## License
See the LICENSE file.