#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
dataman_app.py - Streamlit web interface for the Dataman application

This module provides a web-based interface for the Dataman application
using Streamlit, allowing users to interact with the application through a browser.
"""
import os
import time
from typing import List, Optional, Tuple

import streamlit as st

from dataman.core.models import Problem, ProblemSet
from dataman.core.operations import DatamanOperations
from dataman.core.storage_factory import StorageFactory
from dataman.core.utils import format_time, get_default_storage_path


# Streamlit app configuration
st.set_page_config(
    page_title="Dataman",
    page_icon="🔢",
    layout="wide",
    initial_sidebar_state="expanded"
)


def initialize_session_state():
    """Initialize session state variables if they don't exist."""
    if "operations" not in st.session_state:
        # Use JSON storage by default
        storage_path = get_default_storage_path("json")
        storage = StorageFactory.create_storage("json", file_path=storage_path)
        st.session_state.operations = DatamanOperations(storage)
    
    if "current_problem_index" not in st.session_state:
        st.session_state.current_problem_index = 0
    
    if "drill_problems" not in st.session_state:
        st.session_state.drill_problems = []
    
    if "drill_start_time" not in st.session_state:
        st.session_state.drill_start_time = None
    
    if "drill_answers" not in st.session_state:
        st.session_state.drill_answers = []
    
    if "drill_completed" not in st.session_state:
        st.session_state.drill_completed = False


def render_sidebar():
    """Render the sidebar with navigation options."""
    st.sidebar.title("Dataman")
    st.sidebar.subheader("Math Problem Solver & Trainer")
    
    # Navigation
    page = st.sidebar.radio(
        "Navigation",
        ["Home", "Answer Checker", "Memory Bank", "Problem Sets", "Timed Drill"]
    )
    
    # Show current problem set if loaded
    if st.session_state.operations.current_problem_set:
        st.sidebar.subheader("Current Problem Set")
        st.sidebar.write(f"📚 {st.session_state.operations.current_problem_set.name}")
        
        # Show problem set stats
        stats = st.session_state.operations.get_statistics()
        st.sidebar.write(f"Problems: {stats['total_problems']}")
        if stats['attempted'] > 0:
            st.sidebar.write(f"Accuracy: {stats['accuracy']:.1f}%")
    
    # Storage configuration
    st.sidebar.subheader("Storage Configuration")
    storage_type = st.sidebar.selectbox(
        "Storage Type",
        ["json", "sqlite"],
        index=0
    )
    
    if storage_type == "json":
        storage_path = st.sidebar.text_input(
            "JSON File Path",
            value=get_default_storage_path("json")
        )
    else:
        storage_path = st.sidebar.text_input(
            "SQLite Database Path",
            value=get_default_storage_path("sqlite")
        )
    
    if st.sidebar.button("Apply Storage Configuration"):
        try:
            storage = StorageFactory.create_storage(storage_type, 
                                                   file_path=storage_path if storage_type == "json" else None,
                                                   db_path=storage_path if storage_type == "sqlite" else None)
            st.session_state.operations = DatamanOperations(storage)
            st.sidebar.success(f"Storage configuration updated to {storage_type}.")
        except Exception as e:
            st.sidebar.error(f"Error updating storage configuration: {e}")
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("© 2023 Dataman")
    
    return page


def render_home_page():
    """Render the home page with application information."""
    st.title("Welcome to Dataman! 🔢")
    
    st.markdown("""
    Dataman is a math problem solver and trainer that helps you:
    
    - Check your answers to math problems
    - Build and practice problem sets
    - Test your speed with timed drills
    - Track your progress over time
    
    Use the sidebar to navigate through different features.
    """)
    
    # Show options as cards in a grid
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### Answer Checker
        
        Verify if your answer to a math problem is correct.
        
        [Go to Answer Checker](#)
        """)
        
        st.markdown("""
        ### Problem Sets
        
        Create, load, and manage problem sets for practice.
        
        [Go to Problem Sets](#)
        """)
    
    with col2:
        st.markdown("""
        ### Memory Bank
        
        Store and practice math problems.
        
        [Go to Memory Bank](#)
        """)
        
        st.markdown("""
        ### Timed Drill
        
        Test your speed and accuracy with timed drills.
        
        [Go to Timed Drill](#)
        """)


def render_answer_checker():
    """Render the answer checker page."""
    st.title("Answer Checker ✓")
    
    st.markdown("""
    Enter a math problem in the format "2 + 2 = 4" to check if the answer is correct.
    Supported operators: +, -, *, /
    """)
    
    problem_input = st.text_input("Enter math problem (e.g., 2 + 2 = 4)")
    
    if st.button("Check Answer"):
        if not problem_input:
            st.error("Please enter a math problem.")
            return
        
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
                st.success("Correct! ✓")
            else:
                st.error(f"Incorrect. ✗ The correct answer is {problem.solve()}.")
            
            # Option to add to current problem set
            if st.session_state.operations.current_problem_set:
                if st.button("Add to Current Problem Set"):
                    if st.session_state.operations.add_problem(problem):
                        st.session_state.operations.save_current_problem_set()
                        st.success(f"Problem added to '{st.session_state.operations.current_problem_set.name}'.")
                    else:
                        st.error("Failed to add problem to the current problem set.")
        except (ValueError, IndexError) as e:
            st.error(f"Invalid problem format. Please use the format '2 + 2 = 4'. Error: {e}")
    
    # Custom problem builder
    st.markdown("---")
    st.subheader("Problem Builder")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        first = st.number_input("First number", value=2)
    
    with col2:
        operator = st.selectbox("Operator", ["+", "-", "*", "/"])
    
    with col3:
        second = st.number_input("Second number", value=2)
    
    with col4:
        answer = st.number_input("Answer", value=4)
    
    if st.button("Check Built Problem"):
        problem = Problem(first, operator, second)
        is_correct = problem.check_answer(answer)
        
        if is_correct:
            st.success("Correct! ✓")
        else:
            st.error(f"Incorrect. ✗ The correct answer is {problem.solve()}.")
        
        # Option to add to current problem set
        if st.session_state.operations.current_problem_set:
            if st.button("Add Built Problem to Current Problem Set"):
                if st.session_state.operations.add_problem(problem):
                    st.session_state.operations.save_current_problem_set()
                    st.success(f"Problem added to '{st.session_state.operations.current_problem_set.name}'.")
                else:
                    st.error("Failed to add problem to the current problem set.")


def render_memory_bank():
    """Render the memory bank page."""
    st.title("Memory Bank 🧠")
    
    if not st.session_state.operations.current_problem_set:
        st.warning("No problem set loaded. Please load or create a problem set first.")
        render_problem_sets()
        return
    
    st.subheader(f"Current Problem Set: {st.session_state.operations.current_problem_set.name}")
    
    # Tabs for different memory bank functions
    tab1, tab2, tab3 = st.tabs(["Solve Problems", "Add Problems", "Manage Problems"])
    
    with tab1:
        render_solve_problems()
    
    with tab2:
        render_add_problems()
    
    with tab3:
        render_manage_problems()


def render_solve_problems():
    """Render the solve problems tab in the memory bank."""
    problems = st.session_state.operations.get_current_problems()
    if not problems:
        st.warning("No problems in the current problem set.")
        return
    
    # Problem navigation
    col1, col2, col3 = st.columns([1, 3, 1])
    
    with col1:
        if st.button("Previous") and st.session_state.current_problem_index > 0:
            st.session_state.current_problem_index -= 1
    
    with col2:
        st.write(f"Problem {st.session_state.current_problem_index + 1} of {len(problems)}")
    
    with col3:
        if st.button("Next") and st.session_state.current_problem_index < len(problems) - 1:
            st.session_state.current_problem_index += 1
    
    # Display current problem
    current_index = st.session_state.current_problem_index
    if current_index < len(problems):
        current_problem = problems[current_index]
        
        st.markdown(f"### {current_problem.show_problem_to_solve()}")
        
        answer = st.number_input("Your answer", key=f"answer_{current_index}")
        
        if st.button("Check Answer"):
            is_correct = st.session_state.operations.check_answer(current_index, answer)
            
            if is_correct:
                st.success("Correct! ✓")
            else:
                st.error(f"Incorrect. ✗ The correct answer is {current_problem.solve()}.")
            
            # Save the problem set
            st.session_state.operations.save_current_problem_set()


def render_add_problems():
    """Render the add problems tab in the memory bank."""
    st.subheader("Add a New Problem")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        first = st.number_input("First number", value=2, key="add_first")
    
    with col2:
        operator = st.selectbox("Operator", ["+", "-", "*", "/"], key="add_operator")
    
    with col3:
        second = st.number_input("Second number", value=2, key="add_second")
    
    with col4:
        answer = st.number_input("Answer", value=4, key="add_answer")
    
    if st.button("Add Problem"):
        problem = Problem(first, operator, second, answer)
        
        if st.session_state.operations.add_problem(problem):
            st.session_state.operations.save_current_problem_set()
            st.success("Problem added successfully.")
        else:
            st.error("Failed to add problem.")


def render_manage_problems():
    """Render the manage problems tab in the memory bank."""
    problems = st.session_state.operations.get_current_problems()
    if not problems:
        st.warning("No problems in the current problem set.")
        return
    
    st.subheader("All Problems")
    
    # Display problems in a table
    problem_data = []
    for i, problem in enumerate(problems):
        status = "✓" if problem.user_answer is not None and problem.user_answer == problem.solve() else \
                "✗" if problem.user_answer is not None else " "
        problem_data.append([i+1, str(problem), status, "Delete"])
    
    # Create a DataFrame and display it
    import pandas as pd
    df = pd.DataFrame(problem_data, columns=["#", "Problem", "Status", "Action"])
    st.dataframe(df)
    
    # Allow removal of problems
    col1, col2 = st.columns(2)
    
    with col1:
        problem_to_remove = st.number_input("Problem number to remove", min_value=1, max_value=len(problems), step=1)
    
    with col2:
        if st.button("Remove Problem"):
            try:
                idx = int(problem_to_remove) - 1
                if idx < 0 or idx >= len(problems):
                    st.error("Invalid problem number.")
                else:
                    removed = st.session_state.operations.remove_problem(idx)
                    if removed:
                        st.session_state.operations.save_current_problem_set()
                        st.success(f"Problem '{removed}' removed successfully.")
                        
                        # Update current problem index if needed
                        if st.session_state.current_problem_index >= len(st.session_state.operations.get_current_problems()):
                            st.session_state.current_problem_index = max(0, len(st.session_state.operations.get_current_problems()) - 1)
                    else:
                        st.error("Failed to remove problem.")
            except ValueError:
                st.error("Invalid input. Please enter a number.")


def render_problem_sets():
    """Render the problem sets page."""
    st.title("Problem Sets 📚")
    
    # Tabs for different problem set functions
    tab1, tab2, tab3, tab4 = st.tabs(["Available Sets", "Create New", "Generate Random", "Statistics"])
    
    with tab1:
        render_available_problem_sets()
    
    with tab2:
        render_create_problem_set()
    
    with tab3:
        render_generate_problem_set()
    
    with tab4:
        render_problem_set_statistics()


def render_available_problem_sets():
    """Render the available problem sets tab."""
    st.subheader("Available Problem Sets")
    
    problem_sets = st.session_state.operations.list_problem_sets()
    if not problem_sets:
        st.info("No problem sets available.")
        return
    
    # Display problem sets
    for i, name in enumerate(problem_sets):
        col1, col2, col3 = st.columns([3, 1, 1])
        
        with col1:
            st.write(f"{i+1}. {name}")
        
        with col2:
            if st.button("Load", key=f"load_{i}"):
                problem_set = st.session_state.operations.load_problem_set(name)
                if problem_set:
                    st.success(f"Problem set '{name}' loaded successfully.")
                    st.session_state.current_problem_index = 0
                else:
                    st.error(f"Failed to load problem set '{name}'.")
        
        with col3:
            if st.button("Delete", key=f"delete_{i}"):
                success = st.session_state.operations.storage.delete_problem_set(name)
                if success:
                    st.success(f"Problem set '{name}' deleted successfully.")
                    # Reset current problem set if it was the deleted one
                    if (st.session_state.operations.current_problem_set and 
                        st.session_state.operations.current_problem_set.name == name):
                        st.session_state.operations.current_problem_set = None
                else:
                    st.error(f"Failed to delete problem set '{name}'.")


def render_create_problem_set():
    """Render the create problem set tab."""
    st.subheader("Create a New Problem Set")
    
    name = st.text_input("Problem Set Name")
    description = st.text_area("Description (optional)")
    
    if st.button("Create Problem Set"):
        if not name:
            st.error("Please enter a name for the problem set.")
            return
        
        problem_set = st.session_state.operations.create_problem_set(name, description)
        if problem_set:
            st.session_state.operations.save_current_problem_set()
            st.success(f"Problem set '{name}' created successfully.")
            st.session_state.current_problem_index = 0
        else:
            st.error("Failed to create problem set.")


def render_generate_problem_set():
    """Render the generate problem set tab."""
    st.subheader("Generate a Random Problem Set")
    
    name = st.text_input("Problem Set Name", key="gen_name")
    description = st.text_area("Description (optional)", key="gen_desc")
    
    num_problems = st.slider("Number of Problems", min_value=1, max_value=50, value=10)
    
    difficulty = st.selectbox(
        "Difficulty",
        ["easy", "medium", "hard"],
        format_func=lambda x: x.capitalize()
    )
    
    operators = st.multiselect(
        "Operators",
        ["+", "-", "*", "/"],
        default=["+", "-", "*", "/"]
    )
    
    if st.button("Generate Problem Set"):
        if not name:
            st.error("Please enter a name for the problem set.")
            return
        
        if not operators:
            st.error("Please select at least one operator.")
            return
        
        problem_set = st.session_state.operations.generate_problem_set(
            name, num_problems, difficulty, operators, description
        )
        
        if problem_set:
            st.session_state.operations.save_current_problem_set()
            st.success(f"Problem set '{name}' with {num_problems} problems generated successfully.")
            st.session_state.current_problem_index = 0
        else:
            st.error("Failed to generate problem set.")


def render_problem_set_statistics():
    """Render the problem set statistics tab."""
    if not st.session_state.operations.current_problem_set:
        st.warning("No problem set loaded. Please load or create a problem set first.")
        return
    
    stats = st.session_state.operations.get_statistics()
    
    st.subheader(f"Statistics for '{st.session_state.operations.current_problem_set.name}'")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Total Problems", stats["total_problems"])
        st.metric("Attempted", stats["attempted"])
    
    with col2:
        st.metric("Correct", stats["correct"])
        st.metric("Accuracy", f"{stats['accuracy']:.1f}%")
    
    # Chart for operator breakdown
    if stats['by_operator']:
        st.subheader("By Operator")
        
        # Prepare data for chart
        import pandas as pd
        import altair as alt
        
        operator_data = []
        for op, op_stats in stats['by_operator'].items():
            if op_stats['total'] > 0:
                operator_data.append({
                    "Operator": op,
                    "Total": op_stats['total'],
                    "Attempted": op_stats['attempted'],
                    "Correct": op_stats['correct'],
                    "Accuracy": op_stats['accuracy']
                })
        
        if operator_data:
            df = pd.DataFrame(operator_data)
            
            # Bar chart for count by operator
            count_chart = alt.Chart(df).mark_bar().encode(
                x=alt.X('Operator:N', title='Operator'),
                y=alt.Y('Total:Q', title='Count'),
                color='Operator:N'
            ).properties(
                title='Problems by Operator',
                width=300,
                height=200
            )
            
            # Bar chart for accuracy by operator
            accuracy_chart = alt.Chart(df).mark_bar().encode(
                x=alt.X('Operator:N', title='Operator'),
                y=alt.Y('Accuracy:Q', title='Accuracy (%)'),
                color='Operator:N'
            ).properties(
                title='Accuracy by Operator',
                width=300,
                height=200
            )
            
            # Display charts side by side
            st.altair_chart(alt.hconcat(count_chart, accuracy_chart), use_container_width=True)
            
            # Display data table
            st.dataframe(df)


def render_timed_drill():
    """Render the timed drill page."""
    st.title("Timed Drill ⏱️")
    
    if not st.session_state.drill_problems:
        # Drill setup
        st.markdown("""
        Complete a set of problems as quickly as possible.
        Configure your drill and click "Start Drill" when ready.
        """)
        
        col1, col2 = st.columns(2)
        
        with col1:
            num_problems = st.slider("Number of Problems", min_value=5, max_value=50, value=20)
            
            difficulty = st.selectbox(
                "Difficulty",
                ["easy", "medium", "hard"],
                format_func=lambda x: x.capitalize(),
                key="drill_difficulty"
            )
        
        with col2:
            operators = st.multiselect(
                "Operators",
                ["+", "-", "*", "/"],
                default=["+", "-", "*", "/"],
                key="drill_operators"
            )
        
        if st.button("Start Drill"):
            if not operators:
                st.error("Please select at least one operator.")
                return
            
            # Generate problems
            st.session_state.drill_problems = []
            for _ in range(num_problems):
                problem = st.session_state.operations.generate_random_problem(difficulty, operators)
                st.session_state.drill_problems.append(problem)
            
            st.session_state.drill_start_time = time.time()
            st.session_state.drill_answers = [None] * len(st.session_state.drill_problems)
            st.session_state.drill_completed = False
            st.experimental_rerun()
    
    else:
        # Drill in progress
        if not st.session_state.drill_completed:
            # Display elapsed time
            elapsed_time = int(time.time() - st.session_state.drill_start_time)
            st.write(f"⏱️ Time elapsed: {format_time(elapsed_time)}")
            
            # Progress bar
            answered = sum(1 for a in st.session_state.drill_answers if a is not None)
            progress = answered / len(st.session_state.drill_problems)
            st.progress(progress)
            
            # Display problems
            st.subheader(f"Solve {len(st.session_state.drill_problems)} Problems")
            
            for i, problem in enumerate(st.session_state.drill_problems):
                col1, col2 = st.columns([3, 2])
                
                with col1:
                    st.write(f"{i+1}. {problem.show_problem_to_solve()}")
                
                with col2:
                    key = f"drill_answer_{i}"
                    answer = st.number_input("Answer", key=key, label_visibility="collapsed")
                    
                    if answer != 0 or st.session_state.get(key + "_submitted", False):
                        st.session_state[key + "_submitted"] = True
                        st.session_state.drill_answers[i] = answer
            
            # Complete button
            if st.button("Complete Drill"):
                st.session_state.drill_completed = True
                st.experimental_rerun()
        
        else:
            # Drill completed
            end_time = time.time()
            elapsed_time = int(end_time - st.session_state.drill_start_time)
            
            st.success(f"Drill completed in {format_time(elapsed_time)}!")
            
            # Calculate results
            correct = 0
            results = []
            
            for i, problem in enumerate(st.session_state.drill_problems):
                answer = st.session_state.drill_answers[i]
                is_correct = answer is not None and problem.check_answer(answer)
                
                if is_correct:
                    correct += 1
                
                results.append({
                    "problem": str(problem),
                    "user_answer": answer,
                    "correct": is_correct
                })
            
            # Display score
            st.subheader("Results")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Time", format_time(elapsed_time))
            
            with col2:
                st.metric("Score", f"{correct}/{len(st.session_state.drill_problems)}")
            
            with col3:
                accuracy = correct / len(st.session_state.drill_problems) * 100
                st.metric("Accuracy", f"{accuracy:.1f}%")
            
            # Display results table
            import pandas as pd
            
            df = pd.DataFrame(results)
            st.dataframe(df)
            
            # Performance feedback
            if correct == len(st.session_state.drill_problems):
                st.balloons()
                st.success("Perfect score! Excellent work! 🎉")
            elif correct >= len(st.session_state.drill_problems) * 0.8:
                st.success("Great job! 👍")
            elif correct >= len(st.session_state.drill_problems) * 0.6:
                st.info("Good effort! Keep practicing. 👍")
            else:
                st.warning("Keep practicing to improve your skills! 💪")
            
            # Save as problem set
            if st.button("Save as Problem Set"):
                name = st.text_input("Problem Set Name", value=f"Drill {format_time(elapsed_time)}")
                description = f"Timed drill - {format_time(elapsed_time)} - {correct}/{len(st.session_state.drill_problems)}"
                
                if name:
                    problem_set = st.session_state.operations.create_problem_set(name, description)
                    
                    for i, problem in enumerate(st.session_state.drill_problems):
                        # Set user answer
                        problem.user_answer = st.session_state.drill_answers[i]
                        st.session_state.operations.add_problem(problem)
                    
                    st.session_state.operations.save_current_problem_set()
                    st.success(f"Problem set '{name}' saved successfully.")
            
            # New drill button
            if st.button("New Drill"):
                st.session_state.drill_problems = []
                st.session_state.drill_start_time = None
                st.session_state.drill_answers = []
                st.session_state.drill_completed = False
                st.experimental_rerun()


def main():
    """Main entry point for the Streamlit application."""
    # Initialize session state
    initialize_session_state()
    
    # Render sidebar and get selected page
    page = render_sidebar()
    
    # Render selected page
    if page == "Home":
        render_home_page()
    elif page == "Answer Checker":
        render_answer_checker()
    elif page == "Memory Bank":
        render_memory_bank()
    elif page == "Problem Sets":
        render_problem_sets()
    elif page == "Timed Drill":
        render_timed_drill()


if __name__ == "__main__":
    main()