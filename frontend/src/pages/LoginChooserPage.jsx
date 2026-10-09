import React from 'react';
import { Link, useNavigate, useSearchParams } from 'react-router-dom';
import { UserCheck, Building2, Sparkles, Zap, ArrowRight, ShieldCheck } from 'lucide-react';
import { useAuth } from '../context/AuthContext';

export function LoginChooserPage() {
  const navigate = useNavigate();
  const { loginDemo } = useAuth();
  const [searchParams] = useSearchParams();
  const oauthError = searchParams.get('oauth_error');

  const handleDemo = async (role) => {
    try {
      await loginDemo(role);
      navigate('/dashboard');
    } catch (err) {
      console.error('Demo login failed:', err);
    }
  };

  return (
    <div className="max-w-4xl mx-auto px-4 py-12 space-y-8">
      
      {/* Header */}
      <div className="text-center space-y-3">
        <div className="inline-flex items-center gap-2 px-3.5 py-1 rounded-full bg-indigo-50 border border-indigo-200 text-indigo-700 text-xs font-semibold">
          <Sparkles className="w-4 h-4 text-indigo-600" />
          Welcome to GenCraft AI Marketplace
        </div>
        <h1 className="text-3xl sm:text-4xl font-extrabold text-slate-900 tracking-tight">
          Choose Account Type
        </h1>
        <p className="text-sm text-slate-600 max-w-md mx-auto">
          Select your portal below or use 1-click Demo Access to evaluate features instantly.
        </p>
      </div>

      {/* OAuth Error Notice */}
      {oauthError && (
        <div className="p-4 rounded-2xl bg-amber-50 border border-amber-200 text-amber-800 text-xs text-center max-w-md mx-auto">
          {oauthError === 'instagram_test_mode' ? (
            <span>Instagram login is in test mode. Please use Google, Facebook or email.</span>
          ) : oauthError === 'google_not_configured' ? (
            <span>Google login client ID is not configured in environment.</span>
          ) : (
            <span>OAuth authentication attempt failed. Please sign in with email.</span>
          )}
        </div>
      )}

      {/* PROMINENT DEMO ACCESS HERO BANNER FOR JUDGES */}
      <div className="p-6 rounded-3xl bg-gradient-to-r from-amber-50 via-indigo-50 to-purple-50 border border-amber-200 shadow-sm space-y-4">
        <div className="flex items-center justify-between flex-wrap gap-2">
          <div className="flex items-center gap-2 text-amber-900 font-extrabold text-sm">
            <Zap className="w-5 h-5 text-amber-600 fill-amber-500" />
            Instant Evaluator Demo Access (No OAuth or Password required)
          </div>
          <span className="text-[10px] font-bold uppercase tracking-wider bg-amber-200/80 text-amber-900 px-2 py-0.5 rounded border border-amber-300">
            For Hackathon Judges
          </span>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-1">
          {/* Demo Creator 1-Click Button */}
          <button
            onClick={() => handleDemo('creator')}
            className="p-4 rounded-2xl bg-white hover:bg-purple-50/80 border border-purple-200 hover:border-purple-300 text-left transition-all shadow-xs group flex items-center justify-between"
          >
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-purple-100 text-purple-700 flex items-center justify-center font-bold">
                <UserCheck className="w-5 h-5" />
              </div>
              <div>
                <div className="text-xs font-bold text-slate-900 group-hover:text-purple-700 flex items-center gap-1.5">
                  Log in as Demo Creator
                  <span className="text-[10px] text-purple-600 bg-purple-100 px-1.5 py-0.2 rounded font-semibold">1-Click</span>
                </div>
                <div className="text-[11px] text-slate-500">Ananya Rao (Senior AI Filmmaker)</div>
              </div>
            </div>
            <ArrowRight className="w-4 h-4 text-purple-500 group-hover:translate-x-1 transition-transform" />
          </button>

          {/* Demo Brand 1-Click Button */}
          <button
            onClick={() => handleDemo('brand')}
            className="p-4 rounded-2xl bg-white hover:bg-indigo-50/80 border border-indigo-200 hover:border-indigo-300 text-left transition-all shadow-xs group flex items-center justify-between"
          >
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-indigo-100 text-indigo-700 flex items-center justify-center font-bold">
                <Building2 className="w-5 h-5" />
              </div>
              <div>
                <div className="text-xs font-bold text-slate-900 group-hover:text-indigo-700 flex items-center gap-1.5">
                  Log in as Demo Brand
                  <span className="text-[10px] text-indigo-600 bg-indigo-100 px-1.5 py-0.2 rounded font-semibold">1-Click</span>
                </div>
                <div className="text-[11px] text-slate-500">Lotus & Loom (Brand Manager)</div>
              </div>
            </div>
            <ArrowRight className="w-4 h-4 text-indigo-500 group-hover:translate-x-1 transition-transform" />
          </button>
        </div>
      </div>

      {/* Standard Chooser Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        
        {/* Creator Card */}
        <div className="bg-white rounded-3xl p-8 border border-slate-200 shadow-xs hover:shadow-md hover:border-purple-300 transition-all flex flex-col justify-between space-y-6">
          <div className="space-y-4">
            <div className="w-14 h-14 rounded-2xl bg-purple-50 border border-purple-200 flex items-center justify-center text-purple-600">
              <UserCheck className="w-7 h-7" />
            </div>
            <div>
              <span className="text-xs font-bold uppercase tracking-wider text-purple-600">For AI Creators</span>
              <h2 className="text-2xl font-bold text-slate-900 mt-1">Creator Portal</h2>
              <p className="text-xs text-slate-600 leading-relaxed mt-2">
                Showcase your generative AI portfolio, document tool pipelines, set INR project rates, and get matched with brand campaign briefs.
              </p>
            </div>
          </div>

          <div className="space-y-3 pt-4 border-t border-slate-100">
            <div className="grid grid-cols-2 gap-3">
              <Link
                to="/creator/login"
                className="py-2.5 px-4 rounded-xl bg-purple-600 hover:bg-purple-500 text-white font-bold text-xs text-center transition-all shadow-xs flex items-center justify-center gap-1.5"
              >
                Log In
                <ArrowRight className="w-3.5 h-3.5" />
              </Link>
              <Link
                to="/creator/signup"
                className="py-2.5 px-4 rounded-xl bg-purple-50 hover:bg-purple-100 text-purple-700 font-bold text-xs text-center border border-purple-200 transition-all"
              >
                Sign Up
              </Link>
            </div>
          </div>
        </div>

        {/* Brand Card */}
        <div className="bg-white rounded-3xl p-8 border border-slate-200 shadow-xs hover:shadow-md hover:border-indigo-300 transition-all flex flex-col justify-between space-y-6">
          <div className="space-y-4">
            <div className="w-14 h-14 rounded-2xl bg-indigo-50 border border-indigo-200 flex items-center justify-center text-indigo-600">
              <Building2 className="w-7 h-7" />
            </div>
            <div>
              <span className="text-xs font-bold uppercase tracking-wider text-indigo-600">For Brands & Agencies</span>
              <h2 className="text-2xl font-bold text-slate-900 mt-1">Brand Portal</h2>
              <p className="text-xs text-slate-600 leading-relaxed mt-2">
                Find verified AI filmmakers and 3D animators, post campaign briefs using Gemini AI, and review automated match scores.
              </p>
            </div>
          </div>

          <div className="space-y-3 pt-4 border-t border-slate-100">
            <div className="grid grid-cols-2 gap-3">
              <Link
                to="/brand/login"
                className="py-2.5 px-4 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-bold text-xs text-center transition-all shadow-xs flex items-center justify-center gap-1.5"
              >
                Log In
                <ArrowRight className="w-3.5 h-3.5" />
              </Link>
              <Link
                to="/brand/signup"
                className="py-2.5 px-4 rounded-xl bg-indigo-50 hover:bg-indigo-100 text-indigo-700 font-bold text-xs text-center border border-indigo-200 transition-all"
              >
                Sign Up
              </Link>
            </div>
          </div>
        </div>

      </div>

    </div>
  );
}
