"use client";
import React from "react";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle
} from "@/components/ui/card";

import { Input } from "../ui/input";
import { Label } from "../ui/label";
import { Button } from "../ui/button";

import client from "@/api/client";
import { toast } from "sonner";

const API_BASE = process.env.NEXT_PUBLIC_OWN_API;

const Signup = () => {
  const handleSignup = async (e) => {
    e.preventDefault();
    const display_name = e.target[0]?.value;
    const email = e.target[1]?.value;
    const password =e.target[2]?.value;


    if(!email || !password) {
      toast.error("Please enter email and password");
      return;
    }

    const { data,error } = await client.auth.signUp({
      email, password, options: {data: {display_name: display_name}, emailRedirectTo: 'http://f1lightgod/auth/confirm'}
    });

    if(data){
      toast.success("Success to sign up. Please Check your email to confirm the link")
    }

    if(error){
      toast.success("Something get wrong...")
    }

  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>Sign up</CardTitle>
        <CardDescription>
          Enter email and password to signup
        </CardDescription>
      </CardHeader>

      <CardContent>
        <form onSubmit={handleSignup}>
          <div className="flex flex-col gap-6">
          <div className="grid gap-2">
              <Label htmlFor="Display Name">Display Name</Label>
              <Input
                id="display_name"
                name="display_name"
                type="display_name"
                required
                placeholder="Josh000"
              />
            </div>
            <div className="grid gap-2">
              <Label htmlFor="email">Email</Label>
              <Input
                id="email"
                name="email"
                type="email"
                required
                placeholder="example@gmail.com"
              />
            </div>

            <div className="grid gap-2">
              <Label htmlFor="password">Password</Label>
              <Input
                id="password"
                name="password"
                type="password"
                placeholder="qwer1234"
              />
            </div>

            <Button
              type="submit"
              variant="destructive"
              className="w-full"
            >
              Sign up
            </Button>
          </div>
        </form>
      </CardContent>
    </Card>
  );
};

export default Signup;