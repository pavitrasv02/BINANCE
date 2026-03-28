"""Binance Futures API client wrapper."""
import time
import logging
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceRequestException

logger = logging.getLogger('trading_bot.client')


class BinanceFuturesClient:
    """Wrapper for Binance Futures API client."""
    
    TESTNET_BASE_URL = 'https://testnet.binancefuture.com'

    def __init__(self, api_key, api_secret):
        """Initialize Binance Futures client."""
        
        self.api_key = api_key
        self.api_secret = api_secret
        
        try:
            # ✅ Use testnet
            self.client = Client(api_key, api_secret, testnet=True)

            # 🔥 IMPORTANT: Sync time with Binance
            server_time = self.client.get_server_time()
            system_time = int(time.time() * 1000)
            self.client.TIME_OFFSET = server_time['serverTime'] - system_time

            logger.info("Binance Futures Testnet client initialized successfully")

        except Exception as e:
            logger.error(f"Failed to initialize Binance client: {str(e)}")
            raise
    
    def create_order(self, symbol, side, order_type, quantity, price=None):
        """Create a new order on Binance Futures.
        
        Args:
            symbol: Trading pair symbol (e.g., BTCUSDT)
            side: Order side (BUY or SELL)
            order_type: Order type (MARKET or LIMIT)
            quantity: Order quantity
            price: Order price (required for LIMIT orders)
            
        Returns:
            dict: Order response from Binance
            
        Raises:
            BinanceAPIException: If API request fails
            BinanceRequestException: If request fails
        """
        try:
            order_params = {
                'symbol': symbol,
                'side': side,
                'type': order_type,
                'quantity': quantity
                
            }
            
            # Add price for LIMIT orders
            if order_type == 'LIMIT':
                order_params['price'] = price
                order_params['timeInForce'] = 'GTC'  # Good Till Cancel
            
            logger.info(f"Placing order: {order_params}")
            
            # Place the order
            response = self.client.futures_create_order(**order_params)
            
            logger.info(f"Order placed successfully: {response}")
            return response
            
        except BinanceAPIException as e:
            error_msg = f"Binance API error: {e.status_code} - {e.message}"
            logger.error(error_msg)
            raise Exception(error_msg) from e
        except BinanceRequestException as e:
            error_msg = f"Binance request/network error: {str(e)}. This may be due to invalid credentials or testnet being down."
            logger.error(error_msg)
            raise Exception(error_msg) from e
        except Exception as e:
            error_msg = f"Unexpected error while placing order: {str(e)}"
            logger.error(error_msg)
            raise
    
    def get_account_info(self):
        """Get Futures account information.
        
        Returns:
            dict: Account information
        """
        try:
            return self.client.futures_account()
        except Exception as e:
            logger.error(f"Failed to get account info: {str(e)}")
            raise
    
    def get_symbol_info(self, symbol):
        """Get information about a trading symbol.
        
        Args:
            symbol: Trading pair symbol
            
        Returns:
            dict: Symbol information
        """
        try:
            exchange_info = self.client.futures_exchange_info()
            for s in exchange_info['symbols']:
                if s['symbol'] == symbol:
                    return s
            return None
        except Exception as e:
            logger.error(f"Failed to get symbol info: {str(e)}")
            raise

    def get_price(self, symbol):
        """Get current price for a symbol.
        
        Args:
            symbol: Trading pair symbol
            
        Returns:
            float: Current price
        """
        try:
            response = self.client.futures_symbol_ticker(symbol=symbol)
            
            if not response or 'price' not in response:
                raise ValueError(f"Invalid price response from Binance: {response}")
            
            price = float(response['price'])
            logger.info(f"Fetched price for {symbol}: {price}")
            return price

        except Exception as e:
            error_msg = f"Failed to fetch price for {symbol}: {str(e)}"
            logger.error(error_msg)
            raise Exception(error_msg) from e