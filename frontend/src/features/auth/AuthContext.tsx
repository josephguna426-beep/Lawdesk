import { createContext, ReactNode, useContext, useEffect, useState } from "react";
import { get, post } from "../../lib/api";
import type { User } from "../../types";

interface AuthState {
  user: User | null;
  loading: boolean;
  login: (username: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
}

const Ctx = createContext<AuthState>(null as unknown as AuthState);
export const useAuth = () => useContext(Ctx);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    get("/auth/csrf/")
      .then(() => get<User>("/auth/me/"))
      .then(setUser)
      .catch(() => setUser(null))
      .finally(() => setLoading(false));
  }, []);

  const login = async (username: string, password: string) => {
    await get("/auth/csrf/");
    setUser(await post<User>("/auth/login/", { username, password }));
  };
  const logout = async () => {
    await post("/auth/logout/");
    setUser(null);
  };

  return <Ctx.Provider value={{ user, loading, login, logout }}>{children}</Ctx.Provider>;
}
