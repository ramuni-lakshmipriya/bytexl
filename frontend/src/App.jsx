import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import { RoleProvider } from './context/RoleContext';
import { Navbar } from './components/Navbar';
import { Footer } from './components/Footer';

import { HomePage } from './pages/HomePage';
import { CreatorsPage } from './pages/CreatorsPage';
import { CreatorProfilePage } from './pages/CreatorProfilePage';
import { BriefsPage } from './pages/BriefsPage';
import { BriefDetailPage } from './pages/BriefDetailPage';
import { NewBriefPage } from './pages/NewBriefPage';

import { LoginChooserPage } from './pages/LoginChooserPage';
import { CreatorAuthPage } from './pages/CreatorAuthPage';
import { BrandAuthPage } from './pages/BrandAuthPage';
import { CompleteProfilePage } from './pages/CompleteProfilePage';
import { DashboardPage } from './pages/DashboardPage';

import { ProtectedRoute, RoleRoute } from './components/ProtectedRoute';

export default function App() {
  return (
    <AuthProvider>
      <RoleProvider>
        <Router>
          <div className="min-h-screen flex flex-col bg-slate-50 text-slate-900 font-sans selection:bg-indigo-500 selection:text-white">
            <Navbar />
            <main className="flex-1">
              <Routes>
                <Route path="/" element={<HomePage />} />
                <Route path="/creators" element={<CreatorsPage />} />
                <Route path="/creators/:id" element={<CreatorProfilePage />} />
                <Route path="/briefs" element={<BriefsPage />} />
                <Route path="/briefs/:id" element={<BriefDetailPage />} />

                {/* Auth Routes */}
                <Route path="/login" element={<LoginChooserPage />} />
                <Route path="/creator/login" element={<CreatorAuthPage />} />
                <Route path="/creator/signup" element={<CreatorAuthPage />} />
                <Route path="/brand/login" element={<BrandAuthPage />} />
                <Route path="/brand/signup" element={<BrandAuthPage />} />

                {/* Protected & Role Routes */}
                <Route path="/briefs/new" element={
                  <RoleRoute role="brand">
                    <NewBriefPage />
                  </RoleRoute>
                } />
                <Route path="/creator/complete-profile" element={
                  <RoleRoute role="creator">
                    <CompleteProfilePage />
                  </RoleRoute>
                } />
                <Route path="/dashboard" element={
                  <ProtectedRoute>
                    <DashboardPage />
                  </ProtectedRoute>
                } />

              </Routes>
            </main>
            <Footer />
          </div>
        </Router>
      </RoleProvider>
    </AuthProvider>
  );
}
