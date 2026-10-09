import React from 'react';
import { Link } from 'react-router-dom';
import { MapPin } from 'lucide-react';
import { VerificationBadge } from './VerificationBadge';

export function CreatorCard({ creator }) {
  const formatCurrency = (amount) => {
    if (!amount) return 'N/A';
    return `₹${amount.toLocaleString('en-IN')}`;
  };

  const experienceColors = {
    junior: 'bg-emerald-50 text-emerald-700 border-emerald-200',
    mid: 'bg-indigo-50 text-indigo-700 border-indigo-200',
    senior: 'bg-purple-50 text-purple-700 border-purple-200'
  };

  return (
    <div className="glass-card rounded-2xl p-5 flex flex-col justify-between h-full group hover:shadow-lg transition-all">
      <div>
        {/* Top Header Row */}
        <div className="flex items-start justify-between gap-3 mb-4">
          <div className="flex items-center gap-3.5">
            <div className="relative">
              <img
                src={creator.avatar_url || 'https://picsum.photos/seed/default/150'}
                alt={creator.name}
                className="w-14 h-14 rounded-2xl object-cover border-2 border-slate-200 group-hover:border-indigo-500 transition-colors shadow-sm"
              />
              <span className={`absolute -bottom-1 -right-1 w-4 h-4 rounded-full border-2 border-white ${
                creator.availability === 'available' ? 'bg-emerald-500' : 'bg-amber-500'
              }`} title={creator.availability === 'available' ? 'Available for hire' : 'Currently busy'} />
            </div>
            <div>
              <Link to={`/creators/${creator.id}`} className="font-bold text-lg text-slate-900 group-hover:text-indigo-600 transition-colors line-clamp-1">
                {creator.name}
              </Link>
              <div className="text-xs text-slate-500 font-medium line-clamp-1">
                {creator.specialization}
              </div>
              <div className="flex items-center gap-2 mt-1">
                <span className={`px-2 py-0.5 rounded-md text-[10px] font-bold uppercase tracking-wider border ${experienceColors[creator.experience_level]}`}>
                  {creator.experience_level}
                </span>
                {creator.location && (
                  <span className="text-[11px] text-slate-500 flex items-center gap-1">
                    <MapPin className="w-3 h-3 text-slate-400" />
                    {creator.location}
                  </span>
                )}
              </div>
            </div>
          </div>
        </div>

        {/* Bio / Headline */}
        <p className="text-xs text-slate-600 line-clamp-2 leading-relaxed mb-4">
          {creator.headline || creator.bio}
        </p>

        {/* Verification Badges */}
        <div className="flex flex-wrap gap-1.5 mb-4">
          {creator.tools_verified && <VerificationBadge type="tools" size="sm" />}
          {creator.workflow_documented && <VerificationBadge type="workflow" size="sm" />}
          {creator.past_work_linked && <VerificationBadge type="past_work" size="sm" />}
        </div>

        {/* Tools Stack Chips */}
        <div className="mb-4">
          <span className="text-[11px] font-semibold text-slate-500 uppercase tracking-wider block mb-1.5">
            AI Tool Stack
          </span>
          <div className="flex flex-wrap gap-1.5">
            {creator.tools && creator.tools.length > 0 ? (
              creator.tools.slice(0, 4).map(t => (
                <span key={t.id} className="px-2 py-1 rounded-md text-xs font-medium bg-slate-100 text-indigo-700 border border-slate-200">
                  {t.name}
                </span>
              ))
            ) : (
              <span className="text-xs text-slate-400">No tools specified</span>
            )}
            {creator.tools && creator.tools.length > 4 && (
              <span className="px-2 py-1 rounded-md text-xs font-medium bg-slate-100 text-slate-500 border border-slate-200">
                +{creator.tools.length - 4} more
              </span>
            )}
          </div>
        </div>
      </div>

      {/* Card Footer: Rate & Action Link */}
      <div className="pt-4 border-t border-slate-100 flex items-center justify-between mt-auto">
        <div>
          <span className="text-[10px] font-semibold text-slate-400 uppercase tracking-wider block">Rate / Project</span>
          <span className="text-sm font-bold text-emerald-600 flex items-center gap-0.5">
            {formatCurrency(creator.rate_min_inr)} - {formatCurrency(creator.rate_max_inr)}
          </span>
        </div>

        <Link
          to={`/creators/${creator.id}`}
          className="px-3 py-1.5 rounded-lg bg-indigo-50 hover:bg-indigo-600 text-indigo-700 hover:text-white text-xs font-semibold border border-indigo-200 hover:border-indigo-600 transition-all"
        >
          View Profile
        </Link>
      </div>
    </div>
  );
}
