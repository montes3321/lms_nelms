import { useEffect, useState } from "react";

interface AuthTokens {
  access: string | null;
  refresh: string | null;
}

export default function useAuth() {
  const [tokens, setTokens] = useState<AuthTokens>(() => ({
    access: localStorage.getItem("access"),
    refresh: localStorage.getItem("refresh"),
  }));

  const saveTokens = (access: string, refresh: string) => {
    localStorage.setItem("access", access);
    localStorage.setItem("refresh", refresh);
    setTokens({ access, refresh });
  };

  const logout = () => {
    localStorage.removeItem("access");
    localStorage.removeItem("refresh");
    setTokens({ access: null, refresh: null });
  };

  useEffect(() => {
    if (!tokens.refresh) return;
    const id = setInterval(
      async () => {
        try {
          const res = await fetch("/auth/refresh", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ refresh_token: tokens.refresh }),
          });
          if (res.ok) {
            const data = await res.json();
            saveTokens(data.access_token, data.refresh_token);
          } else {
            logout();
          }
        } catch {
          logout();
        }
      },
      5 * 60 * 1000,
    );
    return () => clearInterval(id);
  }, [tokens.refresh]);

  return { ...tokens, saveTokens, logout };
}
