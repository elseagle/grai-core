import React from "react"
import userEvent from "@testing-library/user-event"
import { render, screen, waitFor } from "testing"
import RegisterForm, { REGISTER } from "./RegisterForm"
import { GraphQLError } from "graphql"

test("renders", async () => {
  const user = userEvent.setup()

  render(<RegisterForm />, {
    guestRoute: true,
    loggedIn: false,
    path: "/register",
    route: "/register",
    routes: ["/"],
  })

  await user.type(screen.getByRole("textbox", { name: /name/i }), "Test User")
  await user.type(
    screen.getByRole("textbox", { name: /email/i }),
    "email@grai.io"
  )
  await user.type(screen.getByTestId("password"), "password")

  await waitFor(() => {
    expect(screen.getByTestId("password")).toHaveValue("password")
  })

  await user.click(screen.getByRole("button", { name: /register/i }))

  await waitFor(() => {
    expect(screen.getByText("New Page")).toBeInTheDocument()
  })
})

test("error", async () => {
  const user = userEvent.setup()

  const mocks = [
    {
      request: {
        query: REGISTER,
        variables: {
          name: "Test User",
          username: "email@grai.io",
          password: "password",
        },
      },
      result: {
        errors: [new GraphQLError("Error!")],
      },
    },
  ]

  render(<RegisterForm />, {
    withRouter: true,
    mocks,
  })

  await user.type(screen.getByRole("textbox", { name: /name/i }), "Test User")
  await user.type(
    screen.getByRole("textbox", { name: /email/i }),
    "email@grai.io"
  )
  await user.type(screen.getByTestId("password"), "password")

  await waitFor(() => {
    expect(screen.getByTestId("password")).toHaveValue("password")
  })

  await user.click(screen.getByRole("button", { name: /register/i }))

  await waitFor(() => {
    expect(screen.getByText("Error!")).toBeInTheDocument()
  })
})
