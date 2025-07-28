#!/usr/bin/env python3
"""
NamiBot Launcher
Choose between console and GUI versions of NamiBot.
"""

import sys
import os


def main():
    """Main launcher function."""
    print("🤖 NamiBot Launcher")
    print("=" * 40)
    print("Choose your preferred interface:")
    print("1. Console Version (Command Line)")
    print("2. GUI Version (Graphical Interface)")
    print("3. Test Suite & Demo")
    print("4. Install Dependencies")
    print("5. Exit")
    print("=" * 40)
    
    while True:
        try:
            choice = input("Enter your choice (1-5): ").strip()
            
            if choice == "1":
                print("\nStarting Console Version...")
                print("Ask me about any topic and I'll search Wikipedia documents!")
                os.system("python namibot.py")
                break
            elif choice == "2":
                print("\nStarting GUI Version...")
                print("Opening graphical interface with clickable links!")
                os.system("python gui_namibot.py")
                break
            elif choice == "3":
                print("\nStarting Test Suite...")
                print("Running comprehensive tests and demo...")
                os.system("python test_namibot.py")
                break
            elif choice == "4":
                print("\nInstalling Dependencies...")
                print("This will install the required packages for Wikipedia API access.")
                os.system("pip install -r requirements.txt")
                print("Dependencies installed! You can now run NamiBot.")
                break
            elif choice == "5":
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please enter 1, 2, 3, 4, or 5.")
                
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except EOFError:
            print("\n\nGoodbye!")
            break


if __name__ == "__main__":
    main() 