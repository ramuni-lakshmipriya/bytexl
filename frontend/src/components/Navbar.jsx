import React, { useState } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { Sparkles, Users, Briefcase, PlusCircle, LayoutDashboard, LogOut, LogIn, UserPlus, Zap, ChevronDown, UserCheck, Building2 } from 'lucide-react';
import { useAuth } from '../context/AuthContext';

export function Navbar() {
  const location = useLocation();
  const navigate = useNavigate();
  const { user, logout, loginDemo } = useAuth();
  const [showDemoMenu, setShowDemoMenu] = useState(false);

  const isActive = (path) => location.pathname === path;

  const handleLogout = async () => {
    await logout();
    navigate('/');
  };

  const handleDemoClick = async (role) => {
    setShowDemoMenu(false);
    try {
      await loginDemo(role);
      navigate('/dashboard');
    } catch (err) {
      console.error('Demo login error:', err);
    }
  };

  const isDemoUser = user && (user.email === 'demo.creator@gencraft.demo' || user.email === 'demo.brand@gencraft.demo' || user.email?.includes('demo'));

  return (
    <>
      {/* Top Banner for Hackathon Evaluator Demo Mode */}
      {isDemoUser && (
        <div className="bg-gradient-to-r from-amber-600 via-indigo-600 to-purple-600 text-white text-xs font-semibold py-2 px-4 shadow-sm z-50">
          <div className="max-w-7xl mx-auto flex items-center justify-between flex-wrap gap-2">
            <div className="flex items-center gap-2">
              <Zap className="w-4 h-4 text-amber-300 fill-amber-300 animate-pulse shrink-0" />
              <span>
                <strong className="tracking-wide">Evaluator Demo Mode Active:</strong> Logged in as{' '}
                <span className="underline decoration-amber-300 font-extrabold">{user.display_name || user.email}</span> ({user.role === 'creator' ? 'AI Creator' : 'Brand User'})
              </span>
            </div>
            <div className="flex items-center gap-2">
              {user.role === 'creator' ? (
                <button
                  onClick={() => handleDemoClick('brand')}
                  className="bg-white/20 hover:bg-white/30 text-white px-3 py-1 rounded-xl border border-white/40 font-bold text-[11px] transition-all flex items-center gap-1.5 shadow-xs"
                >
                  <Building2 className="w-3.5 h-3.5 text-indigo-200" />
                  Switch to Demo Brand (Lotus & Loom) ↔️
                </button>
              ) : (
                <button
                  onClick={() => handleDemoClick('creator')}
                  className="bg-white/20 hover:bg-white/30 text-white px-3 py-1 rounded-xl border border-white/40 font-bold text-[11px] transition-all flex items-center gap-1.5 shadow-xs"
                >
                  <UserCheck className="w-3.5 h-3.5 text-purple-200" />
                  Switch to Demo Creator (Ananya Rao) ↔️
                </button>
              )}
            </div>
          </div>
        </div>
      )}

      <header className="sticky top-0 z-40 w-full glass-panel border-b border-slate-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          
          {/* Brand Logo */}
          <Link to="/" className="flex items-center gap-2.5 group">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-indigo-600 via-purple-600 to-pink-500 flex items-center justify-center shadow-md shadow-indigo-500/20 group-hover:scale-105 transition-transform">
              <Sparkles className="w-5 h-5 text-white" />
            </div>
            <div>
              <span className="font-bold text-lg text-slate-900 tracking-tight">GenCraft</span>
              <span className="text-xs px-1.5 py-0.5 ml-1.5 rounded bg-indigo-100 text-indigo-700 font-semibold border border-indigo-200">AI</span>
            </div>
          </Link>

          {/* Nav Links */}
          <nav className="hidden md:flex items-center gap-1">
            <Link
              to="/creators"
              className={`px-3.5 py-2 rounded-lg text-sm font-medium transition-all flex items-center gap-2 ${
                isActive('/creators')
                  ? 'bg-indigo-50 text-indigo-600 border border-indigo-200 font-semibold'
                  : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'
              }`}
            >
              <Users className="w-4 h-4" />
              Find Creators
            </Link>

            <Link
              to="/briefs"
              className={`px-3.5 py-2 rounded-lg text-sm font-medium transition-all flex items-center gap-2 ${
                isActive('/briefs')
                  ? 'bg-indigo-50 text-indigo-600 border border-indigo-200 font-semibold'
                  : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'
              }`}
            >
              <Briefcase className="w-4 h-4" />
              Campaign Briefs
            </Link>

            {user && (
              <Link
                to="/dashboard"
                className={`px-3.5 py-2 rounded-lg text-sm font-medium transition-all flex items-center gap-2 ${
                  isActive('/dashboard')
                    ? 'bg-indigo-50 text-indigo-600 border border-indigo-200 font-semibold'
                    : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'
                }`}
              >
                <LayoutDashboard className="w-4 h-4" />
                My Dashboard
              </Link>
            )}
          </nav>

          {/* Right Section: Auth State / Actions */}
          <div className="flex items-center gap-3">
            
            {user ? (
              <div className="flex items-center gap-3">
                {/* Post Brief CTA (Brand users or general) */}
                {user.role === 'brand' && (
                  <Link
                    to="/briefs/new"
                    className="hidden sm:flex items-center gap-2 px-3.5 py-1.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-semibold shadow-sm transition-all hover:scale-105"
                  >
                    <PlusCircle className="w-4 h-4" />
                    Post Brief
                  </Link>
                )}

                {/* User Profile Badge */}
                <div className="flex items-center gap-2.5 bg-slate-100 p-1.5 rounded-2xl border border-slate-200">
                  <img
                    src={user.avatar_url || 'https://picsum.photos/seed/user/100'}
                    alt={user.display_name}
                    className="w-7 h-7 rounded-xl object-cover border border-slate-300"
                  />
                  <div className="hidden sm:block text-left pr-1">
                    <div className="text-xs font-bold text-slate-800 line-clamp-1">{user.display_name || user.email}</div>
                    <span className={`text-[10px] font-bold uppercase tracking-wider px-1.5 py-0.2 rounded border ${
                      user.role === 'creator'
                        ? 'bg-purple-100 text-purple-700 border-purple-200'
                        : 'bg-indigo-100 text-indigo-700 border-indigo-200'
                    }`}>
                      {user.role}
                    </span>
                  </div>
                </div>

                {/* Logout Button */}
                <button
                  onClick={handleLogout}
                  className="p-2 rounded-xl text-slate-500 hover:text-slate-900 hover:bg-slate-100 transition-colors"
                  title="Log Out"
                >
                  <LogOut className="w-4 h-4" />
                </button>
              </div>
            ) : (
              <div className="flex items-center gap-2">
                
                {/* Eye-catching Demo Quick Login Menu */}
                <div className="relative">
                  <button
                    onClick={() => setShowDemoMenu(!showDemoMenu)}
                    className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-gradient-to-r from-amber-500 to-amber-600 hover:from-amber-600 hover:to-amber-700 text-white font-bold text-xs transition-all shadow-sm hover:shadow-md animate-pulse hover:animate-none"
                  >
                    <Zap className="w-3.5 h-3.5 text-amber-200 fill-amber-200" />
                    <span>⚡ 1-Click Demo Login</span>
                    <ChevronDown className="w-3 h-3 text-amber-100" />
                  </button>

                  {showDemoMenu && (
                    <div className="absolute right-0 mt-2 w-64 bg-white border border-slate-200 rounded-2xl shadow-xl p-2.5 z-50 text-slate-800 animate-fade-in">
                      <div className="text-[10px] font-extrabold uppercase tracking-wider text-amber-700 bg-amber-50 px-2.5 py-1 rounded-lg border border-amber-200 mb-1 flex items-center justify-between">
                        <span>Evaluator Quick Access</span>
                        <span className="bg-amber-200 text-amber-900 text-[9px] px-1 rounded">No Password</span>
                      </div>
                      
                      <button
                        onClick={() => handleDemoClick('creator')}
                        className="w-full p-2.5 rounded-xl hover:bg-purple-50 text-left flex items-center gap-3 transition-all border border-transparent hover:border-purple-200 group"
                      >
                        <div className="w-9 h-9 rounded-xl bg-purple-100 text-purple-700 flex items-center justify-center font-bold shrink-0 shadow-xs">
                          <UserCheck className="w-5 h-5" />
                        </div>
                        <div className="overflow-hidden">
                          <div className="text-xs font-bold text-slate-900 group-hover:text-purple-700 flex items-center gap-1">
                            Demo Creator
                            <span className="text-[9px] bg-purple-100 text-purple-700 font-bold px-1 rounded">Creator</span>
                          </div>
                          <div className="text-[10px] text-slate-500 truncate">Ananya Rao (AI Filmmaker)</div>
                        </div>
                      </button>

                      <button
                        onClick={() => handleDemoClick('brand')}
                        className="w-full p-2.5 rounded-xl hover:bg-indigo-50 text-left flex items-center gap-3 transition-all border border-transparent hover:border-indigo-200 group mt-1"
                      >
                        <div className="w-9 h-9 rounded-xl bg-indigo-100 text-indigo-700 flex items-center justify-center font-bold shrink-0 shadow-xs">
                          <Building2 className="w-5 h-5" />
                        </div>
                        <div className="overflow-hidden">
                          <div className="text-xs font-bold text-slate-900 group-hover:text-indigo-700 flex items-center gap-1">
                            Demo Brand
                            <span className="text-[9px] bg-indigo-100 text-indigo-700 font-bold px-1 rounded">Brand</span>
                          </div>
                          <div className="text-[10px] text-slate-500 truncate">Lotus & Loom (Brand Manager)</div>
                        </div>
                      </button>
                    </div>
                  )}
                </div>

                <Link
                  to="/login"
                  className="hidden sm:flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-semibold text-slate-700 hover:text-slate-900 hover:bg-slate-100 transition-all"
                >
                  <LogIn className="w-3.5 h-3.5" />
                  Log In
                </Link>

                <Link
                  to="/login"
                  className="flex items-center gap-1.5 px-3.5 py-1.5 rounded-xl text-xs font-semibold bg-indigo-600 hover:bg-indigo-500 text-white shadow-xs transition-all hover:scale-105"
                >
                  <UserPlus className="w-3.5 h-3.5" />
                  Sign Up
                </Link>
              </div>
            )}

          </div>
        </div>
      </header>
    </>
  );
}

