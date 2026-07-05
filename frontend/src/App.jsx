import React from 'react'
import Login from './pages/Login';
import Layout from './components/Layout.jsx';
import YouTubeSummarizer from "./pages/YoutubeSummarizer.jsx";
import AudioVideoSummarizer from "./pages/AudioVideoSummarizer.jsx";
import PdfTextSummarizer from "./pages/PdfTextSummarizer.jsx";
import { Routes, Route, Navigate } from "react-router-dom";
import PublicOnlyRoute from "./components/PublicOnlyRoute.jsx";
import ProtectedRoute from "./components/ProtectedRoute.jsx";
function App(){
  return (
    <div className="h-screen bg-black">
      <Routes>
         <Route path="/login" element={<PublicOnlyRoute><Login /></PublicOnlyRoute>} />
          <Route
          path="/"
          element={
            <ProtectedRoute>
              <Layout />
            </ProtectedRoute>
          }>
          <Route index element={<Navigate to="/yt" replace />} />
          <Route path="/yt" element={<YouTubeSummarizer />} />
          <Route path="/audio-video" element={<AudioVideoSummarizer />} />
          <Route path="/pdf-text" element={<PdfTextSummarizer />} />
        </Route>
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
      
    </div>
  )
}

export default App;