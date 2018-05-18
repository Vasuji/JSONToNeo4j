# JSON To Neo4j

This is a script that reads from a json file output by the script in the [Aztec-Network](https://github.com/BD2K-Aztec/Aztec-Network) repository.
## Prerequisite
Python 3.3+, neo4j 3.3.x, neomodel package

## Format

The format of the JSON file is

```python
{
    "nodes": [
        {
            "group": int,
            "id": str,
            "protein": str,
            "score": float
        },
        ...
    ],
    "links": [
        {
            "source": str,
            "target": str,
            "value": int
        },
        ...
    ]
}
```

Element of `nodes` or `links` represents a node or a relation in Neo4j respectively.

## Usage

1. Start your Neo4j database.

2. Put your database information in `dbConfig.py`.

3. Run the following command.

    ```bash
    python jsonToNeo4j.py yourFilename.json 
    ```

4. Now you can query results in Neo4j's console. For example:

    ```cypher
    MATCH (n) MATCH (n)-[r]-() RETURN n, r LIMIT 20;
    ```

## Limitations

* Almost no error checking
* Slow