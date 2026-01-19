#!/usr/bin/env python3
"""
Test runner script for AI Story Weaver Pro.
Runs comprehensive integration tests for the complete platform.
"""
import sys
import subprocess
import argparse
from pathlib import Path


def run_command(command, description):
    """Run a command and return success status."""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Command: {' '.join(command)}")
    print('='*60)

    try:
        result = subprocess.run(command, capture_output=True, text=True, cwd=Path(__file__).parent)

        if result.returncode == 0:
            print("✓ SUCCESS")
            if result.stdout:
                print("Output:")
                print(result.stdout)
        else:
            print("✗ FAILED")
            print("Error output:")
            print(result.stderr)
            return False

        return True
    except Exception as e:
        print(f"✗ ERROR: {e}")
        return False


def main():
    """Main test runner function."""
    parser = argparse.ArgumentParser(description="AI Story Weaver Pro Test Runner")
    parser.add_argument("--unit", action="store_true", help="Run only unit tests")
    parser.add_argument("--integration", action="store_true", help="Run only integration tests")
    parser.add_argument("--e2e", action="store_true", help="Run only end-to-end tests")
    parser.add_argument("--coverage", action="store_true", help="Generate coverage report")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--fail-fast", action="store_true", help="Stop on first failure")

    args = parser.parse_args()

    # Base test command
    base_cmd = [sys.executable, "-m", "pytest"]

    if args.verbose:
        base_cmd.append("-v")

    if args.fail_fast:
        base_cmd.append("--tb=short")
    else:
        base_cmd.append("--tb=long")

    if args.coverage:
        base_cmd.extend([
            "--cov=app",
            "--cov-report=term-missing",
            "--cov-report=html:htmlcov",
            "--cov-fail-under=80"
        ])

    # Determine which tests to run
    if args.unit:
        test_paths = ["tests/test_database.py::TestDatabaseConnections"]
    elif args.integration:
        test_paths = ["tests/test_agents.py", "tests/test_api.py"]
    elif args.e2e:
        test_paths = ["tests/test_e2e.py"]
    else:
        # Run all tests
        test_paths = ["tests/"]

    success = True

    # Run database connection tests first
    if not args.unit and not args.e2e:
        print("\n🔍 Testing Database Connections...")
        db_cmd = base_cmd + ["tests/test_database.py::TestDatabaseConnections", "-v"]
        if not run_command(db_cmd, "Database Connection Tests"):
            success = False
            if args.fail_fast:
                return 1

    # Run database operations tests
    if not args.unit and not args.e2e:
        print("\n🗄️ Testing Database Operations...")
        db_ops_cmd = base_cmd + ["tests/test_database.py::TestDatabaseOperations", "-v"]
        if not run_command(db_ops_cmd, "Database Operations Tests"):
            success = False
            if args.fail_fast:
                return 1

    # Run agent integration tests
    if not args.unit and not args.e2e:
        print("\n🤖 Testing Agent Integration...")
        agent_cmd = base_cmd + ["tests/test_agents.py", "-v"]
        if not run_command(agent_cmd, "Agent Integration Tests"):
            success = False
            if args.fail_fast:
                return 1

    # Run API integration tests
    if not args.unit and not args.e2e:
        print("\n🌐 Testing API Integration...")
        api_cmd = base_cmd + ["tests/test_api.py", "-v"]
        if not run_command(api_cmd, "API Integration Tests"):
            success = False
            if args.fail_fast:
                return 1

    # Run end-to-end tests
    if not args.unit and not args.integration:
        print("\n🚀 Testing End-to-End Workflows...")
        e2e_cmd = base_cmd + ["tests/test_e2e.py", "-v"]
        if not run_command(e2e_cmd, "End-to-End Tests"):
            success = False
            if args.fail_fast:
                return 1

    # Run all tests together if no specific type requested
    if not any([args.unit, args.integration, args.e2e]):
        print("\n🧪 Running Complete Test Suite...")
        full_cmd = base_cmd + test_paths
        if not run_command(full_cmd, "Complete Test Suite"):
            success = False

    # Generate coverage report if requested
    if args.coverage and success:
        print("\n📊 Generating Coverage Report...")
        coverage_cmd = [sys.executable, "-m", "pytest", "--cov=app", "--cov-report=html:htmlcov", "tests/"]
        run_command(coverage_cmd, "Coverage Report Generation")

    # Final status
    print(f"\n{'='*60}")
    if success:
        print("🎉 ALL TESTS PASSED!")
        print("AI Story Weaver Pro integration tests completed successfully.")
        return 0
    else:
        print("❌ SOME TESTS FAILED!")
        print("Please review the test output above for details.")
        return 1


if __name__ == "__main__":
    sys.exit(main())