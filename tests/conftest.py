"""
Pytest configuration for skill tests
"""

import pytest


def pytest_configure(config):
    """Add custom markers"""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests requiring network"
    )


@pytest.fixture
def sparql_endpoint():
    """SPARQL endpoint URL"""
    return "https://datos.bcn.cl/sparql"


@pytest.fixture
def resource_base():
    """Resource base URL"""
    return "https://datos.bcn.cl/recurso"
