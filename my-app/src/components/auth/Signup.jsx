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

const Signup = () => {
  const handleSignup = async (e) => {
    e.preventDefault();
    const email = e.target[0]?.value;
    const password =e.target[1]?.value;

    if(!email || !password) {
      toast.error("Please enter email and password");
      return;
    }

    const { data,error } = await client.auth.signUp({
      email, password,
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