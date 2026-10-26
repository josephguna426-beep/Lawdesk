import { NavLink, Outlet } from "react-router-dom";
import { useAuth } from "../features/auth/AuthContext";

const links = [
  ["/", "Dashboard"],
  ["/cases", "Cases"],
  ["/clients", "Clients"],
  ["/parties", "Parties"],
  ["/courts", "Courts"],
  ["/advocates", "Advocates"],
  ["/hearings", "Hearings"],
  ["/reports", "Reports"],
  ["/notifications", "Notifications"],
  ["/settings", "Settings"],
  ["/audit", "Audit"],
];

export default function AppLayout() {
  const { user, logout } = useAuth();
  return (
    <div className="flex min-h-screen flex-col md:flex-row">
      <aside className="w-full border-b bg-gray-50 p-3 md:w-56 md:border-b-0 md:border-r">
        <div className="mb-3 font-bold">CRMS</div>
        <nav className="flex flex-wrap gap-1 md:flex-col">
          {links.map(([to, label]) => (
            <NavLink key={to} to={to} end={to === "/"}
              className={({ isActive }) => `rounded px-2 py-1 text-sm ${isActive ? "bg-gray-200 font-medium" : "hover:bg-gray-100"}`}>
              {label}
            </NavLink>
          ))}
        </nav>
        <div className="mt-4 text-xs text-gray-500">{user?.username}</div>
        <button onClick={logout} className="mt-1 text-xs text-red-600 underline">Logout</button>
      </aside>
      <main className="flex-1 p-4"><Outlet /></main>
    </div>
  );
}
