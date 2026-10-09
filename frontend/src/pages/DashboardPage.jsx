import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { LayoutDashboard, PlusCircle, Briefcase, Award, CheckCircle2, UserCheck, Building2, ArrowRight, Clock } from 'lucide-react';
import { fetchDashboard } from '../api';
import { useAuth } from '../context/AuthContext';

export function DashboardPage() {
  const { user } = useAuth();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    setLoading(true);
    fetchDashboard()
      .then(res => {
        setData(res);
        setLoading(false);
      })
      .catch(err => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return (
      <div className="max-w-6xl mx-auto px-4 py-16 text-center space-y-4">
        <div className="h-8 bg-slate-200 rounded w-1/3 mx-auto animate-pulse" />
        <div className="h-20 bg-slate-200 rounded-2xl w-full animate-pulse" />
      </div>
    );
  }

  if (error || !data) {
    return (
      <div className="max-w-md mx-auto px-4 py-16 text-center space-y-4">
        <div className="text-xl font-bold text-rose-600">Failed to load dashboard</div>
        <p className="text-xs text-slate-500">{error}</p>
      </div>
    );
  }

  const formatCurrency = (amount) => {
    if (!amount) return 'N/A';
    return `₹${amount.toLocaleString('en-IN')}`;
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10 space-y-8">
      
      {/* Dashboard Top Header */}
      <div className="bg-white p-6 sm:p-8 rounded-3xl border border-slate-200 shadow-xs flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
        <div className="flex items-center gap-4">
          <img
            src={user.avatar_url || 'https://picsum.photos/seed/user/150'}
            alt={user.display_name}
            className="w-16 h-16 rounded-2xl object-cover border-2 border-slate-200 shadow-sm"
          />
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-2xl font-extrabold text-slate-900">{user.display_name || user.email}</h1>
              <span className={`text-xs px-2.5 py-0.5 rounded-full font-bold uppercase border ${
                user.role === 'brand'
                  ? 'bg-indigo-50 text-indigo-700 border-indigo-200'
                  : 'bg-purple-50 text-purple-700 border-purple-200'
              }`}>
                {user.role} Dashboard
              </span>
            </div>
            <p className="text-xs text-slate-500 mt-0.5">{user.email}</p>
          </div>
        </div>

        {user.role === 'brand' ? (
          <Link
            to="/briefs/new"
            className="px-5 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-bold text-xs shadow-md shadow-indigo-600/20 flex items-center gap-2 transition-all hover:scale-105"
          >
            <PlusCircle className="w-4 h-4" />
            Post New Campaign Brief
          </Link>
        ) : (
          <Link
            to={`/creators/${user.creator_id}`}
            className="px-5 py-2.5 rounded-xl bg-purple-600 hover:bg-purple-500 text-white font-bold text-xs shadow-md shadow-purple-600/20 flex items-center gap-2 transition-all hover:scale-105"
          >
            <UserCheck className="w-4 h-4" />
            View Public Profile
          </Link>
        )}
      </div>

      {/* BRAND DASHBOARD VIEW */}
      {data.role === 'brand' && (
        <div className="space-y-8">
          
          {/* Brand Stats Bar */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
            <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-xs flex items-center justify-between">
              <div>
                <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider block">Total Briefs Posted</span>
                <span className="text-3xl font-extrabold text-indigo-600">{data.stats.total_briefs}</span>
              </div>
              <div className="w-12 h-12 rounded-xl bg-indigo-50 border border-indigo-200 flex items-center justify-center text-indigo-600">
                <Briefcase className="w-6 h-6" />
              </div>
            </div>

            <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-xs flex items-center justify-between">
              <div>
                <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider block">Active Open Briefs</span>
                <span className="text-3xl font-extrabold text-emerald-600">{data.stats.open_briefs}</span>
              </div>
              <div className="w-12 h-12 rounded-xl bg-emerald-50 border border-emerald-200 flex items-center justify-center text-emerald-600">
                <Clock className="w-6 h-6" />
              </div>
            </div>
          </div>

          {/* My Campaign Briefs List */}
          <div className="space-y-4">
            <h2 className="text-xl font-bold text-slate-900 flex items-center gap-2">
              <Briefcase className="w-5 h-5 text-indigo-600" />
              My Campaign Briefs ({data.briefs.length})
            </h2>

            {data.briefs.length === 0 ? (
              <div className="bg-white p-8 rounded-2xl border border-slate-200 text-center text-xs text-slate-500">
                You have not posted any campaign briefs yet.
              </div>
            ) : (
              <div className="space-y-4">
                {data.briefs.map(b => (
                  <div key={b.id} className="bg-white p-5 rounded-2xl border border-slate-200 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 shadow-xs hover:border-indigo-300 transition-all">
                    <div>
                      <div className="flex items-center gap-2 mb-1">
                        <span className={`px-2 py-0.5 rounded text-[10px] font-bold uppercase border ${
                          b.status === 'open' ? 'bg-emerald-50 text-emerald-700 border-emerald-200' : 'bg-slate-100 text-slate-500 border-slate-200'
                        }`}>
                          {b.status}
                        </span>
                        <span className="text-xs text-slate-400 font-mono">ID: {b.id}</span>
                      </div>
                      <h3 className="font-bold text-base text-slate-900">{b.title}</h3>
                      <p className="text-xs text-slate-500 mt-1">
                        Format: <strong className="text-slate-700">{b.content_type_name}</strong> &bull; Budget: <strong className="text-emerald-600">{formatCurrency(b.budget_min_inr)} - {formatCurrency(b.budget_max_inr)}</strong>
                      </p>
                    </div>

                    <Link
                      to={`/briefs/${b.id}`}
                      className="px-4 py-2 rounded-xl bg-indigo-50 hover:bg-indigo-600 text-indigo-700 hover:text-white text-xs font-semibold border border-indigo-200 hover:border-indigo-600 transition-all flex items-center gap-1.5 shrink-0"
                    >
                      View Matches
                      <ArrowRight className="w-3.5 h-3.5" />
                    </Link>
                  </div>
                ))}
              </div>
            )}
          </div>

        </div>
      )}

      {/* CREATOR DASHBOARD VIEW */}
      {data.role === 'creator' && (
        <div className="space-y-8">
          
          {/* Profile Completeness Bar */}
          <div className="bg-white p-6 rounded-3xl border border-slate-200 shadow-xs space-y-3">
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold text-slate-700 uppercase tracking-wider">Profile Completeness</span>
              <span className="text-sm font-extrabold text-purple-600">{data.profile_completeness}%</span>
            </div>
            
            <div className="w-full bg-slate-100 h-3 rounded-full overflow-hidden border border-slate-200">
              <div
                className="bg-gradient-to-r from-purple-600 to-indigo-600 h-full rounded-full transition-all duration-500"
                style={{ width: `${data.profile_completeness}%` }}
              />
            </div>

            {data.profile_completeness < 100 && (
              <p className="text-xs text-slate-500 pt-1">
                Tip: Complete your profile details and upload portfolio clips to increase brief match scores!
              </p>
            )}
          </div>

          {/* Matching Briefs Section */}
          <div className="space-y-4">
            <h2 className="text-xl font-bold text-slate-900 flex items-center gap-2">
              <Award className="w-5 h-5 text-purple-600" />
              Campaign Briefs Matching Your Skillset ({data.matching_briefs.length})
            </h2>

            {data.matching_briefs.length === 0 ? (
              <div className="bg-white p-8 rounded-2xl border border-slate-200 text-center text-xs text-slate-500">
                No active campaign briefs matching your profile right now.
              </div>
            ) : (
              <div className="space-y-4">
                {data.matching_briefs.map(m => (
                  <div key={m.brief.id} className="bg-white p-5 rounded-2xl border border-slate-200 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 shadow-xs hover:border-purple-300 transition-all">
                    <div>
                      <div className="flex items-center gap-2 mb-1">
                        <span className="px-2.5 py-0.5 rounded-full text-xs font-extrabold bg-purple-50 text-purple-700 border border-purple-200">
                          {m.match_score}% Match
                        </span>
                        <span className="text-xs text-slate-500 font-medium">{m.brief.brand_name}</span>
                      </div>
                      <h3 className="font-bold text-base text-slate-900">{m.brief.title}</h3>
                      <p className="text-xs text-indigo-700 font-medium mt-1 flex items-center gap-1">
                        <CheckCircle2 className="w-3.5 h-3.5 text-indigo-600" />
                        {m.match_reason}
                      </p>
                    </div>

                    <Link
                      to={`/briefs/${m.brief.id}`}
                      className="px-4 py-2 rounded-xl bg-purple-600 hover:bg-purple-500 text-white text-xs font-bold shadow-xs flex items-center gap-1.5 shrink-0"
                    >
                      View Brief
                      <ArrowRight className="w-3.5 h-3.5" />
                    </Link>
                  </div>
                ))}
              </div>
            )}
          </div>

        </div>
      )}

    </div>
  );
}
