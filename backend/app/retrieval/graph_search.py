from app.db.neo4j import driver


def search_graph(project_name: str):
    query = """
    MATCH (project:Project {name: $project_name})-[:USES]->(technology:Technology)
    RETURN technology.name AS technology
    ORDER BY technology.name
    """

    with driver.session() as session:
        result = session.run(
            query,
            project_name=project_name,
        )

        return [
            record["technology"]
            for record in result
        ]