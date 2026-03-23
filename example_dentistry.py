from ontology_engine import OntologyEngine
import json

def run_dentistry_example():
    # Initialize engine with default file ontology.db
    engine = OntologyEngine("sqlite:///dentistry_ontology.db")

    # 1. Set version
    print("Setting ontology version...")
    engine.set_version("v1.0-dentistry", "Taxonomía básica de odontología")

    # 2. Create nodes (General concepts)
    print("Creating ontology nodes...")
    patologia_id = engine.create_node("Patología", {"domain": "Odontología", "scope": "General"})
    periodoncia_id = engine.create_node("Periodoncia", {"specialty": "True"})
    gingivitis_id = engine.create_node("Gingivitis", {"type": "Inflamatoria", "severity": "Moderate"})
    periodontitis_id = engine.create_node("Periodontitis", {"type": "Destructiva", "severity": "High"})
    caries_id = engine.create_node("Caries", {"type": "Bacteriana"})

    # 3. Establish relationships with weights
    print("Establishing relationships...")

    # Hierarchical relations (Parent -> Child)
    # Patología -> Periodoncia (Weight 1.0)
    engine.create_relationship(patologia_id, periodoncia_id, "hierarchical", weight=1.0)

    # Periodoncia -> Gingivitis (Weight 0.9)
    engine.create_relationship(periodoncia_id, gingivitis_id, "hierarchical", weight=0.9)

    # Periodoncia -> Periodontitis (Weight 0.95)
    engine.create_relationship(periodoncia_id, periodontitis_id, "hierarchical", weight=0.95)

    # Cross-correlations (Lateral relationships)
    # Gingivitis can lead to Periodontitis (Correlation)
    engine.create_relationship(gingivitis_id, periodontitis_id, "correlation", weight=0.75)

    # 4. Query data
    print("\n--- Current Ontology Nodes (v1.0-dentistry) ---")
    nodes = engine.get_version_nodes("v1.0-dentistry")
    for node in nodes:
        print(f"ID: {node['id']} | Name: {node['name']} | Metadata: {node['metadata']}")

    # 5. Audit logs
    print("\n--- Recent Audit Logs (Last 5) ---")
    logs = engine.get_logs()
    for log in logs[:5]:
        print(f"[{log['timestamp']}] Action: {log['action']} | Entity: {log['entity']} | ID: {log['id']}")

if __name__ == "__main__":
    run_dentistry_example()
