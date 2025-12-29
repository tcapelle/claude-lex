"""
Tests for the LeyChile skill

Tests are organized following Claude's skill testing recommendations:
1. Triggering Tests - Does the skill activate correctly?
2. Functional Tests - Does it produce expected outputs?
3. API Smoke Tests - Are the underlying APIs working?

See: https://www.claude.com/blog/how-to-create-skills-key-steps-limitations-and-examples
"""

import pytest
import requests
from requests.exceptions import ReadTimeout, ConnectionError

SPARQL_ENDPOINT = "https://datos.bcn.cl/sparql"
RESOURCE_BASE = "https://datos.bcn.cl/recurso"
# Note: BCN SPARQL endpoint can be slow under load
TIMEOUT = 60


def sparql_query(query, timeout=TIMEOUT):
    """Execute SPARQL query with error handling for flaky endpoint"""
    try:
        response = requests.post(
            SPARQL_ENDPOINT,
            data={"query": query},
            headers={"Accept": "application/json"},
            timeout=timeout,
        )
        return response
    except (ReadTimeout, ConnectionError) as e:
        pytest.skip(f"BCN SPARQL endpoint timeout/unavailable: {e}")


# =============================================================================
# TRIGGERING TESTS
# =============================================================================
# These document when the skill SHOULD and SHOULD NOT activate.
# Run these manually by testing the prompts with Claude.

class TestTriggeringExamples:
    """
    Examples of prompts that should/shouldn't trigger the leychile skill.

    These aren't automated tests - they're documentation for manual testing
    and for improving the skill's description.
    """

    # Prompts that SHOULD trigger the skill
    SHOULD_TRIGGER = [
        # Explicit invocations
        "/leychile busca leyes sobre teletrabajo",
        "/leychile que dice el codigo civil sobre compraventa",

        # Natural language - Chilean law references
        "Que dice la ley 19.628 sobre proteccion de datos?",
        "Busca el articulo 1545 del Codigo Civil",
        "Muestrame la Constitucion de Chile",
        "Que leyes regulan el trabajo remoto en Chile?",
        "Busca decretos sobre medio ambiente",
        "Cual es el Codigo del Trabajo chileno?",
        "Necesito informacion sobre la ley de pension alimenticia",

        # Specific law IDs
        "Muestrame la ley con idNorma 172986",
        "Busca la norma 242302",
    ]

    # Prompts that should NOT trigger the skill
    SHOULD_NOT_TRIGGER = [
        # Other countries' laws
        "What does US copyright law say?",
        "Busca leyes de Argentina sobre trabajo",
        "Mexican labor code",

        # General legal questions (not Chilean specific)
        "What is contract law?",
        "Explain habeas corpus",
        "Define tort",

        # Other tasks
        "Write a Python function",
        "Summarize this document",
        "Help me with my resume",

        # Ambiguous - might need clarification
        "What are labor laws?",  # Which country?
    ]

    def test_trigger_examples_documented(self):
        """Verify trigger examples are defined"""
        assert len(self.SHOULD_TRIGGER) > 0
        assert len(self.SHOULD_NOT_TRIGGER) > 0


# =============================================================================
# FUNCTIONAL TESTS
# =============================================================================
# These verify the skill produces expected outputs for typical requests.

class TestFunctionalExamples:
    """
    Expected behaviors when the skill is triggered.

    These document what output Claude should produce.
    """

    EXPECTED_BEHAVIORS = [
        {
            "input": "/leychile busca proyectos de ley",
            "should_contain": ["ProyectoDeLey", "SPARQL"],
            "should_do": "Execute a SPARQL query for bcn:ProyectoDeLey",
        },
        {
            "input": "Que dice el Codigo Civil?",
            "should_contain": ["172986", "Codigo Civil"],
            "should_do": "Query for idNorma 172986 or provide link to bcn.cl",
        },
        {
            "input": "/leychile constitucion articulo 1",
            "should_contain": ["242302", "Constitucion"],
            "should_do": "Reference Constitution idNorma 242302",
        },
    ]

    def test_behaviors_documented(self):
        """Verify expected behaviors are defined"""
        assert len(self.EXPECTED_BEHAVIORS) > 0
        for behavior in self.EXPECTED_BEHAVIORS:
            assert "input" in behavior
            assert "should_do" in behavior


# =============================================================================
# EDGE CASE TESTS
# =============================================================================

class TestEdgeCases:
    """Edge cases the skill should handle gracefully"""

    EDGE_CASES = [
        {
            "input": "/leychile",  # No query provided
            "expected": "Should ask what law to search for",
        },
        {
            "input": "/leychile ley 99999999",  # Non-existent law
            "expected": "Should report no results found",
        },
        {
            "input": "/leychile @#$%^&",  # Invalid input
            "expected": "Should handle gracefully, ask for clarification",
        },
        {
            "input": "busca la ley de xxxxxx en chile",  # Vague topic
            "expected": "Should attempt search or ask for clarification",
        },
    ]

    def test_edge_cases_documented(self):
        """Verify edge cases are documented"""
        assert len(self.EDGE_CASES) > 0


# =============================================================================
# API SMOKE TESTS
# =============================================================================
# These verify the underlying APIs are still working.

class TestAPISmokeTests:
    """
    Smoke tests for the BCN APIs.

    These verify the external APIs the skill depends on are functioning.
    If these fail, the skill won't work regardless of triggering.
    """

    def test_sparql_endpoint_available(self):
        """SPARQL endpoint responds"""
        # Use a specific query - generic queries can timeout
        query = """
        PREFIX bcn: <http://datos.bcn.cl/ontologies/bcn-resources#>
        SELECT ?p WHERE { ?p a bcn:ProyectoDeLey } LIMIT 1
        """
        response = sparql_query(query)
        assert response.status_code == 200
        assert "results" in response.json()

    def test_can_query_norms(self):
        """Can query bcnnorms:Norm class"""
        query = """
        PREFIX bcnnorms: <http://datos.bcn.cl/ontologies/bcn-norms#>
        SELECT ?norma WHERE { ?norma a bcnnorms:Norm } LIMIT 1
        """
        response = sparql_query(query)
        assert response.status_code == 200
        assert len(response.json()["results"]["bindings"]) > 0

    def test_can_query_law_projects(self):
        """Can query bcn:ProyectoDeLey class"""
        query = """
        PREFIX bcn: <http://datos.bcn.cl/ontologies/bcn-resources#>
        SELECT ?p WHERE { ?p a bcn:ProyectoDeLey } LIMIT 1
        """
        response = sparql_query(query)
        assert response.status_code == 200
        assert len(response.json()["results"]["bindings"]) > 0

    def test_json_resource_available(self):
        """Can access JSON resources directly"""
        url = f"{RESOURCE_BASE}/cl/ley/330/datos.json"
        response = requests.get(url, timeout=TIMEOUT)
        assert response.status_code == 200
        assert len(response.json()) > 0

    def test_common_laws_exist(self):
        """Common Chilean laws are in the database"""
        common_laws = [
            ("Constitucion", 242302),
            ("Codigo Civil", 172986),
            ("Codigo Penal", 1984),
        ]
        for name, id_norma in common_laws:
            query = f"""
            PREFIX bcnnorms: <http://datos.bcn.cl/ontologies/bcn-norms#>
            SELECT ?n WHERE {{ ?n bcnnorms:leychileCode {id_norma} }} LIMIT 1
            """
            response = sparql_query(query)
            assert response.status_code == 200
            assert len(response.json()["results"]["bindings"]) > 0, f"{name} not found"


# =============================================================================
# DEPRECATION TESTS
# =============================================================================

class TestDeprecatedAPIs:
    """Verify deprecated APIs are still unavailable (so skill doesn't use them)"""

    def test_ley_facil_still_401(self):
        """Ley Facil API should still return 401"""
        response = requests.get(
            "https://www.bcn.cl/leyfacil/recurso/trabajo",
            timeout=TIMEOUT,
        )
        # If this starts returning 200, we could re-enable this API in the skill
        assert response.status_code == 401, "Ley Facil API may be available again!"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
