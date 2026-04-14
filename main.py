import argparse
from generator import generate_test, suggest_fix
from validator import validate_pytest


def main():
    parser = argparse.ArgumentParser(description="LLM Test Case Generator")
    parser.add_argument("--input", required=True, help="Function or user story to test")
    parser.add_argument("--format", default="pytest", choices=["pytest", "xctest"])
    parser.add_argument("--validate", action="store_true", help="Run generated tests")
    parser.add_argument("--fix", action="store_true", help="Auto fix failing tests")
    args = parser.parse_args()

    print("Generating tests...")
    tests = generate_test(args.input, args.format)
    print("\n--- Generated Tests ---\n")
    print(tests)

    if args.validate and args.format == "pytest":
        print("\n--- Validation Results ---\n")
        results = validate_pytest(tests)
        print(results["output"])

        if not results["passed"] and args.fix:
            print("\n--- Suggest Fixes ---\n")
            fix = suggest_fix(tests, results["errors"])
            print(fix)


if __name__ == "__main__":
    main()
