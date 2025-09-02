"use client";
import { useEffect } from "react";
import Auth from "@/components/auth/Auth";
import useAuth from "../../hooks/useAuth";
import { useRouter } from "next/navigation";

export default function LoginPage() {
  const { user, loading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!loading && user) {
      router.replace("/dashboard"); 
    }
  }, [loading, user, router]);

  if (loading) {
    return <p>Loading...</p>; 
  }

  if (user) return null;

  return <Auth />; 
}