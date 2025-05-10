#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
dataman_cli.py - Command-line interface for the Dataman application

This module provides a command-line interface for the Dataman application,
allowing users to interact with the application from the terminal.
"""
import argparse
import time
from typing import List, Optional

from dataman.core.models import Problem, ProblemSet
from dataman.core.operations import DatamanOperations
from dataman.core.storage_factory import StorageFactory
from dataman.core.utils import format_time, get_default_storage_path


class DatamanCLI:
    """Command-line interface for the Dataman application."""
    
    def __init__(self, storage_type: str = 'json', storage_path: Optional[str] = None):
        """
        Initialize the CLI with the specified storage backend.
        
        Args:
            storage_type (str): Type of storage to use ('json', 'sqlite')
            storage_path (Optional[str]): Path to the storage file or database
        """
        if storage_path is None:
            storage_path = get_default_storage_path(storage_type)
        
        if storage_type == 'json':
            storage = StorageFactory.create_storage(storage_type, file_path=storage_path)
        elif storage_type == 'sqlite':
            storage = StorageFactory.create_storage(storage_type, db_path=storage_path)
        else:
            raise ValueError(f"Unsupported storage type: {storage_type}")
        
        self.operations = DatamanOperations(storage)
    
    def run(self):
        """Run the main CLI interface."""
        print("Welcome to Dataman!")
        print("===================")
        
        running = True
        while running:
            print("\nMain Menu:")
            print("1. Answer Checker")
            print("2. Memory Bank")
            print("3. Problem Sets")
            print("4. Timed Drill")
            print("5. Statistics")
            print("0. Exit")
            
            choice = input("Enter your choice: ")
            
            if choice == "0":
                running = False
            elif choice == "1":
                self.answer_checker_menu()
            elif choice == "2":
                self.memory_bank_menu()
            elif choice == "3":
                self.problem_sets_menu()
            elif choice == "4":
                self.timed_drill_menu()
            elif choice == "5":
                self.show_statistics()
            else:
                print("Invalid choice. Please try again.")
    
    def answer_checker_menu(self):
        """Show the answer checker menu."""
        print("\nAnswer Checker")
        print("=============")
        print("Problem format: 2 + 2 = 4")
        
        problem_input = input("Enter math problem: ")
        try:
            parts = problem_input.split()
            first = int(parts[0])
            operator = parts[1]
            second = int(parts[2])
            # Skip the equals sign
            answer = int(parts[4])
            
            problem = Problem(first, operator, second)
            is_correct = problem.check_answer(answer)
            
            if is_correct:
                print("Correct!")
            else:
                print(f"Incorrect. The correct answer is {problem.solve()}.")
        except (ValueError, IndexError) as e:
            print(f"Invalid problem format. Please use the format '2 + 2 = 4'. Error: {e}")
    
    def memory_bank_menu(self):
        """Show the memory bank menu."""
        if not self.operations.current_problem_set:
            print("\nNo problem set loaded. Please load or create a problem set first.")
            self.problem_sets_menu()
            return
        
        running = True
        while running:
            print(f"\nMemory Bank - {self.operations.current_problem_set.name}")
            print("=============")
            print("1. Solve Next Problem")
            print("2. Add Problem")
            print("3. List All Problems")
            print("4. Remove Problem")
            print("0. Back to Main Menu")
            
            choice = input("Enter your choice: ")
            
            if choice == "0":
                running = False
            elif choice == "1":
                self.solve_next_problem()
            elif choice == "2":
                self.add_problem()
            elif choice == "3":
                self.list_all_problems()
            elif choice == "4":
                self.remove_problem()
            else:
                print("Invalid choice. Please try again.")
    
    def solve_next_problem(self):
        """Solve the next problem from the current problem set."""
        problems = self.operations.get_current_problems()
        if not problems:
            print("No problems in the current problem set.")
            return
        
        # Find the first unanswered problem
        unanswered = [i for i, p in enumerate(problems) if p.user_answer is None]
        if not unanswered:
            print("All problems have been answered. Starting over...")
            # Reset user answers
            for problem in problems:
                problem.user_answer = None
            unanswered = list(range(len(problems)))
        
        idx = unanswered[0]
        problem = problems[idx]
        
        print(f"\nProblem #{idx + 1}:")
        print(problem.show_problem_to_solve())
        
        try:
            answer = int(input("Your answer: "))
            is_correct = self.operations.check_answer(idx, answer)
            
            if is_correct:
                print("Correct!")
            else:
                print(f"Incorrect. The correct answer is {problem.solve()}.")
            
            # Save the problem set
            self.operations.save_current_problem_set()
        except ValueError:
            print("Invalid input. Please enter a number.")
    
    def add_problem(self):
        """Add a problem to the current problem set."""
        print("\nAdd a new problem")
        print("Problem format: 2 + 2 = 4")
        
        problem_input = input("Enter math problem: ")
        try:
            parts = problem_input.split()
            first = int(parts[0])
            operator = parts[1]
            second = int(parts[2])
            # Skip the equals sign
            answer = int(parts[4])
            
            problem = Problem(first, operator, second, answer)
            
            if self.operations.add_problem(problem):
                print("Problem added successfully.")
                self.operations.save_current_problem_set()
            else:
                print("Failed to add problem.")
        except (ValueError, IndexError) as e:
            print(f"Invalid problem format. Please use the format '2 + 2 = 4'. Error: {e}")
    
    def list_all_problems(self):
        """List all problems in the current problem set."""
        problems = self.operations.get_current_problems()
        if not problems:
            print("No problems in the current problem set.")
            return
        
        print("\nAll Problems:")
        for i, problem in enumerate(problems):
            status = "✓" if problem.user_answer is not None and problem.user_answer == problem.solve() else \
                     "✗" if problem.user_answer is not None else " "
            print(f"{i+1}. [{status}] {problem}")
    
    def remove_problem(self):
        """Remove a problem from the current problem set."""
        self.list_all_problems()
        
        problems = self.operations.get_current_problems()
        if not problems:
            return
        
        try:
            idx = int(input("\nEnter the number of the problem to remove: ")) - 1
            if idx < 0 or idx >= len(problems):
                print("Invalid problem number.")
                return
            
            removed = self.operations.remove_problem(idx)
            if removed:
                print(f"Problem '{removed}' removed successfully.")
                self.operations.save_current_problem_set()
            else:
                print("Failed to remove problem.")
        except ValueError:
            print("Invalid input. Please enter a number.")
    
    def problem_sets_menu(self):
        """Show the problem sets menu."""
        running = True
        while running:
            print("\nProblem Sets")
            print("============")
            print("1. Create New Problem Set")
            print("2. Load Problem Set")
            print("3. Generate Random Problem Set")
            print("4. Delete Problem Set")
            print("0. Back to Main Menu")
            
            choice = input("Enter your choice: ")
            
            if choice == "0":
                running = False
            elif choice == "1":
                self.create_problem_set()
            elif choice == "2":
                self.load_problem_set()
            elif choice == "3":
                self.generate_random_problem_set()
            elif choice == "4":
                self.delete_problem_set()
            else:
                print("Invalid choice. Please try again.")
    
    def create_problem_set(self):
        """Create a new problem set."""
        name = input("Enter a name for the problem set: ")
        description = input("Enter a description (optional): ")
        
        problem_set = self.operations.create_problem_set(name, description)
        if problem_set:
            print(f"Problem set '{name}' created successfully.")
            self.operations.save_current_problem_set()
        else:
            print("Failed to create problem set.")
    
    def load_problem_set(self):
        """Load a problem set from storage."""
        problem_sets = self.operations.list_problem_sets()
        if not problem_sets:
            print("No problem sets available.")
            return
        
        print("\nAvailable Problem Sets:")
        for i, name in enumerate(problem_sets):
            print(f"{i+1}. {name}")
        
        try:
            idx = int(input("\nEnter the number of the problem set to load: ")) - 1
            if idx < 0 or idx >= len(problem_sets):
                print("Invalid problem set number.")
                return
            
            name = problem_sets[idx]
            problem_set = self.operations.load_problem_set(name)
            if problem_set:
                print(f"Problem set '{name}' loaded successfully.")
            else:
                print(f"Failed to load problem set '{name}'.")
        except ValueError:
            print("Invalid input. Please enter a number.")
    
    def generate_random_problem_set(self):
        """Generate a random problem set."""
        name = input("Enter a name for the problem set: ")
        description = input("Enter a description (optional): ")
        
        try:
            num_problems = int(input("Enter the number of problems to generate (default: 10): ") or "10")
            
            print("\nDifficulty levels:")
            print("1. Easy (single digit numbers)")
            print("2. Medium (double digit numbers)")
            print("3. Hard (large numbers)")
            difficulty_choice = input("Select difficulty (default: 1): ") or "1"
            
            difficulty_map = {"1": "easy", "2": "medium", "3": "hard"}
            difficulty = difficulty_map.get(difficulty_choice, "easy")
            
            print("\nOperators:")
            print("1. Addition (+)")
            print("2. Subtraction (-)")
            print("3. Multiplication (*)")
            print("4. Division (/)")
            print("5. All operators")
            operator_choice = input("Select operators (comma-separated, default: 5): ") or "5"
            
            operators = []
            if "5" in operator_choice:
                operators = ["+", "-", "*", "/"]
            else:
                operator_map = {"1": "+", "2": "-", "3": "*", "4": "/"}
                for choice in operator_choice.split(","):
                    if choice.strip() in operator_map:
                        operators.append(operator_map[choice.strip()])
            
            if not operators:
                operators = ["+", "-", "*", "/"]
            
            problem_set = self.operations.generate_problem_set(
                name, num_problems, difficulty, operators, description
            )
            
            if problem_set:
                print(f"Problem set '{name}' with {num_problems} problems generated successfully.")
                self.operations.save_current_problem_set()
            else:
                print("Failed to generate problem set.")
        except ValueError:
            print("Invalid input. Please enter a number.")
    
    def delete_problem_set(self):
        """Delete a problem set from storage."""
        problem_sets = self.operations.list_problem_sets()
        if not problem_sets:
            print("No problem sets available.")
            return
        
        print("\nAvailable Problem Sets:")
        for i, name in enumerate(problem_sets):
            print(f"{i+1}. {name}")
        
        try:
            idx = int(input("\nEnter the number of the problem set to delete: ")) - 1
            if idx < 0 or idx >= len(problem_sets):
                print("Invalid problem set number.")
                return
            
            name = problem_sets[idx]
            confirm = input(f"Are you sure you want to delete problem set '{name}'? (y/N): ")
            if confirm.lower() == 'y':
                success = self.operations.storage.delete_problem_set(name)
                if success:
                    print(f"Problem set '{name}' deleted successfully.")
                    # Reset current problem set if it was the deleted one
                    if self.operations.current_problem_set and self.operations.current_problem_set.name == name:
                        self.operations.current_problem_set = None
                else:
                    print(f"Failed to delete problem set '{name}'.")
        except ValueError:
            print("Invalid input. Please enter a number.")
    
    def timed_drill_menu(self):
        """Show the timed drill menu."""
        print("\nTimed Drill")
        print("===========")
        print("Complete a set of problems as quickly as possible.")
        
        try:
            num_problems = int(input("Enter the number of problems (default: 20): ") or "20")
            
            print("\nDifficulty levels:")
            print("1. Easy (single digit numbers)")
            print("2. Medium (double digit numbers)")
            print("3. Hard (large numbers)")
            difficulty_choice = input("Select difficulty (default: 1): ") or "1"
            
            difficulty_map = {"1": "easy", "2": "medium", "3": "hard"}
            difficulty = difficulty_map.get(difficulty_choice, "easy")
            
            print("\nOperators:")
            print("1. Addition (+)")
            print("2. Subtraction (-)")
            print("3. Multiplication (*)")
            print("4. Division (/)")
            print("5. All operators")
            operator_choice = input("Select operators (comma-separated, default: 5): ") or "5"
            
            operators = []
            if "5" in operator_choice:
                operators = ["+", "-", "*", "/"]
            else:
                operator_map = {"1": "+", "2": "-", "3": "*", "4": "/"}
                for choice in operator_choice.split(","):
                    if choice.strip() in operator_map:
                        operators.append(operator_map[choice.strip()])
            
            if not operators:
                operators = ["+", "-", "*", "/"]
            
            # Generate problems
            problems = []
            for _ in range(num_problems):
                problem = self.operations.generate_random_problem("easy", operators)
                problems.append(problem)
            
            input("\nPress Enter to start the drill...")
            
            # Start the drill
            start_time = time.time()
            correct = 0
            
            for i, problem in enumerate(problems):
                print(f"\nProblem {i+1}/{num_problems}:")
                print(problem.show_problem_to_solve())
                
                try:
                    answer = int(input("Your answer: "))
                    if problem.check_answer(answer):
                        print("Correct!")
                        correct += 1
                    else:
                        print(f"Incorrect. The correct answer is {problem.solve()}.")
                except ValueError:
                    print("Invalid input. Skipping problem.")
            
            # End the drill
            end_time = time.time()
            elapsed_time = int(end_time - start_time)
            
            print("\nDrill completed!")
            print(f"Time: {format_time(elapsed_time)}")
            print(f"Score: {correct}/{num_problems} ({correct/num_problems*100:.1f}%)")
            
            if correct == num_problems:
                print("Perfect score! Excellent work!")
            elif correct >= num_problems * 0.8:
                print("Great job!")
            elif correct >= num_problems * 0.6:
                print("Good effort!")
            else:
                print("Keep practicing!")
            
            # Ask to save as a problem set
            save = input("\nDo you want to save these problems as a problem set? (y/N): ")
            if save.lower() == 'y':
                name = input("Enter a name for the problem set: ")
                description = f"Timed drill - {format_time(elapsed_time)} - {correct}/{num_problems}"
                
                problem_set = self.operations.create_problem_set(name, description)
                for problem in problems:
                    self.operations.add_problem(problem)
                
                self.operations.save_current_problem_set()
                print(f"Problem set '{name}' saved successfully.")
        except ValueError:
            print("Invalid input. Please enter a number.")
    
    def show_statistics(self):
        """Show statistics for the current problem set."""
        if not self.operations.current_problem_set:
            print("\nNo problem set loaded. Please load or create a problem set first.")
            return
        
        stats = self.operations.get_statistics()
        
        print(f"\nStatistics for '{self.operations.current_problem_set.name}'")
        print("======================")
        print(f"Total problems: {stats['total_problems']}")
        print(f"Attempted: {stats['attempted']}")
        print(f"Correct: {stats['correct']}")
        print(f"Accuracy: {stats['accuracy']:.1f}%")
        
        if stats['by_operator']:
            print("\nBy Operator:")
            for op, op_stats in stats['by_operator'].items():
                if op_stats['total'] > 0:
                    print(f"  {op}: {op_stats['correct']}/{op_stats['attempted']} " +
                          f"({op_stats['accuracy']:.1f}%)")


def main():
    """Main entry point for the CLI application."""
    parser = argparse.ArgumentParser(description="Dataman - A math problem solver and trainer")
    parser.add_argument("--storage", choices=["json", "sqlite"], default="json",
                        help="Storage backend to use (default: json)")
    parser.add_argument("--path", help="Path to the storage file or database")
    
    args = parser.parse_args()
    
    try:
        cli = DatamanCLI(args.storage, args.path)
        cli.run()
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())