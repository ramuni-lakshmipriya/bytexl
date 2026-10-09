import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { LayoutDashboard, PlusCircle, Briefcase, Award, CheckCircle2, UserCheck, Building2, ArrowRight, Clock, Sparkles, FolderPlus, Send, Settings, Eye } from 'lucide-react';
import { fetchDashboard, fetchCreatorById } from '../api';
import { useAuth } from '../context/AuthContext';
import { StarterStudio } from '../components/StarterStudio';
import { PortfolioManagerModal } from '../components/PortfolioManagerModal';
import { EngagementTracker } from '../components/EngagementTracker';

export function DashboardPage() {
  const { user } = useAuth();
  const [data, setData] = useState(null);
  const [creatorDetail, setCreatorDetail] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState('studio'); // 'studio' | 'briefs' | 'applications' | 'portfolio'
  
  // Portfolio modal state
  const [isPortfolioModalOpen, setIsPortfolioModalOpen] = useState(false);
  const [initialStudioProject, setInitialStudioProject] = useState(null);
  const [editingPortfolioItem, setEditingPortfolioItem] = useState(null);

  const loadDashboardData = () => {
    setLoading(true);
    fetchDashboard()
      .then(res => {
        setData(res);
        if (res.role === 'creator' && res.creator?.id) {
          fetchCreatorById(res.creator.id)
            .then(cd => setCreatorDetail(cd))
            .catch(() => {});
        }
        setLoading(false);
      })
      .catch(err => {
        setError(err.message);
        setLoading(false);
      });
  };

  useEffect(() => {
    loadDashboardData();
  }, []);

  const handleOpenAddPortfolio = (studioProj = null) => {
    setEditingPortfolioItem(null);
    setInitialStudioProject(studioProj);
    setIsPortfolioModalOpen(true);
  };

  const handleOpenEditPortfolio = (item) => {
    setInitialStudioProject(null);
    setEditingPortfolioItem(item);
    setIsPortfolioModalOpen(true);
  };

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
          <div className="flex items-center gap-3">
            <Link
              to="/briefs/new"
              className="px-5 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-bold text-xs shadow-md shadow-indigo-600/20 flex items-center gap-2 transition-all hover:scale-105"
            >
              <PlusCircle className="w-4 h-4" />
              Post New Campaign Brief
            </Link>
          </div>
        ) : (
          <div className="flex items-center gap-3">
            <Link
              to="/creator/onboarding"
              className="px-4 py-2.5 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-700 font-bold text-xs border border-slate-200 flex items-center gap-1.5 transition-all"
            >
              <Settings className="w-4 h-4 text-purple-600" />
              Edit Onboarding Profile
            </Link>

            <Link
              to={`/creators/${user.creator_id}`}
              className="px-5 py-2.5 rounded-xl bg-purple-600 hover:bg-purple-500 text-white font-bold text-xs shadow-md shadow-purple-600/20 flex items-center gap-2 transition-all hover:scale-105"
            >
              <Eye className="w-4 h-4" />
              View Public Profile
            </Link>
          </div>
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
              My Campaign Briefs & Applications ({data.briefs.length})
            </h2>

            {data.briefs.length === 0 ? (
              <div className="bg-white p-8 rounded-2xl border border-slate-200 text-center text-xs text-slate-500">
                You have not posted any campaign briefs yet.
              </div>
            ) : (
              <div className="space-y-6">
                {data.briefs.map(b => (
                  <div key={b.id} className="bg-white p-6 rounded-3xl border border-slate-200 space-y-4 shadow-xs">
                    
                    <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 border-b border-slate-100 pb-4">
                      <div>
                        <div className="flex items-center gap-2 mb-1">
                          <span className={`px-2 py-0.5 rounded text-[10px] font-bold uppercase border ${
                            b.status === 'open' ? 'bg-emerald-50 text-emerald-700 border-emerald-200' : 'bg-slate-100 text-slate-500 border-slate-200'
                          }`}>
                            {b.status}
                          </span>
                          <span className="text-xs text-slate-400 font-mono">ID: {b.id}</span>
                        </div>
                        <h3 className="font-bold text-lg text-slate-900">{b.title}</h3>
                        <p className="text-xs text-slate-500 mt-1">
                          Format: <strong className="text-slate-700">{b.content_type_name}</strong> &bull; Budget: <strong className="text-emerald-600">{formatCurrency(b.budget_min_inr)} - {formatCurrency(b.budget_max_inr)}</strong>
                        </p>
                      </div>

                      <Link
                        to={`/briefs/${b.id}`}
                        className="px-4 py-2 rounded-xl bg-indigo-50 hover:bg-indigo-600 text-indigo-700 hover:text-white text-xs font-semibold border border-indigo-200 hover:border-indigo-600 transition-all flex items-center gap-1.5 shrink-0"
                      >
                        View AI Matches
                        <ArrowRight className="w-3.5 h-3.5" />
                      </Link>
                    </div>

                    {/* Applicants for this brief */}
                    <EngagementTracker user={user} briefId={b.id} />

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
          
          {/* Profile Completeness Checklist & Bar */}
          <div className="bg-white p-6 sm:p-8 rounded-3xl border border-slate-200 shadow-xs space-y-4">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
              <div>
                <span className="text-xs font-bold text-slate-500 uppercase tracking-wider block">Creator Profile Completeness</span>
                <h3 className="text-xl font-extrabold text-slate-900">{data.profile_completeness}% Complete</h3>
              </div>

              <Link
                to="/creator/onboarding"
                className="px-4 py-2 rounded-xl bg-purple-100 text-purple-700 hover:bg-purple-200 font-bold text-xs flex items-center gap-1.5 self-start"
              >
                <Settings className="w-4 h-4" /> Edit Profile Details
              </Link>
            </div>
            
            <div className="w-full bg-slate-100 h-3 rounded-full overflow-hidden border border-slate-200">
              <div
                className="bg-gradient-to-r from-purple-600 to-indigo-600 h-full rounded-full transition-all duration-500"
                style={{ width: `${data.profile_completeness}%` }}
              />
            </div>

            {/* Checklist Badges */}
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 pt-2 text-xs">
              <div className="p-2.5 rounded-xl bg-slate-50 border border-slate-200 flex items-center gap-2">
                <CheckCircle2 className={`w-4 h-4 ${data.creator?.headline ? 'text-emerald-500' : 'text-slate-300'}`} />
                <span className="font-semibold text-slate-700">Headline & Bio</span>
              </div>
              <div className="p-2.5 rounded-xl bg-slate-50 border border-slate-200 flex items-center gap-2">
                <CheckCircle2 className={`w-4 h-4 ${data.creator?.tools?.length > 0 ? 'text-emerald-500' : 'text-slate-300'}`} />
                <span className="font-semibold text-slate-700">AI Tools Tagged ({data.creator?.tools?.length || 0})</span>
              </div>
              <div className="p-2.5 rounded-xl bg-slate-50 border border-slate-200 flex items-center gap-2">
                <CheckCircle2 className={`w-4 h-4 ${data.creator?.portfolio_count > 0 ? 'text-emerald-500' : 'text-slate-300'}`} />
                <span className="font-semibold text-slate-700">Portfolio Items ({data.creator?.portfolio_count || 0})</span>
              </div>
              <div className="p-2.5 rounded-xl bg-slate-50 border border-slate-200 flex items-center gap-2">
                <CheckCircle2 className={`w-4 h-4 ${data.creator?.workflow_documented ? 'text-emerald-500' : 'text-slate-300'}`} />
                <span className="font-semibold text-slate-700">Workflow Verified</span>
              </div>
            </div>
          </div>

          {/* Navigation Tabs */}
          <div className="flex items-center gap-2 border-b border-slate-200 pb-2 overflow-x-auto">
            <button
              onClick={() => setActiveTab('studio')}
              className={`px-4 py-2 rounded-xl text-xs font-bold transition-all flex items-center gap-2 ${
                activeTab === 'studio'
                  ? 'bg-purple-600 text-white shadow-xs'
                  : 'bg-white text-slate-600 hover:bg-slate-100 border border-slate-200'
              }`}
            >
              <Sparkles className="w-4 h-4" /> Starter Studio Recommendations
            </button>

            <button
              onClick={() => setActiveTab('briefs')}
              className={`px-4 py-2 rounded-xl text-xs font-bold transition-all flex items-center gap-2 ${
                activeTab === 'briefs'
                  ? 'bg-purple-600 text-white shadow-xs'
                  : 'bg-white text-slate-600 hover:bg-slate-100 border border-slate-200'
              }`}
            >
              <Award className="w-4 h-4" /> Skill-Matched Briefs ({data.matching_briefs.length})
            </button>

            <button
              onClick={() => setActiveTab('applications')}
              className={`px-4 py-2 rounded-xl text-xs font-bold transition-all flex items-center gap-2 ${
                activeTab === 'applications'
                  ? 'bg-purple-600 text-white shadow-xs'
                  : 'bg-white text-slate-600 hover:bg-slate-100 border border-slate-200'
              }`}
            >
              <Send className="w-4 h-4" /> My Applications & Deliveries
            </button>

            <button
              onClick={() => setActiveTab('portfolio')}
              className={`px-4 py-2 rounded-xl text-xs font-bold transition-all flex items-center gap-2 ${
                activeTab === 'portfolio'
                  ? 'bg-purple-600 text-white shadow-xs'
                  : 'bg-white text-slate-600 hover:bg-slate-100 border border-slate-200'
              }`}
            >
              <FolderPlus className="w-4 h-4" /> Manage My Portfolio ({creatorDetail?.portfolio?.length || data.creator?.portfolio_count || 0})
            </button>
          </div>

          {/* TAB 1: Starter Studio Recommendations */}
          {activeTab === 'studio' && (
            <StarterStudio
              creator={data.creator}
              onOpenAddPortfolio={handleOpenAddPortfolio}
            />
          )}

          {/* TAB 2: Skill-Matched Briefs */}
          {activeTab === 'briefs' && (
            <div className="space-y-4">
              <h2 className="text-xl font-bold text-slate-900 flex items-center gap-2">
                <Award className="w-5 h-5 text-purple-600" />
                Campaign Briefs Matching Your Skillset ({data.matching_briefs.length})
              </h2>

              {data.matching_briefs.length === 0 ? (
                <div className="bg-white p-8 rounded-3xl border border-slate-200 text-center text-xs text-slate-500">
                  No active campaign briefs matching your profile right now. Update your profile skills to see more!
                </div>
              ) : (
                <div className="space-y-4">
                  {data.matching_briefs.map(m => (
                    <div key={m.brief.id} className="bg-white p-5 rounded-3xl border border-slate-200 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 shadow-xs hover:border-purple-300 transition-all">
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
                        Apply / View Brief
                        <ArrowRight className="w-3.5 h-3.5" />
                      </Link>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}

          {/* TAB 3: My Applications & Deliveries */}
          {activeTab === 'applications' && (
            <EngagementTracker user={user} />
          )}

          {/* TAB 4: Manage My Portfolio */}
          {activeTab === 'portfolio' && (
            <div className="bg-white rounded-3xl p-6 sm:p-8 border border-slate-200 space-y-6">
              
              <div className="flex items-center justify-between border-b border-slate-100 pb-4">
                <div>
                  <h3 className="text-xl font-bold text-slate-900">Manage Your Portfolio Works</h3>
                  <p className="text-xs text-slate-500">Add new generative video/art samples or edit production workflow notes.</p>
                </div>

                <button
                  onClick={() => handleOpenAddPortfolio()}
                  className="px-4 py-2 bg-purple-600 hover:bg-purple-500 text-white font-bold text-xs rounded-xl shadow-xs flex items-center gap-2"
                >
                  <PlusCircle className="w-4 h-4" /> Add New Portfolio Work
                </button>
              </div>

              {!creatorDetail?.portfolio || creatorDetail.portfolio.length === 0 ? (
                <div className="p-12 text-center bg-slate-50 rounded-2xl border border-dashed border-slate-300 space-y-3">
                  <FolderPlus className="w-10 h-10 text-slate-400 mx-auto" />
                  <h4 className="font-bold text-slate-700">Empty Portfolio</h4>
                  <p className="text-xs text-slate-500 max-w-sm mx-auto">
                    You haven't uploaded any portfolio works yet. Use Starter Studio or click below to publish your first work!
                  </p>
                  <button
                    onClick={() => handleOpenAddPortfolio()}
                    className="px-5 py-2.5 bg-purple-600 text-white font-bold text-xs rounded-xl shadow-md"
                  >
                    Add Your First Work
                  </button>
                </div>
              ) : (
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
                  {creatorDetail.portfolio.map(item => (
                    <div key={item.id} className="bg-white border border-slate-200 rounded-2xl overflow-hidden shadow-xs hover:shadow-md transition-all group">
                      <div className="relative h-44 bg-slate-900">
                        <img
                          src={item.thumbnail_url || 'https://picsum.photos/seed/pf/400/300'}
                          alt={item.title}
                          className="w-full h-full object-cover group-hover:scale-105 transition-all duration-300 opacity-90"
                        />
                        <span className="absolute top-2 right-2 px-2 py-0.5 rounded bg-slate-900/80 text-white text-[10px] font-mono backdrop-blur-xs">
                          {item.aspect_ratio || '16:9'}
                        </span>
                      </div>

                      <div className="p-4 space-y-2">
                        <h4 className="font-bold text-sm text-slate-900 line-clamp-1">{item.title}</h4>
                        <p className="text-[11px] text-purple-700 font-mono line-clamp-1">{item.workflow || 'No workflow documented'}</p>
                        
                        <div className="pt-2 border-t border-slate-100 flex items-center justify-between">
                          <span className="text-[10px] px-2 py-0.5 rounded bg-emerald-50 text-emerald-700 border border-emerald-200 font-semibold">
                            {item.commercial_use === 'cleared' ? 'Cleared Commercial' : item.commercial_use}
                          </span>

                          <button
                            onClick={() => handleOpenEditPortfolio(item)}
                            className="px-3 py-1 bg-slate-100 hover:bg-purple-100 text-slate-700 hover:text-purple-700 rounded-lg text-xs font-bold transition-all"
                          >
                            Edit
                          </button>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}

            </div>
          )}

        </div>
      )}

      {/* Portfolio Manager Modal */}
      <PortfolioManagerModal
        isOpen={isPortfolioModalOpen}
        onClose={() => setIsPortfolioModalOpen(false)}
        initialProject={initialStudioProject}
        editItem={editingPortfolioItem}
        onSaved={() => loadDashboardData()}
      />

    </div>
  );
}

