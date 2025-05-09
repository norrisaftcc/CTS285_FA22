#!/usr/bin/env python3
"""
Test runner for the BookSense application.

This script runs all tests and generates a coverage report.
"""

import os
import sys
import unittest
import coverage

def run_tests():
    """Run all tests in the 'tests' directory."""
    # Start code coverage measurement
    cov = coverage.Coverage(
        source=["core"],
        omit=["*/__pycache__/*"]
    )
    cov.start()
    
    try:
        # Discover and run tests
        loader = unittest.TestLoader()
        tests = loader.discover("tests")
        test_runner = unittest.TextTestRunner(verbosity=2)
        result = test_runner.run(tests)
        
        # Stop coverage measurement
        cov.stop()
        cov.save()
        
        # Generate coverage report
        print("\nCoverage Report:")
        cov.report()
        
        # Generate HTML report
        cov_dir = "coverage_html"
        if not os.path.exists(cov_dir):
            os.makedirs(cov_dir)
        cov.html_report(directory=cov_dir)
        print(f"\nHTML coverage report generated in {cov_dir}/")
        
        # Return exit code based on test results
        return 0 if result.wasSuccessful() else 1
    
    except KeyboardInterrupt:
        print("\nTests interrupted by user.")
        return 130

if __name__ == "__main__":
    # Run tests and exit with appropriate code
    sys.exit(run_tests())