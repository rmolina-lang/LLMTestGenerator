import re
import ollama


def _strip_markdown_fences(text: str) -> str:
    text = re.sub(r"```(?:python)?", "", text)
    lines = text.splitlines()
    code_start = next(
        (i for i, l in enumerate(lines) if l.startswith("import ") or l.startswith("from ")),
        0
    )
    lines = lines[code_start:]
    lines = [l for l in lines if l.strip() != "```"]
    return "\n".join(lines).strip()


def generate_test(input_text: str, format: str = "pytest") -> str:
    if format == "pytest":
        prompt = f"""You are a Python test engineer. Output ONLY valid Python code. No prose, no comments, no markdown.

Rules:
- Import pytest at the top
- Do not import from any external module — define the function under test as a stub directly in the file
- The stub must have a real implementation (not just `pass`) so the assertions can produce a result
- Write test functions named test_<function_name>, test_<function_name>_edge, etc.
- Cover: normal values, zero, negative numbers, None inputs, empty strings, boundary values
- Use only assert statements and pytest.raises
- Every assert must use a concrete expected value computed from the stub logic
- Do not include any text, comments, or prose outside the Python code

Function to test:
{input_text}"""
    elif format == "xctest":
        prompt = f"""You are an iOS test engineer. Output ONLY valid Swift code. No prose, no comments, no markdown.

Rules:
- Import XCTest
- Wrap tests in a class extending XCTestCase
- Use XCTAssertEqual, XCTAssertTrue, XCTAssertNil
- Include setUp and tearDown methods
- Cover normal cases, edge cases (nil, zero, negative, boundary values)
- Do not include any text outside the Swift code

Function to test:
{input_text}"""
    else:
        raise ValueError(f"Unsupported format: {format!r}")

    response = ollama.chat(
        model="mistral",
        messages=[{"role": "user", "content": prompt}]
    )

    return _strip_markdown_fences(response.message.content)


def suggest_fix(test_code: str, error_log: str) -> str:
    prompt = f"""You are a Python test engineer. Output ONLY valid Python code. No prose, no comments, no markdown.

The test code below has failures. Fix it so all tests pass based on the error log.
- Keep the same test structure
- Fix syntax errors, wrong assertions, and missing imports
- Do not include any text outside the Python code

Test Code:
{test_code}

Error Log:
{error_log}"""

    response = ollama.chat(
        model="mistral",
        messages=[{"role": "user", "content": prompt}]
    )

    return _strip_markdown_fences(response.message.content)
