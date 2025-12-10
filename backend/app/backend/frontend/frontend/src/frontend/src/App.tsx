import React from "react";
import { BrowserRouter, Routes, Route, Link } from "react-router-dom";
import Dashboard from "./pages/Dashboard";
import NewAnalysis from "./pages/NewAnalysis";

export default function App(){
  return (
    <BrowserRouter>
      <div style={{padding:20}}>
        <h1>PropScan AI - MVP</h1>
        <nav><Link to="/">Dashboard</Link> | <Link to="/new">Nouvelle analyse</Link></nav>
        <Routes>
          <Route path="/" element={<Dashboard/>} />
          <Route path="/new" element={<NewAnalysis/>} />
        </Routes>
      </div>
    </BrowserRouter>
  )
}
