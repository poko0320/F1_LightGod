import React from "react";
import ChampionshipScenarioForm from "@/components/predict/ChampionshipScenarioForm";
const API_BASE = process.env.NEXT_PUBLIC_OWN_API!;

const CalculateWDC = async () => {
    return (
        <ChampionshipScenarioForm/>
      )
};

export default CalculateWDC;

