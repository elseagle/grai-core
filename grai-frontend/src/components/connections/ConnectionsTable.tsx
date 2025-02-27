import React from "react"
import {
  Table,
  TableBody,
  TableFooter,
  TableHead,
  TableRow,
  Typography,
} from "@mui/material"
import { useNavigate } from "react-router-dom"
import Loading from "components/layout/Loading"
import RunStatus from "components/runs/RunStatus"
import TablePagination from "components/table/TablePagination"
import TableCell from "components/tables/TableCell"
import { Connection as BaseConnection } from "./ConnectionRun"
import ConnectionsMenu from "./ConnectionsMenu"

interface Connector {
  id: string
  name: string
  events: boolean
}

interface Connection extends BaseConnection {
  name: string
  namespace: string
  connector: Connector
  is_active: boolean
}

type ConnectionsTableProps = {
  connections: Connection[]
  workspaceId: string
  loading?: boolean
  total: number
}

const ConnectionsTable: React.FC<ConnectionsTableProps> = ({
  connections,
  workspaceId,
  loading,
  total,
}) => {
  const navigate = useNavigate()

  return (
    <Table sx={{ mb: -1 }}>
      <TableHead>
        <TableRow>
          <TableCell>Name</TableCell>
          <TableCell>Namespace</TableCell>
          <TableCell>Integration</TableCell>
          <TableCell>Active</TableCell>
          <TableCell>Status</TableCell>
          <TableCell sx={{ width: 0 }} />
        </TableRow>
      </TableHead>
      <TableBody>
        {connections.map(connection => (
          <TableRow
            key={connection.id}
            hover
            sx={{ cursor: "pointer" }}
            onClick={() => navigate(connection.id)}
          >
            <TableCell>{connection.name}</TableCell>
            <TableCell>{connection.namespace}</TableCell>
            <TableCell>{connection.connector.name}</TableCell>
            <TableCell>{connection.is_active ? "Yes" : "No"}</TableCell>
            <TableCell sx={{ py: 0, px: 1 }} stopPropagation>
              {connection.last_run && (
                <RunStatus
                  run={connection.last_run}
                  size="small"
                  link
                  sx={{ cursor: "pointer" }}
                />
              )}
            </TableCell>
            <TableCell sx={{ py: 0, px: 1 }} stopPropagation>
              <ConnectionsMenu
                connection={connection}
                workspaceId={workspaceId}
              />
            </TableCell>
          </TableRow>
        ))}
        {!loading && connections.length === 0 && (
          <TableRow>
            <TableCell colSpan={99} sx={{ textAlign: "center", py: 10 }}>
              <Typography>No connections found</Typography>
            </TableCell>
          </TableRow>
        )}
        {loading && (
          <TableRow>
            <TableCell colSpan={99}>
              <Loading />
            </TableCell>
          </TableRow>
        )}
      </TableBody>
      <TableFooter>
        <TablePagination
          count={total}
          rowsPerPage={1000}
          page={0}
          type="connections"
        />
      </TableFooter>
    </Table>
  )
}

export default ConnectionsTable
