import React, { useState } from "react";
import {
  TextField,
  Button,
  Checkbox,
  FormControlLabel,
  Box,
} from "@mui/material";
import { Link } from "react-router-dom";

export default function SignUp() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [name, setName] = useState("");
  const [policy, setPolicy] = useState(false);
  const [error, setError] = useState("");

  const validatePassword = (pwd: string) => pwd.length >= 6;

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!validatePassword(password)) {
      setError("Weak password");
      return;
    }
    try {
      const res = await fetch("/auth/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password, name }),
      });
      if (res.ok) {
        window.location.href = "/email-sent";
      } else if (res.status === 409) {
        setError("Email already registered");
      } else {
        setError("Error");
      }
    } catch {
      setError("Network error");
    }
  };

  return (
    <Box
      component="form"
      onSubmit={onSubmit}
      sx={{
        display: "flex",
        flexDirection: "column",
        gap: 2,
        width: 300,
        m: "auto",
      }}
    >
      <TextField
        label="Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        required
      />
      <TextField
        label="Password"
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        required
      />
      <TextField
        label="Name"
        value={name}
        onChange={(e) => setName(e.target.value)}
        required
      />
      <FormControlLabel
        control={
          <Checkbox
            checked={policy}
            onChange={(e) => setPolicy(e.target.checked)}
          />
        }
        label="I accept the policy"
      />
      {error && <Box color="red">{error}</Box>}
      <Button type="submit" variant="contained" disabled={!policy}>
        Sign Up
      </Button>
      <Button component={Link} to="/login">
        Login
      </Button>
    </Box>
  );
}
