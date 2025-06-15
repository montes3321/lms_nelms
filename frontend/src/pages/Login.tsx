import React from "react";
import { Button, Box } from "@mui/material";

export default function Login() {
  const onGoogle = () => {
    window.location.href = "/auth/google/login";
  };

  return (
    <Box sx={{ textAlign: "center", mt: 10 }}>
      <Button variant="contained" onClick={onGoogle}>
        Login via Google
      </Button>
    </Box>
  );
}
