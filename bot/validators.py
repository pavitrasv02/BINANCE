"""Input validation for trading bot."""

import logging

logger = logging.getLogger('trading_bot.validators')


class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass


def validate_symbol(symbol):
    """Validate trading symbol.
    
    Args:
        symbol: Trading pair symbol (e.g., BTCUSDT)
        
    Raises:
        ValidationError: If symbol is invalid
    """
    if not symbol:
        raise ValidationError("Symbol cannot be empty")
    
    # Convert to uppercase for validation
    symbol_upper = symbol.upper()
    
    if not symbol_upper.endswith('USDT'):
        raise ValidationError(
            f"Invalid symbol '{symbol}'. Only USDT pairs are allowed (e.g., BTCUSDT, ETHUSDT)"
        )
    
    if not symbol_upper.isalnum():
        raise ValidationError(
            f"Invalid symbol '{symbol}'. Symbol should contain only alphanumeric characters"
        )
    
    logger.info(f"Symbol validation passed: {symbol_upper}")
    return symbol_upper


def validate_side(side):
    """Validate order side.
    
    Args:
        side: Order side (BUY or SELL)
        
    Raises:
        ValidationError: If side is invalid
    """
    valid_sides = ['BUY', 'SELL']
    side_upper = side.upper()
    
    if side_upper not in valid_sides:
        raise ValidationError(
            f"Invalid side '{side}'. Must be one of: {', '.join(valid_sides)}"
        )
    
    logger.info(f"Side validation passed: {side_upper}")
    return side_upper


def validate_order_type(order_type):
    """Validate order type.
    
    Args:
        order_type: Type of order (MARKET or LIMIT)
        
    Raises:
        ValidationError: If order type is invalid
    """
    valid_types = ['MARKET', 'LIMIT']
    type_upper = order_type.upper()
    
    if type_upper not in valid_types:
        raise ValidationError(
            f"Invalid order type '{order_type}'. Must be one of: {', '.join(valid_types)}"
        )
    
    logger.info(f"Order type validation passed: {type_upper}")
    return type_upper


def validate_quantity(quantity):
    """Validate order quantity.
    
    Args:
        quantity: Order quantity
        
    Raises:
        ValidationError: If quantity is invalid
    """
    try:
        qty = float(quantity)
    except (ValueError, TypeError):
        raise ValidationError(
            f"Invalid quantity '{quantity}'. Must be a valid number"
        )
    
    if qty <= 0:
        raise ValidationError(
            f"Invalid quantity '{qty}'. Must be greater than 0"
        )
    
    logger.info(f"Quantity validation passed: {qty}")
    return qty


def validate_price(price, order_type):
    """Validate order price.
    
    Args:
        price: Order price (required for LIMIT orders)
        order_type: Type of order
        
    Raises:
        ValidationError: If price is invalid
    """
    if order_type == 'LIMIT':
        if price is None:
            raise ValidationError(
                "Price is required for LIMIT orders. Use --price <value>"
            )
        
        try:
            price_float = float(price)
        except (ValueError, TypeError):
            raise ValidationError(
                f"Invalid price '{price}'. Must be a valid number"
            )
        
        if price_float <= 0:
            raise ValidationError(
                f"Invalid price '{price_float}'. Must be greater than 0"
            )
        
        logger.info(f"Price validation passed: {price_float}")
        return price_float
    
    return None


def validate_order_params(symbol, side, order_type, quantity, price=None, current_price=None):
    
    # Validate each parameter using individual validators
    symbol = validate_symbol(symbol)
    side = validate_side(side)
    order_type = validate_order_type(order_type)
    quantity = validate_quantity(quantity)
    
    # Validate price for LIMIT orders
    if order_type == 'LIMIT':
        if price is None:
            raise ValidationError(
                "Price is required for LIMIT orders. Use --price <value>"
            )
        price = validate_price(price, order_type)
    
    # =========================================
    # Notional value validation
    # =========================================

    MIN_NOTIONAL = 100

    # For price calculation: use provided price if available, otherwise use current_price
    # If we have either price or current_price, validate notional
    if price:
        notional = float(price) * float(quantity)
        if notional < MIN_NOTIONAL:
            raise ValidationError(
                f"Order value must be at least {MIN_NOTIONAL} USDT. Current: {notional:.2f}"
            )
    elif current_price is not None:
        notional = float(current_price) * float(quantity)
        if notional < MIN_NOTIONAL:
            raise ValidationError(
                f"Order value must be at least {MIN_NOTIONAL} USDT. Current: {notional:.2f}"
            )
    # If we don't have either price or current_price, skip notional validation for now
    # (it will be validated again during execute_order)

    # =========================================
    # ✅ RETURN (must be AFTER validation)
    # =========================================

    return {
        'symbol': symbol,
        'side': side,
        'type': order_type,
        'quantity': quantity,
        'price': price
    }