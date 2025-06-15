import React, { useEffect } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import useAuth from "../hooks/useAuth";

export default function AuthCallback() {
  const navigate = useNavigate();
  const [params] = useSearchParams();
  const { saveTokens } = useAuth();

  useEffect(() => {
    const access = params.get("access");
    const refresh = params.get("refresh");
    if (access && refresh) {
      saveTokens(access, refresh);
    }
    navigate("/");
  }, [params, saveTokens, navigate]);

  return <p>Logging in...</p>;
}
