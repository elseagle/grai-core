import React from "react"
import { Box, Card, CardContent, Container, Typography } from "@mui/material"
import { Helmet } from "react-helmet-async"
import LoginForm from "components/auth/login/LoginForm"
import SignupLink from "components/auth/login/SignupLink"
import GraiLogo from "components/icons/GraiLogo"

const Login: React.FC = () => (
  <>
    <Helmet>
      <title>Grai Cloud Login</title>
      <meta
        name="description"
        content="Login to Grai Cloud. The easiest way to get started with data lineage. Create a free account today."
      />
    </Helmet>
    <Box
      sx={{
        width: "100%",
        height: "100vh",
        overflowX: "hidden",
        position: "relative",
      }}
    >
      <Box
        sx={{
          backgroundColor: "#8338EC20",
          width: 810,
          height: 568,
          position: "absolute",
          top: 490,
          left: -318,
          borderRadius: "50%",
          filter: "blur(200px)",
          zIndex: -1,
        }}
      />
      <Box
        sx={{
          backgroundColor: "#3A86FF20",
          width: 800,
          height: 624,
          position: "absolute",
          top: 557,
          right: -300,
          borderRadius: "50%",
          filter: "blur(200px)",
          overflow: "hidden",
          zIndex: -1,
        }}
      />

      <Container maxWidth="sm" sx={{ pt: 10, maxWidth: { xs: 500 } }}>
        <Box sx={{ textAlign: "center" }}>
          <Box sx={{ mb: 5, ml: 1 }}>
            <GraiLogo />
          </Box>
          <Typography
            variant="h1"
            sx={{ fontSize: 36, fontWeight: 800, mb: 5, lineHeight: 1.6 }}
          >
            Welcome Back!
          </Typography>
        </Box>
        <Card
          sx={{
            boxShadow: "0 10px 20px 0 rgb(0 0 0 / 0.04)",
            borderRadius: "20px",
            borderColor: "rgba(0, 0, 0, 0.06)",
            borderWidth: 1,
            borderStyle: "solid",
          }}
        >
          <CardContent sx={{ p: "20px" }}>
            <LoginForm />
          </CardContent>
        </Card>
        <SignupLink />
      </Container>
    </Box>
  </>
)

export default Login
