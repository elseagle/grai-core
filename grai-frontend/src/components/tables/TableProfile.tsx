import React from "react"
import { Card, Grid, Table, TableBody } from "@mui/material"
import { Column } from "./columns/TableColumnsTable"
import TableDependencies from "./TableDependencies"
import TableDetail from "./TableDetail"

interface BaseTable {
  id: string
  display_name: string
}

export interface TableInterface {
  id: string
  name: string
  namespace: string
  data_source: string
  display_name: string
  columns: { data: Column[] }
  metadata: any | null
  source_tables: { data: BaseTable[] }
  destination_tables: { data: BaseTable[] }
}

type TableProfileProps = {
  table: TableInterface
}

const TableProfile: React.FC<TableProfileProps> = ({ table }) => (
  <Grid container spacing={3}>
    <Grid item md={6}>
      <TableDetail table={table} />
    </Grid>
    <Grid item md={6}>
      <Card variant="outlined" sx={{ borderRadius: 0, borderBottom: 0 }}>
        <Table>
          <TableBody>
            <TableDependencies
              label="Upstream dependencies"
              dependencies={table.destination_tables.data}
            />
            <TableDependencies
              label="Downstream dependencies"
              dependencies={table.source_tables.data}
            />
          </TableBody>
        </Table>
      </Card>
    </Grid>
  </Grid>
)

export default TableProfile
