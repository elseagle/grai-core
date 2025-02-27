from typing import Literal, Optional, Union
from uuid import UUID, uuid4

import httpx
from httpx import Response

from grai_client.endpoints.client import BaseClient
from grai_client.endpoints.utilities import is_valid_uuid


class ClientV1(BaseClient):
    """ """

    id: Literal["v1"] = "v1"
    base = "/api/v1/"
    _node_endpoint = "lineage/nodes/"
    _edge_endpoint = "lineage/edges/"
    _workspace_endpoint = "workspaces/"
    _is_authenticated_endpoint = "auth/is-authenticated/"

    def __init__(self, *args, workspace: Optional[Union[str, UUID]] = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.api = f"{self.url}{self.base}"
        self.node_endpoint = f"{self.api}{self._node_endpoint}"
        self.edge_endpoint = f"{self.api}{self._edge_endpoint}"
        self.workspace_endpoint = f"{self.api}{self._workspace_endpoint}"
        self.is_authenticated_endpoint = f"{self.api}{self._is_authenticated_endpoint}"

        self._workspace = str(workspace) if isinstance(workspace, (str, UUID)) else None

        if self.init_auth_values.is_valid():
            self.authenticate(**self.init_auth_values.dict())

    def check_authentication(self) -> Response:
        """

        Args:

        Returns:

        Raises:

        """
        return httpx.get(self.is_authenticated_endpoint, auth=self.auth)

    @property
    def workspace(self) -> Optional[str]:
        """

        Args:

        Returns:

        Raises:

        """
        return self._workspace

    @workspace.setter
    def workspace(self, workspace: Optional[Union[str, UUID]]):
        """

        Args:
            workspace (Optional[Union[str, UUID]]):

        Returns:

        Raises:

        """
        if workspace is None:
            self._workspace = workspace
            self.default_query_args.pop("workspace", None)
            self.default_payload.pop("workspace", None)
            return

        if is_valid_uuid(workspace) or isinstance(workspace, str):
            result = self.get("workspace", workspace)

            if result is None:
                raise Exception(f"No workspace found matching `{workspace}`")
            elif isinstance(workspace, str) and "/" in workspace:  # workspace ref
                if workspace != result.ref:
                    raise Exception(f"No workspace matching `ref={workspace}`")
            elif workspace != result.name:  # workspace name
                raise Exception(f"No workspace matching `name={workspace}`")

            workspace = result.id
        else:
            raise TypeError("Workspace must be either a string, uuid, or None.")

        self._workspace = str(workspace)
        self.default_query_args["workspace"] = self._workspace
        self.default_payload["workspace"] = self._workspace

    def authenticate(
        self,
        username: Optional[str] = None,
        password: Optional[str] = None,
        api_key: Optional[str] = None,
    ) -> None:
        """

        Args:
            username (Optional[str], optional):  (Default value = None)
            password (Optional[str], optional):  (Default value = None)
            api_key (Optional[str], optional):  (Default value = None)

        Returns:

        Raises:

        """
        super().authenticate(username, password, api_key)
        self.workspace = self.workspace
