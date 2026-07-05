import React from 'react'
import Login from './pages/Login';
import { Routes, Route, Navigate } from "react-router-dom";
import PublicOnlyRoute from "./components/PublicOnlyRoute.jsx";
import ProtectedRoute from "./components/ProtectedRoute.jsx";
function App(){
  return (
    <div className="h-screen bg-black">
      <Routes>
         <Route path="/login" element={<PublicOnlyRoute><Login /></PublicOnlyRoute>} />
      </Routes>
      
    </div>
  )
}

export default App;