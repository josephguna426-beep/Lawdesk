import { useState } from "react";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { Navigate, useNavigate } from "react-router-dom";
import { useAuth } from "./AuthContext";

const schema = z.object({ username: z.string().min(1, "Required"), password: z.string().min(1, "Required") });
type Form = z.infer<typeof schema>;

export default function LoginPage() {
  const { user, login } = useAuth();
  const navigate = useNavigate();
  const [error, setError] = useState("");
  const { register, handleSubmit, formState: { errors, isSubmitting } } = useForm<Form>({ resolver: zodResolver(schema) });

  if (user) return <Navigate to="/" replace />;

  const onSubmit = async (v: Form) => {
    setError("");
    try {
      await login(v.username, v.password);
      navigate("/");
    } catch {
      setError("Invalid username or password.");
    }
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-gray-50">
      <form onSubmit={handleSubmit(onSubmit)} className="w-80 space-y-3 rounded bg-white p-6 shadow">
        <h1 className="text-lg font-semibold">CRMS Login</h1>
        <div>
          <input {...register("username")} placeholder="Username" className="w-full rounded border p-2" />
          <p className="text-xs text-red-600">{errors.username?.message}</p>
        </div>
        <div>
          <input type="password" {...register("password")} placeholder="Password" className="w-full rounded border p-2" />
          <p className="text-xs text-red-600">{errors.password?.message}</p>
        </div>
        {error && <p className="text-sm text-red-600">{error}</p>}
        <button disabled={isSubmitting} className="w-full rounded bg-gray-900 p-2 text-white">Sign in</button>
      </form>
    </div>
  );
}
