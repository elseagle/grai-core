import os
from itertools import chain

import pytest

from grai_source_snowflake.base import adapt_to_client, get_nodes_and_edges
from grai_source_snowflake.loader import SnowflakeConnector
from grai_source_snowflake.models import Column, Edge, Table

# Tests only run with a separate snowflake container deployed
# TODO: Mock the DB connection: https://blog.devgenius.io/creating-a-mock-database-for-unittesting-in-python-is-easier-than-you-think-c458e747224b

# @pytest.fixture
# def connection() -> SnowflakeConnector:
#     test_credentials = {
#         "host": "localhost",
#         "dbname": "docker",
#         "user": "docker",
#         "password": "docker",
#         "port": "5433",
#         "namespace": "test",
#         "account": "test",
#         "warehouse": "test",
#     }
#     connection = SnowflakeConnector(**test_credentials)
#     return connection
#
#
# @pytest.fixture
# def nodes_and_edges(connection):
#     nodes, edges = get_nodes_and_edges(connection, "v1")
#     return nodes, edges


@pytest.fixture
def v1_adapted_nodes(mock_get_nodes_and_edges):
    """

    Args:
        mock_get_nodes_and_edges:

    Returns:

    Raises:

    """
    return mock_get_nodes_and_edges[0]


@pytest.fixture
def v1_adapted_edges(mock_get_nodes_and_edges):
    """

    Args:
        mock_get_nodes_and_edges:

    Returns:

    Raises:

    """
    return mock_get_nodes_and_edges[1]


@pytest.fixture
def column_params():
    """ """
    column_params = [
        {
            "name": "test",
            "namespace": "test",
            "data_type": "integer",
            "is_nullable": True,
        },
        {
            "column_name": "test",
            "namespace": "test",
            "data_type": "integer",
            "is_nullable": True,
        },
        {
            "column_name": "test",
            "namespace": "test",
            "data_type": "integer",
            "is_nullable": True,
            "default_value": 2,
        },
        {
            "column_name": "test",
            "namespace": "test",
            "data_type": "integer",
            "is_nullable": True,
            "column_default": 2,
        },
    ]
    shared = {"table": "test_table", "schema": "test_schema"}
    for param in column_params:
        param.update(shared)
    return column_params


@pytest.fixture
def columns(column_params):
    """

    Args:
        column_params:

    Returns:

    Raises:

    """
    return [Column(**params) for params in column_params]


@pytest.fixture
def table_params(column_params):
    """

    Args:
        column_params:

    Returns:

    Raises:

    """
    table_params = [
        {"name": "test", "namespace": "test", "schema": "test"},
        {"table_name": "test", "namespace": "test", "table_schema": "test"},
        {"table_name": "test", "namespace": "test", "schema": "test"},
        {
            "name": "test",
            "schema": "test",
            "namespace": "test",
            "table_type": "TEMPORARY TABLE",
        },
        {"name": "test", "namespace": "test", "schema": "test", "columns": []},
        {"name": "test", "namespace": "test", "schema": "test", "metadata": {}},
        {
            "name": "test",
            "namespace": "test",
            "schema": "test",
            "table_type": "VIEW",
            "metadata": {},
            "columns": [],
        },
    ]
    for param in table_params:
        param["table_database"] = "test"
        param.setdefault("table_type", "BASE TABLE")
    new_table = table_params[-1]
    new_table["columns"] = column_params
    table_params.append(new_table)
    return table_params


@pytest.fixture
def edge_params():
    """ """

    def make_column_id():
        """ """
        return {
            "table_schema": "schema",
            "table_name": "table",
            "name": "column",
            "namespace": "test",
        }

    edge_params = [
        {
            "definition": "test",
            "constraint_type": "p",
            "destination": make_column_id(),
            "source": make_column_id(),
        },
        {
            "definition": "test",
            "constraint_type": "f",
            "destination": make_column_id(),
            "source": make_column_id(),
        },
    ]
    return edge_params


@pytest.fixture
def tables(table_params, edges):
    """

    Args:
        table_params:
        edges:

    Returns:

    Raises:

    """
    return [Table(**params) for params in table_params]


@pytest.fixture
def edges(edge_params):
    """

    Args:
        edge_params:

    Returns:

    Raises:

    """
    return [Edge(**params) for params in edge_params]


@pytest.fixture
def mock_get_nodes_and_edges(tables, edges):
    """

    Args:
        tables:
        edges:

    Returns:

    Raises:

    """
    nodes = adapt_to_client(tables, "v1")
    edges = adapt_to_client(edges, "v1")
    return nodes, edges
