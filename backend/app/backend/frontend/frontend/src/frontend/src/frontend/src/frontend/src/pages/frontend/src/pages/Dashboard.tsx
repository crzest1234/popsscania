import React, { useEffect, useState } from "react";
import API from "../api";

export default function Dashboard(){
  const [analyses, setAnalyses] = useState<any[]>([]);

  useEffect(()=>{
    // pas d'endpoint list dans backend minimal => placeholder
  },[]);

  return (
    <div>
      <h2>Dashboard</h2>
      <p>Utilise "Nouvelle analyse" pour tester le flux.</p>
    </div>
  )
}
