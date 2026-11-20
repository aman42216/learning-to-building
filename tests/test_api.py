
import importlib.util
import sys
from pathlib import Path

from fastapi.testclient import TestClient

# Project paths
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DAY08_APP = PROJECT_ROOT / "Day-08" / "app"

# Add Day-08 app folder to Python path
sys.path.insert(0, str(DAY08_APP))


# Remove previously imported modules
sys.modules.pop("main", None)
sys.modules.pop("rag", None)


# Load the exact Day-08 rag.py file
rag_path = DAY08_APP / "rag.py"

rag_spec = importlib.util.spec_from_file_location(
    "rag",
    rag_path
)

rag = importlib.util.module_from_spec(rag_spec)
sys.modules["rag"] = rag
rag_spec.loader.exec_module(rag)


# Load the exact Day-08 main.py file
main_path = DAY08_APP / "main.py"

main_spec = importlib.util.spec_from_file_location(
    "day08_main",
    main_path
)

main = importlib.util.module_from_spec(main_spec)
sys.modules["day08_main"] = main
main_spec.loader.exec_module(main)

app = main.app

client = TestClient(app)


# Display registered routes for verification
print("\nDAY-08 REGISTERED ROUTES:")
for route in app.routes:
    print(route.path, route.methods)


# Test 1: Health endpoint status code
def test_health_endpoint_status_code():
    response = client.get("/health")

    assert response.status_code == 200


# Test 2: Health endpoint response
def test_health_endpoint_response():
    response = client.get("/health")

    assert response.json() == {
        "status": "healthy",
        "service": "ShramikSathi RAG API"
    }


# Test 3: Ask endpoint with fake LLM
def test_ask_endpoint_with_fake_llm(monkeypatch):

    class FakeCollection:
        def count(self):
            return 1

    monkeypatch.setattr(
        rag,
        "get_collection",
        lambda: FakeCollection()
    )

    monkeypatch.setattr(
        rag,
        "semantic_search",
        lambda collection, question, top_k: {
            "documents": [["Official gratuity information"]],
            "metadatas": [[{
                "title": "Test Labour FAQ",
                "source": "test.json",
                "page": 1
            }]],
            "distances": [[0.2]]
        }
    )

    monkeypatch.setattr(
        rag,
        "generate_response",
        lambda prompt, system_prompt:
            "Gratuity is calculated using the applicable formula."
    )

    response = client.post(
        "/ask",
        json={
            "question": "How is gratuity calculated?"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["answerable"] is True
    assert "Gratuity" in data["answer"]
    assert len(data["citations"]) == 1


# Test 4: Reject whitespace-only question
def test_ask_endpoint_rejects_whitespace_question():
    response = client.post(
        "/ask",
        json={
            "question": "   "
        }
    )

    assert response.status_code == 400
