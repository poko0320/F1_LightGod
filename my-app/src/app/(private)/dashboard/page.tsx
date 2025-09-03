"use client";
import useAuth from "@/hooks/useAuth";

export default function Dashboard() {
  const { user, loading } = useAuth();
  
  if (loading) return <p>Loading...</p>;
  if (!user) return <p>You must log in</p>;
  
  const displayName = user.user_metadata?.display_name || 
                     user.user_metadata?.full_name ||
                     user.email || 
                     'User';
  
  
  return (
    <div>
      <h1>Welcome, {displayName} 👋</h1>
    </div>
  );
}