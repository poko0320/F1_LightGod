"use client";
import React from "react";
import { drivers } from "./driver";

type DriverSelectProps = {
  id?: string;
  name: string;                
  defaultValue?: string;
  onChange?: (value: string) => void;
};

const DriverSelect: React.FC<DriverSelectProps> = ({ id, name, defaultValue = "", onChange }) => {
  return (
    <select
      id={id}
      name={name}              
      defaultValue={defaultValue}
      onChange={(e) => onChange?.(e.target.value)}
      required
      style={{
        padding: "8px",
        borderRadius: "6px",
        border: "1px solid #ccc",
        fontSize: "1rem",
      }}
    >
      <option value="" disabled>
        Select a driver
      </option>
      {drivers.map((d) => (
        <option key={d.value} value={d.value}>
          {d.label}
        </option>
      ))}
    </select>
  );
};

export default DriverSelect;