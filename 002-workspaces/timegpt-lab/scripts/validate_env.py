#!/usr/bin/env python3
"""
TimeGPT Lab Environment Validation Script

Validates that the TimeGPT lab environment is correctly configured.
Does NOT make any network calls or contact the TimeGPT API.

Usage:
    python scripts/validate_env.py

Exit codes:
    0: All validations passed
    1: One or more validations failed
"""

import os
import sys
from importlib import import_module


def check_python_version():
    """Check if Python version is >= 3.9"""
    major, minor = sys.version_info[:2]

    if major < 3 or (major == 3 and minor < 9):
        print(f"✗ Python {major}.{minor}.x (unsupported - requires Python 3.9+)")
        return False

    print(f"✓ Python {major}.{minor}.{sys.version_info.micro} (supported)")
    return True


def check_env_var(var_name):
    """Check if environment variable is set (without exposing value)"""
    value = os.getenv(var_name)

    if not value:
        print(f"✗ {var_name} environment variable NOT set")
        return False

    # Show only first 4 chars for security
    masked = value[:4] + "..." if len(value) > 4 else "***"
    print(f"✓ {var_name} environment variable present ({masked})")
    return True


def check_package(package_name, min_version=None):
    """Check if a Python package is installed"""
    try:
        module = import_module(package_name)
        version = getattr(module, "__version__", "unknown")

        version_info = f" (version {version})" if version != "unknown" else ""
        print(f"✓ {package_name} package installed{version_info}")
        return True

    except ImportError:
        print(f"✗ {package_name} package NOT installed")
        return False


def main():
    """Run all environment validations"""
    print("TimeGPT Lab Environment Validation")
    print("=" * 50)
    print()

    checks = []

    # Python version check
    checks.append(check_python_version())

    # Environment variable check
    checks.append(check_env_var("NIXTLA_TIMEGPT_API_KEY"))

    # Optional env var (don't fail if missing)
    nixtla_env = os.getenv("NIXTLA_ENV", "not set")
    print(f"  NIXTLA_ENV: {nixtla_env} (optional)")

    print()

    # Package checks
    print("Checking required packages...")
    checks.append(check_package("nixtla"))
    checks.append(check_package("utilsforecast"))
    checks.append(check_package("pandas"))

    print()
    print("=" * 50)

    if all(checks):
        print("✓ Environment validation: PASSED")
        print()
        print("Next steps:")
        print("  1. Review docs/timegpt-env-setup.md for usage guidance")
        print("  2. Explore scripts/ for TimeGPT workflows")
        print("  3. Run smoke tests: python scripts/timegpt_smoke_placeholder.py")
        return 0
    else:
        print("✗ Environment validation: FAILED")
        print()
        print("Please review the errors above and:")
        print("  1. Install missing packages: pip install nixtla utilsforecast pandas")
        print("  2. Set NIXTLA_TIMEGPT_API_KEY: export NIXTLA_TIMEGPT_API_KEY='your_key'")
        print("  3. See docs/timegpt-env-setup.md for detailed setup instructions")
        return 1


if __name__ == "__main__":
    sys.exit(main())
