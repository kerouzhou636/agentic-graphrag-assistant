from app.db.neo4j import driver


def create_sample_graph():
    query = """
    MERGE (project:Project {name: "Recommendation Engine"})
    MERGE (python:Technology {name: "Python"})
    MERGE (postgres:Technology {name: "PostgreSQL"})
    MERGE (kafka:Technology {name: "Kafka"})

    MERGE (project)-[:USES]->(python)
    MERGE (project)-[:USES]->(postgres)
    MERGE (project)-[:USES]->(kafka)
    """

    with driver.session() as session:
        session.run(query)


if __name__ == "__main__":
    create_sample_graph()
    print("Sample graph created.")