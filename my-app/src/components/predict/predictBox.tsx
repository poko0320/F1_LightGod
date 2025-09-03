"use client";
import React from "react";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle
} from "@/components/ui/card";
import useAuth from "@/hooks/useAuth";

import DriverSelect from "@/components/predict/driverSelect";
import { Label } from "../ui/label";
import { Button } from "../ui/button";
import { toast } from "sonner";

const API_BASE = process.env.NEXT_PUBLIC_OWN_API!;

export default function PredictBox() {
  const { user } = useAuth() as { user: any };
  

  const onSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    const displayName: string | undefined = user?.user_metadata?.display_name;

    const fd = new FormData(e.currentTarget);

    const payload = {
      p1: Number(fd.get("p1") as string),
      p2: Number(fd.get("p2") as string),
      p3: Number(fd.get("p3") as string),
      p4: Number(fd.get("p4") as string),
      p5: Number(fd.get("p5") as string),
      playerName: displayName, 
      raceCode: "2025 monza",
      spec: 1,
    };

    try {
      const res = await fetch(`${API_BASE}/addPlayerPredict`, {
        method: "POST",
        body: JSON.stringify(payload),
      });

      toast.message("done")
    } catch (err: any) {
      const message =
        err instanceof Error ? err.message :
        typeof err === "string" ? err :
        JSON.stringify(err);
      toast.error(message);
    }
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>Predict</CardTitle>
        <CardDescription>Enter predict for current race</CardDescription>
      </CardHeader>
      <CardContent>
        <form onSubmit={onSubmit} className="space-y-6">
          {/* P1 row */}
          <div className="flex items-center gap-3">
            <Label htmlFor="p1" className="w-12">
              P1:
            </Label>
            <div className="flex-1">
              <DriverSelect id="p1" name="p1" />
            </div>
          </div>
          {/* P2 row */}
          <div className="flex items-center gap-3">
            <Label htmlFor="p2" className="w-12">
              P2:
            </Label>
            <div className="flex-1">
              <DriverSelect id="p2" name="p2" />
            </div>
          </div>
          {/* P3 row */}
          <div className="flex items-center gap-3">
            <Label htmlFor="p3" className="w-12">
              P3:
            </Label>
            <div className="flex-1">
              <DriverSelect id="p3" name="p3" />
            </div>
          </div>
          {/* P4 row */}
          <div className="flex items-center gap-3">
            <Label htmlFor="p4" className="w-12">
              P4:
            </Label>
            <div className="flex-1">
              <DriverSelect id="p4" name="p4" />
            </div>
          </div>
          {/* P5 row */}
          <div className="flex items-center gap-3">
            <Label htmlFor="p5" className="w-12">
              P5:
            </Label>
            <div className="flex-1">
              <DriverSelect id="p5" name="p5" />
            </div>
          </div>

          <Button type="submit" variant="destructive" className="w-full">
            Submit
          </Button>
        </form>
      </CardContent>
    </Card>
  );
}