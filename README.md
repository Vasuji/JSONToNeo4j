# JSON To Neo4j

This is a script that reads from a json file output by [Dibakar](https://github.com/Vasuji)'s Clinical Case Report parser.
## Prerequisite
Python 3.3+, neo4j 3.3.x, neomodel package

## Format

The format of the JSON file is

```python
{
    "nodes": [
        {
            "id": str,
            "type": str,
            "name": str,
            "icolor": str,
            "degree": int
        },
        ...
    ],
    "links": [
        {            
            "id": str,
            "name": str,
            "value": float,
            "source": str,
            "source_name": str,
            "target": str,
            "target_name": str
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