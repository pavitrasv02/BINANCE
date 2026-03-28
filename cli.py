#!/usr/bin/env python3
"""Command-line interface for Binance Futures Trading Bot."""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import argparse
import sys
import os
from bot.logging_config import setup_logging
from bot.orders import OrderExecutor
from bot.validators import ValidationError
from binance.exceptions import BinanceAPIException, BinanceRequestException
from dotenv import load_dotenv
import os

load_dotenv()

# Setup logging
logger = setup_logging()


def get_confirmation():
    """Ask user for confirmation before placing order.
    
    Returns:
        bool: True if user confirms, False otherwise
    """
    while True:
        response = input("\nDo you want to place this order? (yes/no): ").strip().lower()
        if response in ['yes', 'y']:
            return True
        elif response in ['no', 'n']:
            return False
        else:
            print("Please enter 'yes' or 'no'")


def print_success_message(response):
    """Print success message after order execution.
    
    Args:
        response: Order response
    """
    print("\n" + "*"*60)
    print("✓ SUCCESS: Order placed successfully!".center(60))
    print("*"*60)


def print_error_message(error_msg):
    """Print error message.
    
    Args:
        error_msg: Error message to display
    """
    print("\n" + "*"*60)
    print("✗ ERROR".center(60))
    print("*"*60)
    print(f"\n{error_msg}\n")
    print("*"*60 + "\n")


def create_parser():
    """Create and configure argument parser.
    
    Returns:
        ArgumentParser: Configured argument parser
    """
    parser = argparse.ArgumentParser(
        description='Binance Futures Testnet Trading Bot',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Place a market buy order
  python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
  
  # Place a limit sell order
  python cli.py --symbol ETHUSDT --side SELL --type LIMIT --quantity 0.01 --price 2000
  
  # Using environment variables for API keys
  export BINANCE_API_KEY="your_api_key"
  export BINANCE_API_SECRET="your_api_secret"
  python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
        '''
    )
    
    parser.add_argument(
        '--symbol',
        type=str,
        required=True,
        help='Trading pair symbol (e.g., BTCUSDT, ETHUSDT)'
    )
    
    parser.add_argument(
        '--side',
        type=str,
        required=True,
        choices=['BUY', 'SELL', 'buy', 'sell'],
        help='Order side: BUY or SELL'
    )
    
    parser.add_argument(
        '--type',
        type=str,
        required=True,
        choices=['MARKET', 'LIMIT', 'market', 'limit'],
        help='Order type: MARKET or LIMIT'
    )
    
    parser.add_argument(
        '--quantity',
        type=float,
        required=True,
        help='Order quantity (must be greater than 0)'
    )
    
    parser.add_argument(
        '--price',
        type=float,
        default=None,
        help='Order price (required for LIMIT orders)'
    )
    
    parser.add_argument(
        '--api-key',
        type=str,
        default=None,
        help='Binance API key (or set BINANCE_API_KEY environment variable)'
    )
    
    parser.add_argument(
        '--api-secret',
        type=str,
        default=None,
        help='Binance API secret (or set BINANCE_API_SECRET environment variable)'
    )
    
    return parser


def get_api_credentials(args):
    """Get API credentials from arguments or environment variables.
    
    Args:
        args: Parsed command-line arguments
        
    Returns:
        tuple: (api_key, api_secret)
        
    Raises:
        ValueError: If credentials are not provided
    """
    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")
    
    if not api_key or not api_secret:
        raise ValueError(
            "API credentials not provided.\n"
            "Please provide credentials using one of these methods:\n"
            "  1. Command-line arguments: --api-key <key> --api-secret <secret>\n"
            "  2. Environment variables: BINANCE_API_KEY and BINANCE_API_SECRET"
        )
    
    return api_key, api_secret


def main():
    """Main entry point for the CLI."""
    parser = create_parser()
    args = parser.parse_args()
    
    try:
        # Get API credentials
        api_key, api_secret = get_api_credentials(args)
        
        # Initialize order executor
        executor = OrderExecutor(api_key, api_secret)
        
        # Test the connection with a simple API call
        try:
            logger.info("Testing API connection...")
            test_price = executor.client.get_price(args.symbol)
            logger.info(f"[OK] API connection successful. Current {args.symbol} price: {test_price}")
        except Exception as test_error:
            logger.warning(f"[WARN] Could not fetch price for connection test: {str(test_error)}")
            logger.warning("This may indicate invalid credentials or testnet server issues")
        
        # Validate parameters and prepare order (this will print the order request)
        logger.info("Starting order execution process")
        
        # For MARKET orders, fetch current price to validate notional value
        current_price = None
        if args.type.upper() == 'MARKET':
            try:
                current_price = executor.client.get_price(args.symbol)
                logger.info(f"Current price for {args.symbol}: {current_price}")
            except Exception as price_error:
                logger.error(f"Could not fetch current price: {str(price_error)}")
                raise
        
        # Validate all parameters first
        from bot.validators import validate_order_params
        validated_params = validate_order_params(
            symbol=args.symbol,
            side=args.side,
            order_type=args.type,
            quantity=args.quantity,
            price=args.price,
            current_price=current_price
        )
        
        # Print order request for user review
        executor.print_order_request(validated_params)
        
        # Get confirmation from user BEFORE placing order
        if not get_confirmation():
            print("\nOrder cancelled by user.")
            logger.info("Order cancelled by user")
            sys.exit(0)
        
        # Place the order after confirmation
        response = executor.client.create_order(
            symbol=validated_params['symbol'],
            side=validated_params['side'],
            order_type=validated_params['type'],
            quantity=validated_params['quantity'],
            price=validated_params['price']
        )
        
        # Format the response
        formatted_response = executor.format_order_response(response)
        
        # Print order response
        executor.print_order_response(formatted_response)
        
        # Print success message
        print_success_message(formatted_response)
        
        logger.info("Order execution completed successfully")
        
    except ValidationError as e:
        print_error_message(f"Validation Error: {str(e)}")
        logger.error(f"Validation error: {str(e)}")
        sys.exit(1)
        
    except BinanceAPIException as e:
        print_error_message(f"Binance API Error [{e.status_code}]: {e.message}")
        logger.error(f"Binance API error: {e.status_code} - {e.message}")
        sys.exit(1)
        
    except BinanceRequestException as e:
        print_error_message(f"Network Error: {str(e)}")
        logger.error(f"Network error: {str(e)}")
        sys.exit(1)
        
    except ValueError as e:
        print_error_message(str(e))
        logger.error(str(e))
        sys.exit(1)
        
    except Exception as e:
        print_error_message(f"Unexpected Error: {str(e)}")
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        sys.exit(1)


if __name__ == '__main__':
    main()