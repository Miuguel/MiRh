import os
import time
import argparse
from pathlib import Path
from simulation.adi_simulation import ADIHeatSimulation
from image_processing import ImageProcessor

def parse_args():
    parser = argparse.ArgumentParser(description='Heat simulation on images using ADI method')
    parser.add_argument('--input', type=str, required=True,
                      help='Path to input image')
    parser.add_argument('--output', type=str, required=True,
                      help='Path to save output image')
    parser.add_argument('--dt', type=float, default=0.2,
                      help='Time step for simulation')
    parser.add_argument('--iterations', type=int, nargs=3, default=[0, 0, 100],
                      help='Number of iterations for R,G,B channels')
    return parser.parse_args()

def main():
    args = parse_args()
    
    # Initialize simulation and image processor
    simulator = ADIHeatSimulation(dt=args.dt)
    processor = ImageProcessor()
    
    # Load image
    print(f"Loading image from {args.input}")
    r, g, b = processor.load_image(args.input)
    
    # Process channels
    print("Running simulation...")
    start_time = time.time()
    
    processed_channels = processor.process_channels(
        channels=[r, g, b],
        simulation_func=simulator.simulate,
        num_iterations=args.iterations
    )
    
    elapsed_time = time.time() - start_time
    print(f"Simulation completed in {elapsed_time:.4f} seconds")
    
    # Combine and save result
    print(f"Saving result to {args.output}")
    result = processor.combine_channels(*processed_channels)
    processor.save_image(result, args.output)
    print("Done!")

if __name__ == '__main__':
    main()
