"use client";

import React, { useEffect} from 'react'
import {useRouter} from 'next/navigation'
import useAuth from "../../hooks/useAuth";
import { toast } from "sonner";

const PrivatePagesLayout = ({children}) => {
  const { user, loading} = useAuth();
  const router = useRouter();

  useEffect(() => {
    if(!loading && !user) {
        router.push("/");
        toast.error("Login First please");
    }
  }, [user, loading])
  if (loading || !user) return null;

  return (
    <>
      {children}
    </>
  );
}

export default PrivatePagesLayout