#!/usr/bin/env python3
"""
Hello World Application
A simple Python program that greets the user.
"""


def hello_world():
    """Print a friendly greeting message."""
    print("Hello, World!")


def generate_multiplication_table(number, limit=10):
    """
    Generate and print a multiplication table for the given number.
    
    Args:
        number (int): The number for which to generate the multiplication table.
        limit (int): The range of multiplication (default is 10).
    """
    print(f"\nMultiplication Table for {number}:")
    print("-" * 30)
    for i in range(1, limit + 1):
        result = number * i
        print(f"{number} × {i} = {result}")
    print("-" * 30)


def main():
    """Main entry point of the application."""
    hello_world()
    
    # Get user input for multiplication table
    try:
        user_input = input("\nEnter a number to generate its multiplication table (or press Enter to skip): ")
        if user_input.strip():
            number = int(user_input)
            limit_input = input("Enter the range for multiplication table (default is 10): ")
            limit = int(limit_input) if limit_input.strip() else 10
            generate_multiplication_table(number, limit)
        else:
            print("Skipped multiplication table generation.")
    except ValueError:
        print("Error: Please enter a valid integer.")


if __name__ == "__main__":
    main()
