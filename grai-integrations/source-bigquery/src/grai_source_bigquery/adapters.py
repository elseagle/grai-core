from typing import Any, Dict, List, Literal, Sequence, Union

from grai_client.schemas.schema import Schema
from grai_schemas import config as base_config
from grai_schemas.generics import DefaultValue
from grai_schemas.v1 import EdgeV1, NodeV1
from grai_schemas.v1.metadata.edges import (
    ColumnToColumnMetadata,
    EdgeMetadataTypeLabels,
    GenericEdgeMetadataV1,
    TableToColumnMetadata,
    TableToTableMetadata,
)
from grai_schemas.v1.metadata.nodes import (
    ColumnMetadata,
    NodeMetadataTypeLabels,
    TableMetadata,
)
from multimethod import multimethod
from pydantic import BaseModel

from grai_source_bigquery.models import (
    ID,
    Column,
    ColumnID,
    Constraint,
    Edge,
    Table,
    TableID,
)
from grai_source_bigquery.package_definitions import config


@multimethod
def build_grai_metadata(current: Any, desired: Any) -> BaseModel:
    """

    Args:
        current (Any):
        desired (Any):

    Returns:

    Raises:

    """
    raise NotImplementedError(f"No adapter between {type(current)} and {type(desired)} for value {current}")


@build_grai_metadata.register
def build_grai_metadata_from_column(current: Column, version: Literal["v1"] = "v1") -> ColumnMetadata:
    """

    Args:
        current (Column):
        version (Literal["v1"], optional):  (Default value = "v1")

    Returns:

    Raises:

    """
    default_value = current.default_value
    if current.default_value is not None:
        default_value = DefaultValue(
            has_default_value=True,
            default_value=current.default_value,
            data_type=current.data_type,
        )

    data = {
        "version": version,
        "node_type": NodeMetadataTypeLabels.column.value,
        "node_attributes": {
            "data_type": current.data_type,
            "default_value": default_value,
            "is_nullable": None if current.is_nullable else False,  # Only not-nullable is definitive.
            # "is_primary_key": current.is_pk, # This is getting a default value right now
            # "is_unique": # Not support in BQ
        },
        "tags": [config.metadata_id],
    }
    return ColumnMetadata(**data)


@build_grai_metadata.register
def build_grai_metadata_from_table(current: Table, version: Literal["v1"] = "v1") -> TableMetadata:
    """

    Args:
        current (Table):
        version (Literal["v1"], optional):  (Default value = "v1")

    Returns:

    Raises:

    """
    data = {
        "version": version,
        "node_type": NodeMetadataTypeLabels.table.value,
        "node_attributes": {},
        "tags": [config.metadata_id],
    }

    return TableMetadata(**data)


@build_grai_metadata.register
def build_grai_metadata_from_edge(current: Edge, version: Literal["v1"] = "v1") -> GenericEdgeMetadataV1:
    """

    Args:
        current (Edge):
        version (Literal["v1"], optional):  (Default value = "v1")

    Returns:

    Raises:

    """
    data = {"version": version, "tags": [config.metadata_id]}

    if isinstance(current.source, TableID):
        if isinstance(current.destination, ColumnID):
            data["edge_type"] = EdgeMetadataTypeLabels.table_to_column.value
            return TableToColumnMetadata(**data)
        elif isinstance(current.destination, TableID):
            data["edge_type"] = EdgeMetadataTypeLabels.table_to_table.value
            return TableToTableMetadata(**data)
    elif isinstance(current.source, ColumnID):
        if isinstance(current.destination, ColumnID):
            data["edge_type"] = EdgeMetadataTypeLabels.column_to_column.value
            return ColumnToColumnMetadata(**data)

    data["edge_type"] = EdgeMetadataTypeLabels.generic.value
    return GenericEdgeMetadataV1(**data)


# ---


@multimethod
def build_app_metadata(current: Any, desired: Any) -> None:
    """

    Args:
        current (Any):
        desired (Any):

    Returns:

    Raises:

    """
    raise NotImplementedError(f"No adapter between {type(current)} and {type(desired)} for value {current}")


@build_app_metadata.register
def build_metadata_from_column(current: Column, version: Literal["v1"] = "v1") -> Dict:
    """

    Args:
        current (Column):
        version (Literal["v1"], optional):  (Default value = "v1")

    Returns:

    Raises:

    """
    data = {
        "table_name": current.table,
        "schema": current.column_schema,
    }

    return data


@build_app_metadata.register
def build_metadata_from_table(current: Table, version: Literal["v1"] = "v1") -> Dict:
    """

    Args:
        current (Table):
        version (Literal["v1"], optional):  (Default value = "v1")

    Returns:

    Raises:

    """
    data = {
        "schema": current.table_schema,
        "table_type": current.table_type.value,
    }
    return data


@build_app_metadata.register
def build_metadata_from_edge(current: Edge, version: Literal["v1"] = "v1") -> Dict:
    """

    Args:
        current (Edge):
        version (Literal["v1"], optional):  (Default value = "v1")

    Returns:

    Raises:

    """
    data = {
        "definition": current.definition,
        "constraint_type": current.constraint_type.value,
    }
    data |= current.metadata if current.metadata is not None else {}

    return data


# ---


def build_metadata(obj, version):
    """

    Args:
        obj:
        version:

    Returns:

    Raises:

    """
    integration_meta = build_app_metadata(obj, version)
    base_metadata = build_grai_metadata(obj, version)
    integration_meta["grai"] = base_metadata

    return {
        base_config.metadata_id: base_metadata,
        config.metadata_id: integration_meta,
    }


@multimethod
def adapt_to_client(current: Any, desired: Any) -> Union[NodeV1, EdgeV1]:
    """

    Args:
        current (Any):
        desired (Any):

    Returns:

    Raises:

    """
    raise NotImplementedError(f"No adapter between {type(current)} and {type(desired)}")


@adapt_to_client.register
def adapt_column_to_client(current: Column, version: Literal["v1"] = "v1") -> NodeV1:
    """

    Args:
        current (Column):
        version (Literal["v1"], optional):  (Default value = "v1")

    Returns:

    Raises:

    """
    spec_dict = {
        "name": current.full_name,
        "namespace": current.namespace,
        "display_name": current.name,
        "data_source": config.integration_name,
        "metadata": build_metadata(current, version),
    }
    return Schema.to_model(spec_dict, version=version, typing_type="Node")


@adapt_to_client.register
def adapt_table_to_client(current: Table, version: Literal["v1"] = "v1") -> NodeV1:
    """

    Args:
        current (Table):
        version (Literal["v1"], optional):  (Default value = "v1")

    Returns:

    Raises:

    """
    metadata = {
        "node_type": NodeMetadataTypeLabels.table.value,
        "schema": current.table_schema,
    }
    spec_dict = {
        "name": current.full_name,
        "namespace": current.namespace,
        "display_name": current.name,
        "data_source": config.integration_name,
        "metadata": build_metadata(current, version),
    }
    metadata.update(current.metadata)
    return Schema.to_model(spec_dict, version=version, typing_type="Node")


def make_name(node1: ID, node2: ID) -> str:
    """

    Args:
        node1 (ID):
        node2 (ID):

    Returns:

    Raises:

    """
    node1_name = f"{node1.namespace}:{node1.full_name}"
    node2_name = f"{node2.namespace}:{node2.full_name}"
    return f"{node1_name} -> {node2_name}"


@adapt_to_client.register
def adapt_edge_to_client(current: Edge, version: Literal["v1"] = "v1") -> EdgeV1:
    """

    Args:
        current (Edge):
        version (Literal["v1"], optional):  (Default value = "v1")

    Returns:

    Raises:

    """
    spec_dict = {
        "data_source": config.integration_name,
        "name": make_name(current.source, current.destination),
        "namespace": current.source.namespace,
        "source": {
            "name": current.source.full_name,
            "namespace": current.source.namespace,
        },
        "destination": {
            "name": current.destination.full_name,
            "namespace": current.destination.namespace,
        },
        "metadata": build_metadata(current, version),
    }
    return Schema.to_model(spec_dict, version=version, typing_type="Edge")


@adapt_to_client.register
def adapt_list_to_client(objs: Sequence, version: Literal["v1"]) -> List:
    """

    Args:
        objs (Sequence):
        version (Literal["v1"]):

    Returns:

    Raises:

    """
    return [adapt_to_client(item, version) for item in objs]
