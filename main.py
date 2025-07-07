import os
import time
import argparse
from pathlib import Path
from simulation.adi_simulation import ADIHeatSimulation
from image_processing import ImageProcessor
from sylvester_resultant.applications import ImageProcessingApplications

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
    parser.add_argument('--adi-bid', action='store_true', help='Run ADI blur and BID deconvolution example')
    parser.add_argument('--bid-on-adi', action='store_true', help='Run BID on cameraman_ADI.png')
    return parser.parse_args()

def main():
    parser = argparse.ArgumentParser(description='Image Processing Experiments')
    parser.add_argument('--adi-bid', action='store_true', help='Run ADI blur and BID deconvolution example')
    parser.add_argument('--bid-on-adi', action='store_true', help='Run BID on cameraman_ADI.png')
    args = parser.parse_args()

    if args.adi_bid:
        ImageProcessingApplications.adi_blur_and_bid_example()
    elif args.bid_on_adi:
        ImageProcessingApplications.bid_on_adi_blurred_image()
    else:
        print('No action specified. Use --adi-bid or --bid-on-adi.')

if __name__ == '__main__':
    main()
