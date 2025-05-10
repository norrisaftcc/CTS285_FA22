#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run_tests.py - Script to run all tests with coverage report

This script runs all the tests in the project and generates a coverage report.
"""
import os
import sys
import unittest
import coverage

# Start coverage tracking
cov = coverage.Coverage(
    source=["dataman"],
    omit=[
        "*/tests/*",
        "*/examples/*",
        "setup.py",
    ]
)
cov.start()

# Find and run all tests
loader = unittest.TestLoader()
tests = loader.discover("tests")
test_runner = unittest.TextTestRunner(verbosity=2)
result = test_runner.run(tests)

# End coverage tracking and generate report
cov.stop()
cov.save()

print("\nCoverage Summary:")
cov.report()

# Generate HTML report
if not os.path.exists("coverage_html"):
    os.makedirs("coverage_html")
cov.html_report(directory="coverage_html")
print(f"\nHTML coverage report generated in coverage_html/index.html")

# Exit with non-zero status if any tests failed
if not result.wasSuccessful():
    sys.exit(1)