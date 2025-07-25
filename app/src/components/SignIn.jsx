import Avatar from "@mui/material/Avatar";
import Button from "@mui/material/Button";
import CssBaseline from "@mui/material/CssBaseline";
import Grid from "@mui/material/Grid";
import Box from "@mui/material/Box";
import TextField from "@mui/material/TextField";
import FormControlLabel from "@mui/material/FormControlLabel";
import Checkbox from "@mui/material/Checkbox";
import LockOutlinedIcon from "@mui/icons-material/LockOutlined";
import Typography from "@mui/material/Typography";
import Container from "@mui/material/Container";
import {
  createTheme,
  ThemeProvider,
  StyledEngineProvider,
} from "@mui/material/styles";
import { useAuth } from "../Context/AuthContext.jsx";
import { useNavigate } from "react-router-dom";
// function Copyright(props) {
//   return (
//     <Typography
//       variant="body2"
//       color="text.secondary"
//       align="center"
//       {...props}
//     >
//       {"Copyright © "}
//       <Link color="inherit" href="https://github.com/OpenLake/Leaderboard-Pro/">
//         LeaderBoard-Pro
//       </Link>{" "}
//       {new Date().getFullYear()}
//       {"."}
//     </Typography>
//   );
// }

const theme = createTheme();

export default function SignIn({ loginUser, googleAuth }) {
  let { toRegister } = useAuth();
  const navigate = useNavigate();
  const handleGoogleAuth = async (e) => {
    e.preventDefault();
    await googleAuth();
    navigate("/");
  };
  return (
    <StyledEngineProvider injectFirst>
      <ThemeProvider theme={theme}>
        <Container component="main" maxWidth="xs">
          <CssBaseline />
          <Box
            sx={{
              marginTop: 8,
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
            }}
          >
            <Avatar sx={{ m: 1, bgcolor: "secondary.main" }}>
              <LockOutlinedIcon />
            </Avatar>
            <Typography component="h1" variant="h5">
              Sign in
            </Typography>
            <Box component="form" noValidate sx={{ mt: 1 }}>
              <TextField
                margin="normal"
                required
                fullWidth
                id="UserName"
                label="UserName"
                name="UserName"
                autoComplete="UserName"
                autoFocus
              />
              <TextField
                margin="normal"
                required
                fullWidth
                name="password"
                label="Password"
                type="password"
                id="password"
                autoComplete="current-password"
              />
              <FormControlLabel
                control={<Checkbox value="remember" color="primary" />}
                label="Remember me"
              />
              <Button
                type="submit"
                fullWidth
                variant="contained"
                onClick={loginUser}
                sx={{ mt: 3, mb: 2 }}
              >
                Sign In
              </Button>
              <Button
                // type="submit"
                fullWidth
                variant="contained"
                onClick={handleGoogleAuth}
                sx={{ mb: 2 }}
              >
                Sign In With Google
              </Button>
              <Grid container alignItems="center" justifyContent="center">
                <Grid>
                  <Button
                    variant="body2"
                    style={{ color: "red" }}
                    onClick={toRegister}
                  >
                    {"Don't have an account? Sign Up"}
                  </Button>
                </Grid>
              </Grid>
            </Box>
          </Box>
        </Container>
      </ThemeProvider>
    </StyledEngineProvider>
  );
}
