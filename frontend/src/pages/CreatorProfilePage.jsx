import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { MapPin, Sparkles, ArrowLeft, Play, Globe, Cpu, Film } from 'lucide-react';
import { fetchCreatorById } from '../api';
import { VerificationBadge } from '../components/VerificationBadge';
import { PortfolioViewerModal } from '../components/PortfolioViewerModal';

export function CreatorProfilePage() {
  const { id } = useParams();
  const [creator, setCreator] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showFullBio, setShowFullBio] = useState(false);
  const [selectedPortfolioItem, setSelectedPortfolioItem] = useState(null);
  const [mediaFilter, setMediaFilter] = useState('all');

  useEffect(() => {
    setLoading(true);
    fetchCreatorById(id)
      .then(data => {
        setCreator(data);
        setLoading(false);
      })
      .catch(err => {
        setError(err.message);
        setLoading(false);
      });
  }, [id]);

  if (loading) {
    return (
      <div className="max-w-5xl mx-auto px-4 py-16 text-center space-y-4">
        <div className="w-20 h-20 rounded-full bg-slate-200 animate-pulse mx-auto" />
        <div className="h-6 bg-slate-200 rounded w-1/3 mx-auto animate-pulse" />
        <div className="h-4 bg-slate-200 rounded w-1/2 mx-auto animate-pulse" />
      </div>
    );
  }

  if (error || !creator) {
    return (
      <div className="max-w-md mx-auto px-4 py-16 text-center space-y-4">
        <div className="text-xl font-bold text-rose-600">Creator Not Found</div>
        <p className="text-xs text-slate-500">{error || 'Invalid Creator ID'}</p>
        <Link to="/creators" className="inline-flex items-center gap-2 text-xs text-indigo-600 hover:underline font-semibold">
          <ArrowLeft className="w-4 h-4" /> Back to Creators
        </Link>
      </div>
    );
  }

  const formatCurrency = (amount) => {
    if (!amount) return 'N/A';
    return `₹${amount.toLocaleString('en-IN')}`;
  };

  const bioThreshold = 180;
  const isBioLong = creator.bio && creator.bio.length > bioThreshold;

  const filteredPortfolio = creator.portfolio.filter(item => {
    if (mediaFilter === 'all') return true;
    return item.media_type === mediaFilter;
  });

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-10 space-y-10">
      
      {/* Back Link */}
      <Link to="/creators" className="inline-flex items-center gap-2 text-xs text-slate-500 hover:text-slate-900 transition-colors font-medium">
        <ArrowLeft className="w-4 h-4" /> Back to Creator Directory
      </Link>

      {/* Main Creator Profile Header */}
      <div className="bg-white rounded-3xl p-6 sm:p-8 border border-slate-200 relative overflow-hidden shadow-xs">
        <div className="absolute top-0 right-0 w-96 h-96 bg-gradient-to-bl from-indigo-100/60 via-purple-100/30 to-transparent blur-3xl pointer-events-none" />

        <div className="flex flex-col md:flex-row items-start justify-between gap-6">
          
          <div className="flex flex-col sm:flex-row items-start gap-6">
            <div className="relative">
              <img
                src={creator.avatar_url || 'https://picsum.photos/seed/default/200'}
                alt={creator.name}
                className="w-24 h-24 sm:w-28 sm:h-28 rounded-3xl object-cover border-4 border-slate-100 shadow-md"
              />
              <span className={`absolute bottom-1 right-1 w-5 h-5 rounded-full border-2 border-white ${
                creator.availability === 'available' ? 'bg-emerald-500' : 'bg-amber-500'
              }`} title={creator.availability === 'available' ? 'Available for new briefs' : 'Currently busy'} />
            </div>

            <div className="space-y-2">
              <div className="flex items-center gap-3 flex-wrap">
                <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900">{creator.name}</h1>
                <span className="px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider bg-indigo-50 text-indigo-700 border border-indigo-200">
                  {creator.experience_level}
                </span>
              </div>

              <div className="text-sm font-medium text-slate-600">
                {creator.specialization}
              </div>

              <div className="flex items-center gap-4 text-xs text-slate-500 flex-wrap">
                {creator.location && (
                  <span className="flex items-center gap-1">
                    <MapPin className="w-3.5 h-3.5 text-slate-400" />
                    {creator.location}
                  </span>
                )}
                {creator.languages && creator.languages.length > 0 && (
                  <span className="flex items-center gap-1">
                    <Globe className="w-3.5 h-3.5 text-slate-400" />
                    {creator.languages.join(', ')}
                  </span>
                )}
              </div>

              {/* Verification Badges */}
              <div className="flex flex-wrap gap-2 pt-1">
                {creator.tools_verified && <VerificationBadge type="tools" size="md" />}
                {creator.workflow_documented && <VerificationBadge type="workflow" size="md" />}
                {creator.past_work_linked && <VerificationBadge type="past_work" size="md" />}
              </div>
            </div>
          </div>

          {/* Rate & Availability Box */}
          <div className="bg-slate-50 p-5 rounded-2xl border border-slate-200 space-y-3 w-full md:w-64 shrink-0 shadow-xs">
            <div>
              <span className="text-[11px] font-semibold text-slate-500 uppercase tracking-wider block">Project Rate Range</span>
              <span className="text-lg font-bold text-emerald-600">
                {formatCurrency(creator.rate_min_inr)} - {formatCurrency(creator.rate_max_inr)}
              </span>
            </div>

            <div className="flex items-center justify-between text-xs pt-2 border-t border-slate-200">
              <span className="text-slate-500 font-medium">Status:</span>
              <span className={`font-bold capitalize ${creator.availability === 'available' ? 'text-emerald-600' : 'text-amber-600'}`}>
                {creator.availability}
              </span>
            </div>

            <Link
              to="/briefs/new"
              className="w-full py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-bold text-xs flex items-center justify-center gap-2 transition-all shadow-md shadow-indigo-600/20"
            >
              Invite to Brief
            </Link>
          </div>

        </div>

        {/* Bio Section with Truncate & Read More Toggle */}
        <div className="mt-8 pt-6 border-t border-slate-100">
          <h3 className="text-xs font-bold text-slate-500 uppercase tracking-wider mb-2">About & Creative Vision</h3>
          <div className="text-sm text-slate-700 leading-relaxed max-w-4xl">
            {isBioLong && !showFullBio ? (
              <>
                {creator.bio.substring(0, bioThreshold)}...
                <button
                  onClick={() => setShowFullBio(true)}
                  className="ml-2 text-indigo-600 hover:underline text-xs font-semibold"
                >
                  Read more
                </button>
              </>
            ) : (
              <>
                {creator.bio}
                {isBioLong && (
                  <button
                    onClick={() => setShowFullBio(false)}
                    className="ml-2 text-indigo-600 hover:underline text-xs font-semibold"
                  >
                    Show less
                  </button>
                )}
              </>
            )}
          </div>
        </div>

        {/* Tools & Skills Grid */}
        <div className="mt-8 grid grid-cols-1 md:grid-cols-2 gap-6 pt-6 border-t border-slate-100">
          
          {/* AI Tools Stack */}
          <div>
            <h3 className="text-xs font-bold text-slate-500 uppercase tracking-wider mb-3 flex items-center gap-1.5">
              <Cpu className="w-4 h-4 text-indigo-600" />
              Verified AI Tools ({creator.tools?.length || 0})
            </h3>
            <div className="flex flex-wrap gap-2">
              {creator.tools && creator.tools.length > 0 ? (
                creator.tools.map(t => (
                  <div key={t.id} className="px-3 py-1.5 rounded-xl bg-slate-100 text-indigo-700 border border-slate-200 text-xs font-medium flex items-center gap-2">
                    <span>{t.name}</span>
                    <span className="text-[10px] text-slate-400 uppercase">({t.category})</span>
                  </div>
                ))
              ) : (
                <span className="text-xs text-slate-400 italic">No tools listed</span>
              )}
            </div>
          </div>

          {/* Creative Skills */}
          <div>
            <h3 className="text-xs font-bold text-slate-500 uppercase tracking-wider mb-3 flex items-center gap-1.5">
              <Sparkles className="w-4 h-4 text-purple-600" />
              Specialized Skills ({creator.skills?.length || 0})
            </h3>
            <div className="flex flex-wrap gap-2">
              {creator.skills && creator.skills.length > 0 ? (
                creator.skills.map(s => (
                  <span key={s.id} className="px-3 py-1.5 rounded-xl bg-slate-100 text-purple-700 border border-slate-200 text-xs font-medium">
                    {s.name}
                  </span>
                ))
              ) : (
                <span className="text-xs text-slate-400 italic">No skills listed</span>
              )}
            </div>
          </div>

        </div>

      </div>

      {/* Portfolio Section */}
      <section className="space-y-6">
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 border-b border-slate-200 pb-4">
          <div>
            <h2 className="text-2xl font-bold text-slate-900 flex items-center gap-2.5">
              <Film className="w-6 h-6 text-indigo-600" />
              AI Portfolio & Case Studies
              <span className="text-xs px-2.5 py-0.5 rounded-full bg-slate-100 text-slate-600 font-semibold border border-slate-200">
                {creator.portfolio?.length || 0} Items
              </span>
            </h2>
            <p className="text-xs text-slate-500 mt-0.5">Click any portfolio card to view workflow breakdown and process notes.</p>
          </div>

          {/* Media Type Filter Pills */}
          <div className="flex items-center bg-slate-100 p-1 rounded-xl border border-slate-200 text-xs">
            {['all', 'video', 'animation', 'image'].map(type => (
              <button
                key={type}
                onClick={() => setMediaFilter(type)}
                className={`px-3 py-1.5 rounded-lg capitalize font-semibold transition-all ${
                  mediaFilter === type ? 'bg-indigo-600 text-white shadow-sm' : 'text-slate-600 hover:text-slate-900'
                }`}
              >
                {type}
              </button>
            ))}
          </div>
        </div>

        {/* Edge Case Handling: No Portfolio */}
        {(!creator.portfolio || creator.portfolio.length === 0) && (
          <div className="bg-white p-10 rounded-3xl text-center max-w-md mx-auto my-8 border border-slate-200 space-y-3 shadow-xs">
            <div className="w-12 h-12 rounded-full bg-slate-100 text-slate-500 flex items-center justify-center mx-auto">
              <Film className="w-6 h-6" />
            </div>
            <h3 className="text-base font-bold text-slate-900">No Portfolio Clips Uploaded Yet</h3>
            <p className="text-xs text-slate-500">
              This creator has not attached public portfolio samples to their profile yet. You can still reach out via brief requests.
            </p>
          </div>
        )}

        {/* Portfolio Grid */}
        {creator.portfolio && creator.portfolio.length > 0 && (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredPortfolio.map(item => (
              <div
                key={item.id}
                onClick={() => setSelectedPortfolioItem(item)}
                className="glass-card rounded-2xl overflow-hidden group cursor-pointer border border-slate-200 hover:border-indigo-500/50 transition-all"
              >
                {/* Thumbnail */}
                <div className="relative aspect-video bg-slate-100 overflow-hidden">
                  <img
                    src={item.thumbnail_url || 'https://picsum.photos/seed/pf/600/337'}
                    alt={item.title}
                    className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                  />
                  <div className="absolute inset-0 bg-gradient-to-t from-slate-900/60 via-transparent to-transparent opacity-80" />
                  
                  {item.media_type === 'video' && (
                    <div className="absolute inset-0 flex items-center justify-center">
                      <div className="w-12 h-12 rounded-full bg-indigo-600 text-white flex items-center justify-center shadow-lg group-hover:scale-110 transition-transform">
                        <Play className="w-6 h-6 fill-current translate-x-0.5" />
                      </div>
                    </div>
                  )}

                  <div className="absolute bottom-3 left-3 right-3 flex items-center justify-between text-xs text-white">
                    <span className="px-2 py-0.5 rounded bg-slate-900/70 backdrop-blur text-[10px] font-bold uppercase border border-white/20">
                      {item.media_type}
                    </span>
                    {item.duration_sec && (
                      <span className="px-2 py-0.5 rounded bg-slate-900/70 backdrop-blur text-[10px] font-semibold flex items-center gap-1 border border-white/20">
                        {item.duration_sec}s
                      </span>
                    )}
                  </div>
                </div>

                {/* Info */}
                <div className="p-4 space-y-2">
                  <h4 className="font-bold text-sm text-slate-900 group-hover:text-indigo-600 transition-colors line-clamp-1">
                    {item.title}
                  </h4>
                  
                  {item.workflow && (
                    <p className="text-[11px] font-mono text-purple-700 line-clamp-1 bg-purple-50 px-2 py-1 rounded border border-purple-200">
                      {item.workflow}
                    </p>
                  )}

                  <div className="flex items-center justify-between text-[11px] text-slate-500 pt-2 border-t border-slate-100">
                    <span>{item.client_name || 'Independent Work'}</span>
                    <span className="capitalize text-emerald-600 font-semibold">{item.commercial_use.replace('_', ' ')}</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}

      </section>

      {/* Portfolio Viewer Modal */}
      {selectedPortfolioItem && (
        <PortfolioViewerModal
          item={selectedPortfolioItem}
          onClose={() => setSelectedPortfolioItem(null)}
        />
      )}

    </div>
  );
}
