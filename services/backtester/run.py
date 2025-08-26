"""
Backtester runner (placeholder).  Parses CLI arguments and runs simulations
using historical data.  Use the design document for guidance on
implementation details.
"""

import argparse


def main():
    parser = argparse.ArgumentParser(description="Run backtests for a strategy")
    parser.add_argument("--strategy", required=True)
    parser.add_argument("--symbol", required=True)
    parser.add_argument("--start", required=True)
    parser.add_argument("--end", required=True)
    args = parser.parse_args()
    print(f"Backtesting {args.strategy} on {args.symbol} from {args.start} to {args.end}")
    # TODO: load data, run simulation, output results


if __name__ == "__main__":
    main()