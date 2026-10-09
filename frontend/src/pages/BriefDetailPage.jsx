import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { ArrowLeft, Cpu, Sparkles, CheckCircle2, Award, Send, Loader2, X, DollarSign } from 'lucide-react';
import { fetchBriefById, fetchBriefMatches, applyToBrief } from '../api';
import { useAuth } from '../context/AuthContext';

export function BriefDetailPage() {
  const { id } = useParams();
  const { user } = useAuth();
  const [brief, setBrief] = useState(null);
  const [matches, setMatches] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Apply Modal state
  const [isApplyOpen, setIsApplyOpen] = useState(false);
  const [pitch, setPitch] = useState('');
  const [proposedRate, setProposedRate] = useState(25000);
  const [estimatedDays, setEstimatedDays] = useState(5);
  const [submittingApp, setSubmittingApp] = useState(false);
  const [appSuccess, setAppSuccess] = useState(null);
  const [appError, setAppError] = useState(null);

  useEffect(() => {
    setLoading(true);
    Promise.all([fetchBriefById(id), fetchBriefMatches(id)])
      .then(([briefData, matchesData]) => {
        setBrief(briefData);
        setMatches(matchesData);
        if (briefData.budget_min_inr) {
          setProposedRate(briefData.budget_min_inr);
        }
        setLoading(false);
      })
      .catch(err => {
        setError(err.message);
        setLoading(false);
      });
  }, [id]);

  const handleApplySubmit = async (e) => {
    e.preventDefault();
    setSubmittingApp(true);
    setAppError(null);

    try {
      await applyToBrief(id, {
        pitch: pitch.trim(),
        proposed_rate_inr: parseInt(proposedRate) || 10000,
        estimated_days: parseInt(estimatedDays) || 3
      });
      setAppSuccess('Your application has been submitted successfully to the brand!');
      setTimeout(() => {
        setIsApplyOpen(false);
        setAppSuccess(null);
      }, 1200);
    } catch (err) {
      setAppError(err.message || 'Failed to submit application.');
    } finally {
      setSubmittingApp(false);
    }
  };

  if (loading) {
    return (
      <div className="max-w-5xl mx-auto px-4 py-16 text-center space-y-4">
        <div className="h-8 bg-slate-200 rounded w-1/3 mx-auto animate-pulse" />
        <div className="h-4 bg-slate-200 rounded w-1/2 mx-auto animate-pulse" />
      </div>
    );
  }

  if (error || !brief) {
    return (
      <div className="max-w-md mx-auto px-4 py-16 text-center space-y-4">
        <div className="text-xl font-bold text-rose-600">Brief Not Found</div>
        <p className="text-xs text-slate-500">{error}</p>
        <Link to="/briefs" className="inline-flex items-center gap-2 text-xs text-indigo-600 hover:underline font-semibold">
          <ArrowLeft className="w-4 h-4" /> Back to Briefs List
        </Link>
      </div>
    );
  }

  const formatCurrency = (amount) => {
    if (!amount) return 'N/A';
    return `₹${amount.toLocaleString('en-IN')}`;
  };

  const getScoreColor = (score) => {
    if (score >= 80) return 'text-emerald-700 bg-emerald-50 border-emerald-200';
    if (score >= 50) return 'text-indigo-700 bg-indigo-50 border-indigo-200';
    return 'text-amber-700 bg-amber-50 border-amber-200';
  };

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-10 space-y-10">
      
      {/* Back Link */}
      <Link to="/briefs" className="inline-flex items-center gap-2 text-xs text-slate-500 hover:text-slate-900 transition-colors font-medium">
        <ArrowLeft className="w-4 h-4" /> Back to Campaign Briefs
      </Link>

      {/* Brief Overview Header */}
      <div className="bg-white rounded-3xl p-6 sm:p-8 border border-slate-200 space-y-6 shadow-xs">
        
        {/* Top Brand & Status Row */}
        <div className="flex items-start justify-between gap-4 flex-wrap">
          <div className="flex items-center gap-4">
            <img
              src={brief.brand_logo || 'https://picsum.photos/seed/brand/150'}
              alt={brief.brand_name}
              className="w-14 h-14 rounded-2xl object-cover border-2 border-slate-200 bg-slate-50"
            />
            <div>
              <span className="text-sm font-semibold text-slate-600 flex items-center gap-2">
                {brief.brand_name}
                {brief.is_agency && (
                  <span className="px-2 py-0.5 rounded bg-purple-50 text-purple-700 text-xs font-bold border border-purple-200">Agency</span>
                )}
              </span>
              <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900">{brief.title}</h1>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <span className="px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider bg-emerald-50 text-emerald-700 border border-emerald-200">
              Status: {brief.status}
            </span>

            {user?.role === 'creator' && (
              <button
                onClick={() => setIsApplyOpen(true)}
                className="px-5 py-2.5 rounded-xl bg-purple-600 hover:bg-purple-500 text-white font-bold text-xs shadow-md shadow-purple-600/20 flex items-center gap-2 transition-all hover:scale-105"
              >
                <Send className="w-4 h-4" /> Apply to Brief
              </button>
            )}
          </div>
        </div>

        {/* Deliverable Specifications Bar */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 p-4 rounded-2xl bg-slate-50 border border-slate-200 text-xs">
          <div>
            <span className="text-slate-500 uppercase tracking-wider text-[10px] block font-semibold">Budget Range</span>
            <span className="text-sm font-bold text-emerald-600">
              {formatCurrency(brief.budget_min_inr)} - {formatCurrency(brief.budget_max_inr)}
            </span>
          </div>

          <div>
            <span className="text-slate-500 uppercase tracking-wider text-[10px] block font-semibold">Content Format</span>
            <span className="text-sm font-semibold text-indigo-700">{brief.content_type_name}</span>
          </div>

          <div>
            <span className="text-slate-500 uppercase tracking-wider text-[10px] block font-semibold">Aspect Ratio / Length</span>
            <span className="text-sm font-semibold text-slate-800">{brief.aspect_ratio || '16:9'} ({brief.duration_sec || 30}s)</span>
          </div>

          <div>
            <span className="text-slate-500 uppercase tracking-wider text-[10px] block font-semibold">Buyout Clearance</span>
            <span className="text-sm font-semibold text-purple-700 capitalize">{brief.commercial_use.replace('_', ' ')}</span>
          </div>
        </div>

        {/* Goals & Description */}
        <div className="space-y-4 pt-2">
          {brief.campaign_goal && (
            <div>
              <h3 className="text-xs font-bold text-slate-500 uppercase tracking-wider mb-1">Campaign Goal</h3>
              <p className="text-sm text-slate-800 leading-relaxed font-medium">{brief.campaign_goal}</p>
            </div>
          )}

          {brief.description && (
            <div>
              <h3 className="text-xs font-bold text-slate-500 uppercase tracking-wider mb-1">Creative Description</h3>
              <p className="text-xs text-slate-600 leading-relaxed">{brief.description}</p>
            </div>
          )}
        </div>

        {/* Required Tools & Skills */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 pt-4 border-t border-slate-100">
          <div>
            <h3 className="text-xs font-bold text-slate-500 uppercase tracking-wider mb-2.5 flex items-center gap-1.5">
              <Cpu className="w-4 h-4 text-indigo-600" />
              Required AI Tools ({brief.required_tools?.length || 0})
            </h3>
            <div className="flex flex-wrap gap-1.5">
              {brief.required_tools && brief.required_tools.length > 0 ? (
                brief.required_tools.map(t => (
                  <Link
                    key={t.id}
                    to={`/tools?search=${encodeURIComponent(t.name)}`}
                    className="px-2.5 py-1 rounded-lg text-xs font-medium bg-slate-100 hover:bg-indigo-50 text-indigo-700 hover:text-indigo-900 border border-slate-200 hover:border-indigo-200 transition-colors"
                    title={`Inspect ${t.name} in directory`}
                  >
                    {t.name}
                  </Link>
                ))
              ) : (
                <span className="text-xs text-slate-400 italic">No specific tool required</span>
              )}
            </div>
          </div>

          <div>
            <h3 className="text-xs font-bold text-slate-500 uppercase tracking-wider mb-2.5 flex items-center gap-1.5">
              <Sparkles className="w-4 h-4 text-purple-600" />
              Required Creative Skills ({brief.required_skills?.length || 0})
            </h3>
            <div className="flex flex-wrap gap-1.5">
              {brief.required_skills && brief.required_skills.length > 0 ? (
                brief.required_skills.map(s => (
                  <span key={s.id} className="px-2.5 py-1 rounded-lg text-xs font-medium bg-slate-100 text-purple-700 border border-slate-200">
                    {s.name}
                  </span>
                ))
              ) : (
                <span className="text-xs text-slate-400 italic">No specific skill required</span>
              )}
            </div>
          </div>
        </div>

      </div>

      {/* Creator Match Score Section */}
      <section className="space-y-6">
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 border-b border-slate-200 pb-4">
          <div>
            <h2 className="text-2xl font-bold text-slate-900 flex items-center gap-2.5">
              <Award className="w-6 h-6 text-purple-600" />
              Ranked Creator Matches ({matches.length})
            </h2>
            <p className="text-xs text-slate-500 mt-0.5">
              Creators ranked dynamically by required tool overlap (30%), skill overlap (30%), content format (15%), budget fit (15%), and verification (10%).
            </p>
          </div>
        </div>

        {matches.length === 0 ? (
          <div className="bg-white p-8 rounded-2xl text-center text-xs text-slate-500 border border-slate-200">
            No matching creators found for this brief's requirements.
          </div>
        ) : (
          <div className="space-y-4">
            {matches.map((m, idx) => (
              <div key={m.creator.id} className="glass-card p-5 rounded-2xl border border-slate-200 flex flex-col md:flex-row items-start md:items-center justify-between gap-6 hover:border-indigo-500/50 transition-all">
                
                {/* Creator Avatar & Basic Info */}
                <div className="flex items-center gap-4 flex-1">
                  <div className="relative shrink-0">
                    <img
                      src={m.creator.avatar_url || 'https://picsum.photos/seed/default/150'}
                      alt={m.creator.name}
                      className="w-14 h-14 rounded-2xl object-cover border border-slate-200"
                    />
                    <span className="absolute -top-2 -left-2 w-6 h-6 rounded-full bg-white border border-slate-200 text-indigo-700 text-xs font-bold flex items-center justify-center shadow-xs">
                      #{idx + 1}
                    </span>
                  </div>

                  <div className="space-y-1">
                    <div className="flex items-center gap-2 flex-wrap">
                      <Link to={`/creators/${m.creator.id}`} className="font-bold text-base text-slate-900 hover:text-indigo-600 transition-colors">
                        {m.creator.name}
                      </Link>
                      <span className="text-[11px] px-2 py-0.5 rounded bg-slate-100 text-slate-700 font-medium capitalize">
                        {m.creator.experience_level}
                      </span>
                    </div>

                    <div className="text-xs text-slate-500 font-medium">
                      {m.creator.specialization} &bull; <span className="text-emerald-600 font-bold">{formatCurrency(m.creator.rate_min_inr)} - {formatCurrency(m.creator.rate_max_inr)}</span>
                    </div>

                    {/* Match Reason Banner */}
                    <div className="text-xs text-indigo-700 font-medium flex items-center gap-1.5 pt-0.5">
                      <CheckCircle2 className="w-3.5 h-3.5 text-indigo-600 shrink-0" />
                      <span>{m.match_reason}</span>
                    </div>
                  </div>
                </div>

                {/* Score Meter & Breakdown */}
                <div className="flex items-center gap-6 w-full md:w-auto justify-between md:justify-end border-t md:border-t-0 pt-3 md:pt-0 border-slate-200">
                  
                  <div className="text-center">
                    <span className={`inline-block px-3.5 py-1.5 rounded-full text-base font-extrabold border ${getScoreColor(m.match_score)}`}>
                      {m.match_score}% Match
                    </span>
                  </div>

                  <Link
                    to={`/creators/${m.creator.id}`}
                    className="px-4 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-semibold shadow-sm transition-all shrink-0"
                  >
                    View Profile
                  </Link>

                </div>

              </div>
            ))}
          </div>
        )}

      </section>

      {/* Apply to Brief Modal */}
      {isApplyOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/60 backdrop-blur-xs p-4">
          <div className="bg-white rounded-3xl max-w-lg w-full p-6 sm:p-8 border border-slate-200 shadow-2xl space-y-5">
            <div className="flex items-center justify-between border-b border-slate-100 pb-3">
              <h3 className="text-lg font-bold text-slate-900">Apply for: {brief.title}</h3>
              <button onClick={() => setIsApplyOpen(false)} className="text-slate-400 hover:text-slate-600">
                <X className="w-5 h-5" />
              </button>
            </div>

            {appSuccess && (
              <div className="p-3 bg-emerald-50 border border-emerald-200 text-emerald-800 rounded-xl text-xs font-bold flex items-center gap-2">
                <CheckCircle2 className="w-4 h-4 text-emerald-600" />
                {appSuccess}
              </div>
            )}

            {appError && (
              <div className="p-3 bg-rose-50 border border-rose-200 text-rose-700 rounded-xl text-xs font-medium">
                {appError}
              </div>
            )}

            <form onSubmit={handleApplySubmit} className="space-y-4 text-xs">
              <div>
                <label className="font-bold text-slate-700 block mb-1">Pitch / Creative Approach *</label>
                <textarea
                  rows="4"
                  required
                  value={pitch}
                  onChange={(e) => setPitch(e.target.value)}
                  placeholder="Explain how your AI pipeline, visual style, and models fit this brand's campaign vision..."
                  className="w-full px-3.5 py-2.5 rounded-xl border border-slate-300 focus:outline-none focus:border-purple-600"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="font-bold text-slate-700 block mb-1">Proposed Project Rate (₹ INR)</label>
                  <input
                    type="number"
                    required
                    value={proposedRate}
                    onChange={(e) => setProposedRate(e.target.value)}
                    className="w-full px-3.5 py-2 rounded-xl border border-slate-300 focus:outline-none focus:border-purple-600"
                  />
                </div>

                <div>
                  <label className="font-bold text-slate-700 block mb-1">Estimated Days to Deliver</label>
                  <input
                    type="number"
                    required
                    value={estimatedDays}
                    onChange={(e) => setEstimatedDays(e.target.value)}
                    className="w-full px-3.5 py-2 rounded-xl border border-slate-300 focus:outline-none focus:border-purple-600"
                  />
                </div>
              </div>

              <div className="p-3 bg-purple-50 rounded-xl border border-purple-100 text-purple-900 text-[11px]">
                🛡️ <strong>Simulated Escrow:</strong> Payment will be held in escrow upon acceptance and released when the brand approves final delivery.
              </div>

              <div className="pt-2 flex items-center justify-end gap-3">
                <button
                  type="button"
                  onClick={() => setIsApplyOpen(false)}
                  className="px-4 py-2 text-slate-500 font-semibold"
                >
                  Cancel
                </button>

                <button
                  type="submit"
                  disabled={submittingApp}
                  className="px-6 py-2.5 rounded-xl bg-purple-600 hover:bg-purple-500 text-white font-bold shadow-md flex items-center gap-2"
                >
                  {submittingApp ? <Loader2 className="w-4 h-4 animate-spin" /> : 'Submit Pitch Application'}
                </button>
              </div>

            </form>
          </div>
        </div>
      )}

    </div>
  );
}

