#!/usr/bin/env python3
import os
import sys
import subprocess


def run_command(command):
    """Run a command and print its output."""
    print(f"Running: {' '.join(command)}")
    result = subprocess.run(command, capture_output=True, text=True)
    print(result.stdout)
    
    if result.stderr:
        print(f"Errors: {result.stderr}")
    
    return result.returncode


def main():
    """Main function to run the mutation testing process."""
    print("==== Starting Mutation Testing ====")
    
    # Remove previous session file if it exists
    if os.path.exists("session.sqlite"):
        print("Removing previous session.sqlite file...")
        os.remove("session.sqlite")
    
    # Step 1: Initialize the mutation testing session
    print("\n==== Step 1: Initializing Mutation Testing Session ====")
    if run_command(["cosmic-ray", "init", "lab.toml", "session.sqlite"]) != 0:
        print("Error initializing mutation testing session.")
        return 1
    
    # Step 2: Show pending mutations
    print("\n==== Step 2: Showing Pending Mutations ====")
    run_command(["cr-report", "session.sqlite", "--show-pending"])
    
    # Step 3: Apply filters
    print("\n==== Step 3: Applying Filters ====")
    run_command(["cr-filter-operators", "session.sqlite", "lab.toml"])
    run_command(["cr-filter-pragma", "session.sqlite"])
    
    # Step 4: Execute mutation testing
    print("\n==== Step 4: Executing Mutation Testing ====")
    if run_command(["cosmic-ray", "exec", "lab.toml", "session.sqlite"]) != 0:
        print("Error executing mutation testing.")
        return 1
    
    # Step 5: Show results
    print("\n==== Step 5: Showing Mutation Testing Results ====")
    run_command(["cr-report", "session.sqlite", "--show-pending"])
    
    # Step 6: Generate HTML report
    print("\n==== Step 6: Generating HTML Report ====")
    with open("report.html", "w") as f:
        subprocess.run(["cr-html", "session.sqlite"], stdout=f, text=True)
    
    print("\n==== Mutation Testing Complete ====")
    print("Results have been saved to report.html")
    
    return 0


if __name__ == "__main__":
    sys.exit(main()) 