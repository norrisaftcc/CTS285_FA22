#!/usr/bin/env python3
"""
Test runner for the PokeSense application.

This script runs all unit tests and generates a coverage report.
"""

import unittest
import sys
import os

try:
    import coverage
    HAS_COVERAGE = True
except ImportError:
    HAS_COVERAGE = False
    print("Coverage module not found. Install with: pip install coverage")
    print("Continuing without coverage reporting...")


def run_tests_with_coverage():
    """Run tests with coverage reporting."""
    cov = coverage.Coverage(
        source=["core"],
        omit=["*/__pycache__/*", "*/tests/*"],
        branch=True
    )
    
    cov.start()
    
    # Run all tests
    test_suite = unittest.defaultTestLoader.discover("tests", pattern="test_*.py")
    test_runner = unittest.TextTestRunner(verbosity=2)
    result = test_runner.run(test_suite)
    
    cov.stop()
    cov.save()
    
    print("\nCoverage Summary:")
    cov.report()
    
    # Generate HTML report
    coverage_dir = os.path.join(os.path.dirname(__file__), "coverage_html")
    cov.html_report(directory=coverage_dir)
    print(f"\nHTML coverage report generated in: {coverage_dir}")
    
    return not result.failures and not result.errors


def run_tests():
    """Run tests without coverage reporting."""
    test_suite = unittest.defaultTestLoader.discover("tests", pattern="test_*.py")
    test_runner = unittest.TextTestRunner(verbosity=2)
    result = test_runner.run(test_suite)
    return not result.failures and not result.errors


if __name__ == "__main__":
    print("Running PokeSense tests...\n")
    
    if HAS_COVERAGE:
        success = run_tests_with_coverage()
    else:
        success = run_tests()
    
    if success:
        print("\nAll tests passed successfully!")
        sys.exit(0)
    else:
        print("\nSome tests failed.")
        sys.exit(1)