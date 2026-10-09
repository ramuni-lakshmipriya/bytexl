import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Briefcase, PlusCircle } from 'lucide-react';
import { fetchBriefs } from '../api';
import { useRole } from '../context/RoleContext';

export function BriefsPage() {
  const { role } = useRole();
  const [briefs, setBriefs] = useState([]);
  const [statusFilter, setStatusFilter] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    setLoading(true);
    fetchBriefs(statusFilter || null)
      .then(data => {
        setBriefs(data);
        setLoading(false);
      })
      .catch(err => {
        setError(err.message);
        setLoading(false);
      });
  }, [statusFilter]);

  const formatCurrency = (amount) => {
    if (!amount) return 'N/A';
    return `₹${amount.toLocaleString('en-IN')}`;
  };

  const statusStyles = {
    open: 'bg-emerald-50 text-emerald-700 border-emerald-200',
    in_review: 'bg-amber-50 text-amber-700 border-amber-200',
    closed: 'bg-slate-100 text-slate-500 border-slate-200'
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      
      {/* Header Bar */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-3">
            <h1 className="text-3xl font-extrabold text-slate-900 tracking-tight">Campaign Briefs</h1>
            <span className="text-xs px-2.5 py-1 rounded-full bg-indigo-50 text-indigo-700 border border-indigo-200 font-bold">
              {role === 'brand' ? 'Brand Management' : 'Creator Marketplace'}
            </span>
          </div>
          <p className="text-xs text-slate-500 mt-1">
            Browse open generative AI production briefs from brands and creative agencies.
          </p>
        </div>

        <Link
          to="/briefs/new"
          className="px-4 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-bold shadow-md shadow-indigo-600/20 flex items-center gap-2 transition-all hover:scale-105"
        >
          <PlusCircle className="w-4 h-4" />
          Create New Brief
        </Link>
      </div>

      {/* Filter Tabs */}
      <div className="bg-white p-2 rounded-2xl flex items-center justify-between gap-4 border border-slate-200 shadow-xs">
        <div className="flex items-center gap-1">
          {[
            { id: '', label: 'All Statuses' },
            { id: 'open', label: 'Open' },
            { id: 'in_review', label: 'In Review' },
            { id: 'closed', label: 'Closed' }
          ].map(tab => (
            <button
              key={tab.id}
              onClick={() => setStatusFilter(tab.id)}
              className={`px-4 py-2 rounded-xl text-xs font-semibold transition-all ${
                statusFilter === tab.id
                  ? 'bg-indigo-50 text-indigo-700 border border-indigo-200 shadow-xs'
                  : 'text-slate-500 hover:text-slate-900'
              }`}
            >
              {tab.label}
            </button>
          ))}
        </div>

        <span className="text-xs text-slate-500 font-medium px-3">
          Showing {briefs.length} briefs
        </span>
      </div>

      {/* Loading Skeletons */}
      {loading && (
        <div className="space-y-4">
          {[1, 2, 3].map(n => (
            <div key={n} className="bg-white p-6 rounded-2xl space-y-3 border border-slate-200 animate-pulse">
              <div className="h-5 bg-slate-100 rounded w-1/3" />
              <div className="h-4 bg-slate-100 rounded w-2/3" />
            </div>
          ))}
        </div>
      )}

      {/* Empty State */}
      {!loading && briefs.length === 0 && (
        <div className="bg-white p-10 rounded-3xl text-center max-w-md mx-auto my-12 border border-slate-200 space-y-4 shadow-xs">
          <Briefcase className="w-12 h-12 text-slate-400 mx-auto" />
          <h3 className="text-lg font-bold text-slate-900">No Briefs Found</h3>
          <p className="text-xs text-slate-500">There are no campaign briefs matching the selected status filter.</p>
        </div>
      )}

      {/* Briefs Cards List */}
      {!loading && briefs.length > 0 && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {briefs.map(brief => (
            <div
              key={brief.id}
              className="glass-card rounded-2xl p-6 flex flex-col justify-between border border-slate-200 hover:border-indigo-500/50 transition-all group"
            >
              <div>
                {/* Top Row: Brand Info & Status */}
                <div className="flex items-start justify-between gap-3 mb-3">
                  <div className="flex items-center gap-3">
                    <img
                      src={brief.brand_logo || 'https://picsum.photos/seed/brand/100'}
                      alt={brief.brand_name}
                      className="w-10 h-10 rounded-xl object-cover border border-slate-200 bg-slate-50"
                    />
                    <div>
                      <span className="text-xs font-semibold text-slate-800 flex items-center gap-1.5">
                        {brief.brand_name}
                        {brief.is_agency && (
                          <span className="px-1.5 py-0.2 rounded bg-purple-50 text-purple-700 text-[10px] font-bold border border-purple-200">
                            Agency
                          </span>
                        )}
                      </span>
                      <span className="text-[10px] text-slate-400 font-mono block">
                        Posted {brief.created_at ? brief.created_at.split('T')[0] : 'recently'}
                      </span>
                    </div>
                  </div>

                  <span className={`px-2.5 py-1 rounded-full text-xs font-bold uppercase tracking-wider border ${statusStyles[brief.status]}`}>
                    {brief.status.replace('_', ' ')}
                  </span>
                </div>

                {/* Brief Title */}
                <Link to={`/briefs/${brief.id}`} className="font-bold text-lg text-slate-900 group-hover:text-indigo-600 transition-colors line-clamp-1 mb-2">
                  {brief.title}
                </Link>

                {/* Description snippet */}
                <p className="text-xs text-slate-600 line-clamp-2 leading-relaxed mb-4">
                  {brief.campaign_goal || brief.description}
                </p>

                {/* Requirements Chips */}
                <div className="space-y-3 mb-4">
                  
                  {/* Required Tools */}
                  {brief.required_tools && brief.required_tools.length > 0 && (
                    <div className="flex items-center gap-2 flex-wrap text-xs">
                      <span className="text-[11px] font-semibold text-slate-500">Required Tools:</span>
                      {brief.required_tools.map(t => (
                        <span key={t.id} className="px-2 py-0.5 rounded-md text-[11px] font-medium bg-slate-100 text-indigo-700 border border-slate-200">
                          {t.name}
                        </span>
                      ))}
                    </div>
                  )}

                  {/* Required Skills */}
                  {brief.required_skills && brief.required_skills.length > 0 && (
                    <div className="flex items-center gap-2 flex-wrap text-xs">
                      <span className="text-[11px] font-semibold text-slate-500">Required Skills:</span>
                      {brief.required_skills.map(s => (
                        <span key={s.id} className="px-2 py-0.5 rounded-md text-[11px] font-medium bg-slate-100 text-purple-700 border border-slate-200">
                          {s.name}
                        </span>
                      ))}
                    </div>
                  )}

                </div>
              </div>

              {/* Bottom Footer Row: Budget & View Matches Link */}
              <div className="pt-4 border-t border-slate-100 flex items-center justify-between mt-auto">
                <div>
                  <span className="text-[10px] font-semibold text-slate-400 uppercase tracking-wider block">Budget Range</span>
                  <span className="text-sm font-bold text-emerald-600">
                    {formatCurrency(brief.budget_min_inr)} - {formatCurrency(brief.budget_max_inr)}
                  </span>
                </div>

                <Link
                  to={`/briefs/${brief.id}`}
                  className="px-3.5 py-2 rounded-xl bg-indigo-50 hover:bg-indigo-600 text-indigo-700 hover:text-white text-xs font-semibold border border-indigo-200 hover:border-indigo-600 transition-all flex items-center gap-1.5"
                >
                  View Brief & Matches
                </Link>
              </div>

            </div>
          ))}
        </div>
      )}

    </div>
  );
}
