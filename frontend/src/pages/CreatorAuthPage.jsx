import React, { useState, useEffect } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { UserCheck, Zap, AlertCircle, Loader2, Sparkles } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { fetchMeta } from '../api';
import { SocialAuthButtons } from '../components/SocialAuthButtons';

export function CreatorAuthPage() {
  const navigate = useNavigate();
  const location = useLocation();
  const { login, signupCreator, loginDemo } = useAuth();
  const isSignup = location.pathname.includes('/signup');

  const [meta, setMeta] = useState(null);
  
  // Login State
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  // Signup State
  const [fullName, setFullName] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [specialization, setSpecialization] = useState('AI Filmmaker');
  const [selectedTools, setSelectedTools] = useState([]);
  const [creatorLocation, setCreatorLocation] = useState('');
  const [acceptTerms, setAcceptTerms] = useState(false);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchMeta()
      .then(d => {
        setMeta(d);
        if (d.specializations && d.specializations.length > 0) {
          setSpecialization(d.specializations[0]);
        }
      })
      .catch(() => {});
  }, []);

  const toggleTool = (name) => {
    setSelectedTools(prev =>
      prev.includes(name) ? prev.filter(t => t !== name) : [...prev, name]
    );
  };

  const passwordStrength = (pwd) => {
    if (!pwd) return '';
    if (pwd.length < 8) return 'Weak (min 8 chars required)';
    if (/[A-Z]/.test(pwd) && /[0-9]/.test(pwd) && pwd.length >= 10) return 'Strong';
    return 'Moderate';
  };

  const handleFillDemo = () => {
    setEmail('demo.creator@gencraft.demo');
    setPassword('DemoCreator123!');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setLoading(true);

    try {
      if (isSignup) {
        if (password !== confirmPassword) {
          throw new Error('Passwords do not match.');
        }
        if (password.length < 8) {
          throw new Error('Password must be at least 8 characters long.');
        }
        if (!acceptTerms) {
          throw new Error('You must accept the terms and conditions.');
        }
        await signupCreator({
          full_name: fullName,
          email,
          password,
          specialization,
          tools: selectedTools,
          location: creatorLocation,
          accept_terms: acceptTerms
        });
        navigate('/creator/complete-profile');
      } else {
        await login(email, password);
        navigate('/dashboard');
      }
    } catch (err) {
      setError(err.message || 'Authentication failed.');
    } finally {
      setLoading(false);
    }
  };

  const handleDemo = async () => {
    setLoading(true);
    try {
      await loginDemo('creator');
      navigate('/dashboard');
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-md mx-auto px-4 py-12">
      <div className="bg-white rounded-3xl p-8 border border-slate-200 shadow-sm space-y-6">
        
        {/* Header */}
        <div className="text-center space-y-2">
          <div className="w-12 h-12 rounded-2xl bg-purple-50 border border-purple-200 text-purple-600 flex items-center justify-center mx-auto">
            <UserCheck className="w-6 h-6" />
          </div>
          <h1 className="text-2xl font-extrabold text-slate-900">
            {isSignup ? 'Creator Registration' : 'Creator Login'}
          </h1>
          <p className="text-xs text-purple-700 font-medium">
            Showcase your AI work, document pipelines & get hired
          </p>
        </div>

        {/* Tab Switcher */}
        <div className="flex bg-slate-100 p-1 rounded-xl border border-slate-200 text-xs font-semibold">
          <Link
            to="/creator/login"
            className={`flex-1 py-2 text-center rounded-lg transition-all ${
              !isSignup ? 'bg-white text-purple-700 shadow-xs' : 'text-slate-500 hover:text-slate-800'
            }`}
          >
            Log In
          </Link>
          <Link
            to="/creator/signup"
            className={`flex-1 py-2 text-center rounded-lg transition-all ${
              isSignup ? 'bg-white text-purple-700 shadow-xs' : 'text-slate-500 hover:text-slate-800'
            }`}
          >
            Sign Up
          </Link>
        </div>

        {/* Highlighted 1-Click Demo Box */}
        <div className="p-3.5 rounded-2xl bg-purple-50/80 border border-purple-200 text-purple-900 flex items-center justify-between gap-3">
          <div className="flex items-center gap-2">
            <Zap className="w-4 h-4 text-amber-600 fill-amber-500 shrink-0" />
            <span className="text-xs font-bold">Hackathon Demo Access</span>
          </div>
          <button
            type="button"
            onClick={handleDemo}
            className="px-3 py-1 rounded-xl bg-purple-600 hover:bg-purple-500 text-white font-bold text-xs shadow-xs transition-all shrink-0"
          >
            1-Click Login
          </button>
        </div>

        {/* Social Auth */}
        <SocialAuthButtons role="creator" />

        <div className="relative flex items-center justify-center">
          <div className="border-t border-slate-200 w-full" />
          <span className="bg-white px-3 text-[11px] text-slate-400 font-medium absolute">Or continue with email</span>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="space-y-4">
          
          {error && (
            <div className="p-3.5 rounded-xl bg-rose-50 border border-rose-200 text-rose-700 text-xs flex items-center gap-2">
              <AlertCircle className="w-4 h-4 shrink-0" />
              <span>{error}</span>
            </div>
          )}

          {!isSignup && (
            <div className="flex justify-end">
              <button
                type="button"
                onClick={handleFillDemo}
                className="text-[11px] text-purple-600 hover:underline font-semibold flex items-center gap-1"
              >
                <Sparkles className="w-3 h-3" />
                Fill Demo Credentials
              </button>
            </div>
          )}

          {isSignup && (
            <div>
              <label className="text-xs font-bold text-slate-700 block mb-1">Full Name *</label>
              <input
                type="text"
                required
                value={fullName}
                onChange={(e) => setFullName(e.target.value)}
                placeholder="e.g. Ananya Rao"
                className="w-full px-3.5 py-2 rounded-xl bg-white border border-slate-300 text-slate-900 text-xs focus:outline-none focus:border-purple-600"
              />
            </div>
          )}

          <div>
            <label className="text-xs font-bold text-slate-700 block mb-1">Email Address *</label>
            <input
              type="email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="demo.creator@gencraft.demo"
              className="w-full px-3.5 py-2 rounded-xl bg-white border border-slate-300 text-slate-900 text-xs focus:outline-none focus:border-purple-600"
            />
          </div>

          <div>
            <div className="flex justify-between items-center mb-1">
              <label className="text-xs font-bold text-slate-700">Password *</label>
              {isSignup && password && (
                <span className="text-[10px] font-semibold text-purple-600">{passwordStrength(password)}</span>
              )}
            </div>
            <input
              type="password"
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••"
              className="w-full px-3.5 py-2 rounded-xl bg-white border border-slate-300 text-slate-900 text-xs focus:outline-none focus:border-purple-600"
            />
          </div>

          {isSignup && (
            <>
              <div>
                <label className="text-xs font-bold text-slate-700 block mb-1">Confirm Password *</label>
                <input
                  type="password"
                  required
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                  placeholder="••••••••"
                  className="w-full px-3.5 py-2 rounded-xl bg-white border border-slate-300 text-slate-900 text-xs focus:outline-none focus:border-purple-600"
                />
              </div>

              <div>
                <label className="text-xs font-bold text-slate-700 block mb-1">Specialization *</label>
                <select
                  value={specialization}
                  onChange={(e) => setSpecialization(e.target.value)}
                  className="w-full px-3 py-2 rounded-xl bg-white border border-slate-300 text-slate-900 text-xs focus:outline-none focus:border-purple-600"
                >
                  {meta?.specializations?.map(spec => (
                    <option key={spec} value={spec}>{spec}</option>
                  ))}
                </select>
              </div>

              <div>
                <label className="text-xs font-bold text-slate-700 block mb-1">Main AI Tools Used</label>
                <div className="grid grid-cols-2 gap-1.5 max-h-32 overflow-y-auto p-2 bg-slate-50 border border-slate-200 rounded-xl custom-scrollbar text-xs">
                  {meta?.tools?.map(t => (
                    <label key={t.id} className="flex items-center gap-1.5 cursor-pointer text-slate-700 hover:text-slate-900">
                      <input
                        type="checkbox"
                        checked={selectedTools.includes(t.name)}
                        onChange={() => toggleTool(t.name)}
                        className="rounded border-slate-300 text-purple-600 focus:ring-purple-500"
                      />
                      <span>{t.name}</span>
                    </label>
                  ))}
                </div>
              </div>

              <div>
                <label className="text-xs font-bold text-slate-700 block mb-1">Location</label>
                <input
                  type="text"
                  value={creatorLocation}
                  onChange={(e) => setCreatorLocation(e.target.value)}
                  placeholder="e.g. Mumbai, IN"
                  className="w-full px-3.5 py-2 rounded-xl bg-white border border-slate-300 text-slate-900 text-xs focus:outline-none focus:border-purple-600"
                />
              </div>

              <label className="flex items-start gap-2 cursor-pointer text-xs text-slate-600 pt-1">
                <input
                  type="checkbox"
                  checked={acceptTerms}
                  onChange={(e) => setAcceptTerms(e.target.checked)}
                  className="mt-0.5 rounded border-slate-300 text-purple-600 focus:ring-purple-500"
                />
                <span>I accept the platform terms and creator code of conduct.</span>
              </label>
            </>
          )}

          <button
            type="submit"
            disabled={loading}
            className="w-full py-3 rounded-xl bg-purple-600 hover:bg-purple-500 text-white font-bold text-xs shadow-md shadow-purple-600/20 transition-all flex items-center justify-center gap-2"
          >
            {loading ? (
              <Loader2 className="w-4 h-4 animate-spin" />
            ) : (
              isSignup ? 'Create Creator Account' : 'Log In as Creator'
            )}
          </button>

        </form>

      </div>
    </div>
  );
}
