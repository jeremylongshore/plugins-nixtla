#!/usr/bin/env python3
"""
Nixtla Baseline Lab - Golden Task Test Runner

Implements the smoke test defined in tests/golden_tasks/baseline_m4_smoke.yaml.

This script:
1. Runs the MCP server in test mode
2. Verifies output files are generated correctly
3. Validates CSV schema and metrics
4. Ensures summary file contains expected content

Exit codes:
- 0: All checks passed
- 1: Test failed (with error message)

Usage:
    python3 tests/run_baseline_m4_smoke.py

Requirements:
- Working directory: plugins/nixtla-baseline-lab/
- Dependencies installed (statsforecast, datasetsforecast, pandas, numpy)
"""

import subprocess
import sys
import os
import json
from pathlib import Path
import csv


def main():
    """Run the golden task smoke test."""
    print("=" * 60)
    print("Nixtla Baseline Lab - Golden Task Smoke Test")
    print("=" * 60)
    print()

    # Step 1: Run MCP test
    print("[1/5] Running MCP test (horizon=7, series_limit=5)...")
    result = run_mcp_test()
    if not result:
        return 1

    # Step 2: Verify output directory
    print("[2/5] Verifying output directory...")
    output_dir = Path("nixtla_baseline_m4_test")
    if not output_dir.exists():
        print(f"FAIL: Output directory {output_dir} does not exist")
        return 1
    print(f"✓ Found output directory: {output_dir}/")

    # Step 3: Validate CSV file
    print("[3/5] Validating results CSV...")
    csv_file = output_dir / "results_M4_Daily_h7.csv"
    if not validate_csv(csv_file):
        return 1

    # Step 4: Validate summary file
    print("[4/5] Validating summary file...")
    summary_file = output_dir / "summary_M4_Daily_h7.txt"
    if not validate_summary(summary_file):
        return 1

    # Step 5: Final checks
    print("[5/5] Running final checks...")
    print("✓ All validations passed")
    print()
    print("=" * 60)
    print("GOLDEN TASK PASSED")
    print("=" * 60)
    return 0


def run_mcp_test():
    """Run the MCP server in test mode."""
    try:
        result = subprocess.run(
            ["python3", "scripts/nixtla_baseline_mcp.py", "test"],
            capture_output=True,
            text=True,
            timeout=120,  # 2 minute timeout
        )

        if result.returncode != 0:
            print(f"FAIL: MCP test exited with code {result.returncode}")
            print(f"STDERR: {result.stderr}")
            return False

        # Parse JSON output (extract first JSON object from output)
        try:
            # Find the first '{' and extract until matching '}'
            stdout = result.stdout
            start = stdout.find('{')
            if start == -1:
                print(f"FAIL: No JSON found in MCP output")
                print(f"Output: {stdout[:500]}")
                return False

            # Count braces to find matching closing brace
            brace_count = 0
            end = start
            for i, char in enumerate(stdout[start:], start=start):
                if char == '{':
                    brace_count += 1
                elif char == '}':
                    brace_count -= 1
                    if brace_count == 0:
                        end = i + 1
                        break

            json_str = stdout[start:end]
            output_data = json.loads(json_str)

            if not output_data.get("success"):
                print(f"FAIL: MCP test reported failure")
                print(f"Message: {output_data.get('message', 'No message')}")
                return False
        except (json.JSONDecodeError, IndexError) as e:
            print(f"FAIL: Could not parse MCP test output")
            print(f"Error: {e}")
            print(f"Output: {result.stdout[:500]}")
            return False

        print("✓ MCP test completed successfully")
        return True

    except subprocess.TimeoutExpired:
        print("FAIL: MCP test timed out after 120 seconds")
        return False
    except Exception as e:
        print(f"FAIL: MCP test raised exception: {e}")
        return False


def validate_csv(csv_file):
    """Validate the results CSV file."""
    if not csv_file.exists():
        print(f"FAIL: CSV file {csv_file} does not exist")
        return False

    print(f"✓ Found CSV: {csv_file}")

    # Check file size
    file_size = csv_file.stat().st_size
    if file_size < 100:
        print(f"FAIL: CSV file is too small ({file_size} bytes, expected > 100)")
        return False
    print(f"✓ CSV file size: {file_size} bytes")

    # Parse and validate CSV
    try:
        with open(csv_file, 'r') as f:
            reader = csv.DictReader(f)

            # Validate header
            expected_columns = {'series_id', 'model', 'sMAPE', 'MASE'}
            actual_columns = set(reader.fieldnames or [])
            if actual_columns != expected_columns:
                print(f"FAIL: CSV columns mismatch")
                print(f"  Expected: {expected_columns}")
                print(f"  Actual: {actual_columns}")
                return False
            print(f"✓ CSV columns: {', '.join(expected_columns)}")

            # Validate rows
            rows = list(reader)
            row_count = len(rows)

            # Should have 5 series × 3 models = 15 rows
            if row_count < 15:
                print(f"FAIL: CSV has only {row_count} rows (expected >= 15)")
                return False
            print(f"✓ CSV row count: {row_count} (>= 15)")

            # Validate model names
            models_found = set()
            for row in rows:
                models_found.add(row['model'])

            expected_models = {'SeasonalNaive', 'AutoETS', 'AutoTheta'}
            if not expected_models.issubset(models_found):
                print(f"FAIL: Missing models")
                print(f"  Expected: {expected_models}")
                print(f"  Found: {models_found}")
                return False
            print(f"✓ Models present: {', '.join(expected_models)}")

            # Validate metrics
            for row in rows:
                series_id = row['series_id']
                model = row['model']

                try:
                    smape = float(row['sMAPE'])
                    mase = float(row['MASE'])
                except ValueError as e:
                    print(f"FAIL: Invalid metric value for {series_id}/{model}: {e}")
                    return False

                # sMAPE should be in (0, 200)
                if not (0 < smape < 200):
                    print(f"FAIL: Invalid sMAPE for {series_id}/{model}: {smape} (should be 0 < sMAPE < 200)")
                    return False

                # MASE should be > 0
                if not (mase > 0):
                    print(f"FAIL: Invalid MASE for {series_id}/{model}: {mase} (should be > 0)")
                    return False

            print("✓ All metrics in valid ranges")

    except Exception as e:
        print(f"FAIL: Error reading/parsing CSV: {e}")
        return False

    return True


def validate_summary(summary_file):
    """Validate the summary text file."""
    if not summary_file.exists():
        print(f"FAIL: Summary file {summary_file} does not exist")
        return False

    print(f"✓ Found summary: {summary_file}")

    try:
        content = summary_file.read_text()

        # Check for required strings
        required_strings = [
            "M4-Daily",
            "SeasonalNaive",
            "AutoETS",
            "AutoTheta",
            "sMAPE",
            "MASE"
        ]

        missing = []
        for required in required_strings:
            if required not in content:
                missing.append(required)

        if missing:
            print(f"FAIL: Summary file missing required content: {', '.join(missing)}")
            return False

        print(f"✓ Summary contains all required strings")

    except Exception as e:
        print(f"FAIL: Error reading summary file: {e}")
        return False

    return True


if __name__ == "__main__":
    sys.exit(main())
