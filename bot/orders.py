"""Order execution logic for the trading bot."""

import logging
from bot.client import BinanceFuturesClient
from bot.validators import validate_order_params, ValidationError
from binance.exceptions import BinanceAPIException, BinanceRequestException

logger = logging.getLogger('trading_bot.orders')


class OrderExecutor:
    """Handles order execution and formatting."""
    
    def __init__(self, api_key, api_secret):
        """Initialize order executor.
        
        Args:
            api_key: Binance API key
            api_secret: Binance API secret
        """
        self.client = BinanceFuturesClient(api_key, api_secret)
        logger.info("OrderExecutor initialized")
    
    def execute_order(self, symbol, side, order_type, quantity, price=None):
        """Execute an order with validation and formatting.
        
        Args:
            symbol: Trading pair symbol
            side: Order side (BUY/SELL)
            order_type: Order type (MARKET/LIMIT)
            quantity: Order quantity
            price: Order price (optional for MARKET)
            
        Returns:
            dict: Formatted order response
        """
        try:
            current_price = self.client.get_price(symbol)
            print("DEBUG current_price:", current_price) 
        except Exception as e:
            logger.error(f"Failed to fetch current price for {symbol}: {str(e)}")
            raise


        try:
            # Validate all parameters
            validated_params = validate_order_params(
                symbol=symbol,
                side=side,
                order_type=order_type,
                quantity=quantity,
                price=price,
                current_price=current_price
            )
            
            # Print order request
            self.print_order_request(validated_params)
            
            # Execute the order
            response = self.client.create_order(
                symbol=validated_params['symbol'],
                side=validated_params['side'],
                order_type=validated_params['type'],
                quantity=validated_params['quantity'],
                price=validated_params['price']
            )
            
            # Format and return response
            formatted_response = self.format_order_response(response)
            return formatted_response
            
        except ValidationError as e:
            logger.error(f"Validation error: {str(e)}")
            raise
        except BinanceAPIException as e:
            logger.error(f"Binance API error: {e.status_code} - {e.message}")
            raise
        except BinanceRequestException as e:
            logger.error(f"Binance request error: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            raise
    
    def print_order_request(self, params):
        """Print formatted order request.
        
        Args:
            params: Validated order parameters
        """
        print("\n" + "="*60)
        print("ORDER REQUEST".center(60))
        print("="*60)
        print(f"Symbol:       {params['symbol']}")
        print(f"Side:         {params['side']}")
        print(f"Type:         {params['type']}")
        print(f"Quantity:     {params['quantity']}")
        if params['price']:
            print(f"Price:        {params['price']}")
        print("="*60 + "\n")
    
    def format_order_response(self, response):
        """Format order response for display.
        
        Args:
            response: Raw order response from Binance
            
        Returns:
            dict: Formatted response
        """
        formatted = {
            'orderId': response.get('orderId'),
            'status': response.get('status'),
            'symbol': response.get('symbol'),
            'side': response.get('side'),
            'type': response.get('type'),
            'quantity': response.get('origQty'),
            'executedQty': response.get('executedQty', '0'),
            'avgPrice': response.get('avgPrice', 'N/A'),
            'updateTime': response.get('updateTime')
        }
        return formatted
    
    def print_order_response(self, response):
        """Print formatted order response.
        
        Args:
            response: Formatted order response
        """
        print("\n" + "="*60)
        print("ORDER RESPONSE".center(60))
        print("="*60)
        print(f"Order ID:       {response['orderId']}")
        print(f"Status:         {response['status']}")
        print(f"Symbol:         {response['symbol']}")
        print(f"Side:           {response['side']}")
        print(f"Type:           {response['type']}")
        print(f"Quantity:       {response['quantity']}")
        print(f"Executed Qty:   {response['executedQty']}")
        print(f"Average Price:  {response['avgPrice']}")
        print("="*60 + "\n")