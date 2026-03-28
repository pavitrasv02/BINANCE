#!/usr/bin/env python3
"""Test script to demonstrate the trading bot functionality without API credentials."""

import sys
import os

# Add the parent directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from bot.validators import (
    validate_symbol,
    validate_side,
    validate_order_type,
    validate_quantity,
    validate_price,
    validate_order_params,
    ValidationError
)


def print_test_header(test_name):
    """Print test section header."""
    print("\n" + "="*70)
    print(f"TEST: {test_name}".center(70))
    print("="*70)


def test_validators():
    """Test all validation functions."""
    
    print_test_header("VALIDATION TESTS")
    
    tests = [
        # Symbol validation
        ("Valid symbol: BTCUSDT", lambda: validate_symbol("BTCUSDT"), True),
        ("Valid symbol: ETHUSDT", lambda: validate_symbol("ethusdt"), True),
        ("Invalid symbol: BTCUSD", lambda: validate_symbol("BTCUSD"), False),
        ("Invalid symbol: BTC", lambda: validate_symbol("BTC"), False),
        
        # Side validation
        ("Valid side: BUY", lambda: validate_side("BUY"), True),
        ("Valid side: sell", lambda: validate_side("sell"), True),
        ("Invalid side: HOLD", lambda: validate_side("HOLD"), False),
        
        # Order type validation
        ("Valid type: MARKET", lambda: validate_order_type("MARKET"), True),
        ("Valid type: limit", lambda: validate_order_type("limit"), True),
        ("Invalid type: STOP", lambda: validate_order_type("STOP"), False),
        
        # Quantity validation
        ("Valid quantity: 0.001", lambda: validate_quantity(0.001), True),
        ("Valid quantity: 100", lambda: validate_quantity(100), True),
        ("Invalid quantity: 0", lambda: validate_quantity(0), False),
        ("Invalid quantity: -1", lambda: validate_quantity(-1), False),
        
        # Price validation
        ("Valid price for LIMIT: 43000", lambda: validate_price(43000, "LIMIT"), True),
        ("Valid price for MARKET: None", lambda: validate_price(None, "MARKET"), True),
        ("Invalid price for LIMIT: None", lambda: validate_price(None, "LIMIT"), False),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func, should_pass in tests:
        try:
            result = test_func()
            if should_pass:
                print(f"✓ PASS: {test_name}")
                passed += 1
            else:
                print(f"✗ FAIL: {test_name} (Expected error but passed)")
                failed += 1
        except ValidationError as e:
            if not should_pass:
                print(f"✓ PASS: {test_name} (Correctly raised error)")
                passed += 1
            else:
                print(f"✗ FAIL: {test_name} - {str(e)}")
                failed += 1
        except Exception as e:
            print(f"✗ FAIL: {test_name} - Unexpected error: {str(e)}")
            failed += 1
    
    print(f"\n{'='*70}")
    print(f"Validation Tests Complete: {passed} passed, {failed} failed")
    print(f"{'='*70}\n")
    
    return failed == 0


def test_order_params_validation():
    """Test complete order parameter validation."""
    
    print_test_header("COMPLETE ORDER VALIDATION TESTS")
    
    test_cases = [
        {
            "name": "Valid MARKET order",
            "params": {
                "symbol": "BTCUSDT",
                "side": "BUY",
                "order_type": "MARKET",
                "quantity": 0.001,
                "price": None
            },
            "should_pass": True
        },
        {
            "name": "Valid LIMIT order",
            "params": {
                "symbol": "ETHUSDT",
                "side": "SELL",
                "order_type": "LIMIT",
                "quantity": 0.1,
                "price": 2500
            },
            "should_pass": True
        },
        {
            "name": "Invalid LIMIT order (missing price)",
            "params": {
                "symbol": "BTCUSDT",
                "side": "BUY",
                "order_type": "LIMIT",
                "quantity": 0.001,
                "price": None
            },
            "should_pass": False
        },
        {
            "name": "Invalid symbol (not USDT pair)",
            "params": {
                "symbol": "BTCUSD",
                "side": "BUY",
                "order_type": "MARKET",
                "quantity": 0.001,
                "price": None
            },
            "should_pass": False
        },
    ]
    
    passed = 0
    failed = 0
    
    for test_case in test_cases:
        try:
            result = validate_order_params(**test_case["params"])
            if test_case["should_pass"]:
                print(f"✓ PASS: {test_case['name']}")
                print(f"  Validated params: {result}")
                passed += 1
            else:
                print(f"✗ FAIL: {test_case['name']} (Expected error but passed)")
                failed += 1
        except ValidationError as e:
            if not test_case["should_pass"]:
                print(f"✓ PASS: {test_case['name']} (Correctly raised error)")
                print(f"  Error: {str(e)}")
                passed += 1
            else:
                print(f"✗ FAIL: {test_case['name']} - {str(e)}")
                failed += 1
        except Exception as e:
            print(f"✗ FAIL: {test_case['name']} - Unexpected error: {str(e)}")
            failed += 1
    
    print(f"\n{'='*70}")
    print(f"Order Validation Tests Complete: {passed} passed, {failed} failed")
    print(f"{'='*70}\n")
    
    return failed == 0


def show_cli_examples():
    """Show CLI usage examples."""
    
    print_test_header("CLI USAGE EXAMPLES")
    
    examples = [
        {
            "description": "Market Buy Order",
            "command": "python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001"
        },
        {
            "description": "Limit Sell Order",
            "command": "python cli.py --symbol ETHUSDT --side SELL --type LIMIT --quantity 0.1 --price 2500"
        },
        {
            "description": "With API Credentials",
            "command": "python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001 --api-key YOUR_KEY --api-secret YOUR_SECRET"
        },
        {
            "description": "Get Help",
            "command": "python cli.py --help"
        },
    ]
    
    for i, example in enumerate(examples, 1):
        print(f"\n{i}. {example['description']}")
        print(f"   {example['command']}")
    
    print("\n" + "="*70 + "\n")


def main():
    """Run all tests."""
    print("\n" + "*"*70)
    print("BINANCE FUTURES TRADING BOT - TEST SUITE".center(70))
    print("*"*70)
    
    all_passed = True
    
    # Run validation tests
    if not test_validators():
        all_passed = False
    
    # Run order parameter validation tests
    if not test_order_params_validation():
        all_passed = False
    
    # Show CLI examples
    show_cli_examples()
    
    # Final summary
    print("*"*70)
    if all_passed:
        print("✓ ALL TESTS PASSED".center(70))
    else:
        print("✗ SOME TESTS FAILED".center(70))
    print("*"*70 + "\n")
    
    print("NOTE: To test with real API, you need to:")
    print("  1. Get API credentials from https://testnet.binancefuture.com/")
    print("  2. Set environment variables:")
    print("     export BINANCE_API_KEY='your_key'")
    print("     export BINANCE_API_SECRET='your_secret'")
    print("  3. Run: python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001\n")


if __name__ == "__main__":
    main()