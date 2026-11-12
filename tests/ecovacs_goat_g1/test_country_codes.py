"""Tests for ECOVACS country-code/API-code mapping helpers."""

from pathlib import Path
import sys
import types

import pytest

PACKAGE_PATH = Path(__file__).parents[2] / "custom_components" / "ecovacs_goat_g1"

custom_components = types.ModuleType("custom_components")
custom_components.__path__ = [str(PACKAGE_PATH.parent)]
sys.modules.setdefault("custom_components", custom_components)

ecovacs_goat_g1 = types.ModuleType("custom_components.ecovacs_goat_g1")
ecovacs_goat_g1.__path__ = [str(PACKAGE_PATH)]
sys.modules.setdefault("custom_components.ecovacs_goat_g1", ecovacs_goat_g1)

from custom_components.ecovacs_goat_g1.mower_api import (
    continent_data_center,
    country_api_code,
    country_continent,
)


@pytest.mark.parametrize(
    ("country", "expected"),
    [
        ("GB", "uk"),
        ("gb", "uk"),
        ("US", "us"),
        ("DE", "de"),
        ("CN", "cn"),
    ],
)
def test_country_api_code_maps_gb_to_uk(country: str, expected: str) -> None:
    """`GB` is rewritten to the `uk` code the API expects; others just lowercase."""
    assert country_api_code(country) == expected


@pytest.mark.parametrize(
    ("country", "expected"),
    [("NZ", "na"), ("US", "na"), ("DE", "eu")],
)
def test_data_center_never_uses_ww(country: str, expected: str) -> None:
    """Non-EU accounts use the na data center; api-base.dc-ww does not exist."""
    assert continent_data_center(country_continent(country)) == expected
