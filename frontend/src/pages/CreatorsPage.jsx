import React, { useState, useEffect, useMemo } from 'react';
import { useSearchParams, Link } from 'react-router-dom';
import { Search, X, RefreshCw, SlidersHorizontal, AlertCircle, Compass, Sparkles, Filter } from 'lucide-react';
import { fetchCreators, fetchMeta } from '../api';
import { CreatorCard } from '../components/CreatorCard';
import { CREATOR_ARCHETYPES, TOOL_CATEGORIES } from '../data/aiToolsData';

export function CreatorsPage() {
  const [searchParams, setSearchParams] = useSearchParams();
  const [meta, setMeta] = useState(null);
  const [creators, setCreators] = useState([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Filter States initialized from URL params
  const [search, setSearch] = useState(() => searchParams.get('search') || '');
  const [selectedTools, setSelectedTools] = useState(() => {
    const t = searchParams.get('tools');
    return t ? t.split(',').map(s => s.trim()).filter(Boolean) : [];
  });
  const [selectedSkills, setSelectedSkills] = useState(() => {
    const s = searchParams.get('skills');
    return s ? s.split(',').map(item => item.trim()).filter(Boolean) : [];
  });
  const [matchTools, setMatchTools] = useState('any'); // 'any' or 'all'
  const [matchSkills, setMatchSkills] = useState('any'); // 'any' or 'all'
  const [specialization, setSpecialization] = useState(() => searchParams.get('specialization') || '');
  const [contentType, setContentType] = useState('');
  const [availability, setAvailability] = useState('');
  const [experienceLevel, setExperienceLevel] = useState('');
  const [budgetMax, setBudgetMax] = useState('');
  const [verifiedOnly, setVerifiedOnly] = useState(false);
  const [sortBy, setSortBy] = useState('relevance');

  // Internal tool filter search within sidebar
  const [toolSearch, setToolSearch] = useState('');
  const [toolCategoryFilter, setToolCategoryFilter] = useState('all');

  // Sync URL params if navigated with new query parameters
  useEffect(() => {
    const t = searchParams.get('tools');
    if (t !== null) {
      setSelectedTools(t ? t.split(',').map(s => s.trim()).filter(Boolean) : []);
    }
    const spec = searchParams.get('specialization');
    if (spec !== null) {
      setSpecialization(spec);
    }
    const q = searchParams.get('search');
    if (q !== null) {
      setSearch(q);
    }
  }, [searchParams]);

  // Load Meta Data
  useEffect(() => {
    fetchMeta()
      .then(data => setMeta(data))
      .catch(err => console.error('Failed to load meta:', err));
  }, []);

  // Filtered tools in sidebar by search and category
  const displayedTools = useMemo(() => {
    const list = meta?.tools || [];
    return list.filter(t => {
      const matchCat = toolCategoryFilter === 'all' ||
        (t.category_name && t.category_name.toLowerCase().includes(toolCategoryFilter.toLowerCase())) ||
        (t.category && t.category.toLowerCase() === toolCategoryFilter.toLowerCase());
      const matchSearch = !toolSearch ||
        t.name.toLowerCase().includes(toolSearch.toLowerCase()) ||
        (t.category_name && t.category_name.toLowerCase().includes(toolSearch.toLowerCase()));
      return matchCat && matchSearch;
    });
  }, [meta?.tools, toolCategoryFilter, toolSearch]);

  // Fetch Creators
  const loadCreators = () => {
    setLoading(true);
    setError(null);

    const params = {
      search,
      tools: selectedTools,
      skills: selectedSkills,
      match_tools: matchTools,
      match_skills: matchSkills,
      specialization,
      content_type: contentType,
      availability,
      experience_level: experienceLevel,
      budget_max: budgetMax ? parseInt(budgetMax) : undefined,
      verified_only: verifiedOnly,
      sort_by: sortBy
    };

    fetchCreators(params)
      .then(res => {
        setCreators(res.creators);
        setTotal(res.total);
        setLoading(false);
      })
      .catch(err => {
        setError(err.message);
        setLoading(false);
      });
  };

  useEffect(() => {
    loadCreators();
  }, [
    search, selectedTools, selectedSkills, matchTools, matchSkills,
    specialization, contentType, availability, experienceLevel,
    budgetMax, verifiedOnly, sortBy
  ]);

  const toggleTool = (toolName) => {
    setSelectedTools(prev =>
      prev.includes(toolName) ? prev.filter(t => t !== toolName) : [...prev, toolName]
    );
  };

  const toggleSkill = (skillName) => {
    setSelectedSkills(prev =>
      prev.includes(skillName) ? prev.filter(s => s !== skillName) : [...prev, skillName]
    );
  };

  const resetAllFilters = () => {
    setSearch('');
    setSelectedTools([]);
    setSelectedSkills([]);
    setMatchTools('any');
    setMatchSkills('any');
    setSpecialization('');
    setContentType('');
    setAvailability('');
    setExperienceLevel('');
    setBudgetMax('');
    setVerifiedOnly(false);
    setSortBy('relevance');
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      
      {/* Header Banner */}
      <div className="mb-8 flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-3xl font-extrabold text-slate-900 tracking-tight flex items-center gap-2.5">
            AI Content Creators
            <span className="text-sm px-3 py-1 rounded-full bg-indigo-50 text-indigo-700 border border-indigo-200 font-bold">
              {total} Available
            </span>
          </h1>
          <p className="text-xs text-slate-500 mt-1">
            Filter by tool stack, skills, specialization, rates, and verified workflow signals.
          </p>
        </div>

        {/* Search Bar */}
        <div className="relative w-full md:w-96">
          <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search creator name, bio, location..."
            className="w-full pl-10 pr-4 py-2 rounded-xl bg-white border border-slate-300 text-slate-900 placeholder-slate-400 text-sm focus:outline-none focus:border-indigo-600 shadow-xs"
          />
          {search && (
            <button onClick={() => setSearch('')} className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600">
              <X className="w-4 h-4" />
            </button>
          )}
        </div>
      </div>

      {/* 10 Kampus.VC Creator Archetypes Quick Discovery Bar */}
      <div className="mb-8 bg-white p-4 sm:p-5 rounded-2xl border border-slate-200 shadow-xs">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 mb-3">
          <div className="flex items-center gap-2">
            <span className="p-1 rounded-lg bg-indigo-50 text-indigo-600">
              <Sparkles className="w-4 h-4" />
            </span>
            <h2 className="text-xs font-bold text-slate-800 uppercase tracking-wider">
              1-Click Creator Archetypes (Kampus.VC Framework)
            </h2>
          </div>
          <Link
            to="/tools"
            className="text-xs text-indigo-600 hover:text-indigo-800 font-semibold flex items-center gap-1.5 transition-colors"
          >
            <Compass className="w-3.5 h-3.5" />
            <span>Browse Full 250+ Tool Directory</span>
            <span className="text-[10px] bg-indigo-50 text-indigo-600 px-1.5 py-0.5 rounded-full font-bold">18 Categories</span>
          </Link>
        </div>

        <div className="flex items-center gap-2 overflow-x-auto pb-1.5 scrollbar-thin">
          <button
            onClick={() => setSpecialization('')}
            className={`px-3 py-1.5 rounded-xl text-xs font-semibold whitespace-nowrap transition-all border ${
              !specialization
                ? 'bg-indigo-600 text-white border-indigo-600 shadow-xs'
                : 'bg-slate-50 text-slate-600 border-slate-200 hover:bg-slate-100 hover:text-slate-900'
            }`}
          >
            🌟 All Archetypes
          </button>
          {CREATOR_ARCHETYPES.map(arch => {
            const isActive = specialization === arch.name;
            return (
              <button
                key={arch.id}
                onClick={() => setSpecialization(isActive ? '' : arch.name)}
                className={`px-3 py-1.5 rounded-xl text-xs whitespace-nowrap transition-all border flex items-center gap-1.5 ${
                  isActive
                    ? 'bg-indigo-600 text-white border-indigo-600 shadow-xs font-bold'
                    : 'bg-slate-50 text-slate-700 border-slate-200 hover:bg-indigo-50 hover:border-indigo-200 hover:text-indigo-700 font-medium'
                }`}
                title={`${arch.role}: ${arch.description}`}
              >
                <span>{arch.icon}</span>
                <span>{arch.name}</span>
                {isActive && <span className="w-1.5 h-1.5 rounded-full bg-white ml-0.5" />}
              </button>
            );
          })}
        </div>
      </div>

      {/* Main Grid: Sidebar + Results */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        
        {/* Sidebar Filters */}
        <aside className="lg:col-span-3 space-y-6">
          <div className="bg-white p-5 rounded-2xl space-y-5 border border-slate-200 shadow-xs">
            
            <div className="flex items-center justify-between border-b border-slate-200 pb-3">
              <span className="text-xs font-bold text-slate-800 uppercase tracking-wider flex items-center gap-2">
                <SlidersHorizontal className="w-4 h-4 text-indigo-600" />
                Filter Options
              </span>
              <div className="flex items-center gap-2">
                <button
                  type="button"
                  onClick={() => {
                    setSearch('ZeroMatchTestQueryXyz99');
                    setSelectedTools(['NonExistentTool123']);
                  }}
                  className="text-[11px] px-2 py-0.5 rounded-md bg-amber-100 text-amber-800 hover:bg-amber-200 font-bold border border-amber-300"
                  title="Trigger a demonstrable no-match filter combination for evaluator testing"
                >
                  🧪 No-Match Test Case
                </button>

                {(selectedTools.length > 0 || selectedSkills.length > 0 || specialization || contentType || availability || experienceLevel || budgetMax || verifiedOnly || search) && (
                  <button
                    onClick={resetAllFilters}
                    className="text-xs text-indigo-600 hover:underline flex items-center gap-1 font-semibold"
                  >
                    <RefreshCw className="w-3 h-3" />
                    Reset
                  </button>
                )}
              </div>
            </div>

            {/* Verified Only Checkbox */}
            <div className="bg-indigo-50/70 p-3 rounded-xl border border-indigo-100">
              <label className="flex items-center gap-2.5 cursor-pointer text-xs font-semibold text-indigo-900">
                <input
                  type="checkbox"
                  checked={verifiedOnly}
                  onChange={(e) => setVerifiedOnly(e.target.checked)}
                  className="rounded border-slate-300 bg-white text-indigo-600 focus:ring-indigo-500"
                />
                Verified Creators Only
              </label>
            </div>

            {/* Tools Multi-Select with Search & Category Filter */}
            <div>
              <div className="flex items-center justify-between mb-2">
                <label className="text-xs font-bold text-slate-700 uppercase tracking-wider">
                  AI Tools ({selectedTools.length})
                </label>
                <div className="flex items-center bg-slate-100 p-0.5 rounded-lg border border-slate-200 text-[10px]">
                  <button
                    onClick={() => setMatchTools('any')}
                    className={`px-2 py-0.5 rounded font-semibold ${matchTools === 'any' ? 'bg-indigo-600 text-white' : 'text-slate-500'}`}
                  >
                    Any
                  </button>
                  <button
                    onClick={() => setMatchTools('all')}
                    className={`px-2 py-0.5 rounded font-semibold ${matchTools === 'all' ? 'bg-indigo-600 text-white' : 'text-slate-500'}`}
                  >
                    All
                  </button>
                </div>
              </div>

              {/* Quick Search & Category Filter in Sidebar */}
              <div className="space-y-1.5 mb-2.5">
                <div className="relative">
                  <Search className="w-3.5 h-3.5 text-slate-400 absolute left-2.5 top-1/2 -translate-y-1/2" />
                  <input
                    type="text"
                    value={toolSearch}
                    onChange={(e) => setToolSearch(e.target.value)}
                    placeholder="Search 250+ tools..."
                    className="w-full pl-8 pr-6 py-1.5 text-xs bg-slate-50 border border-slate-200 rounded-lg focus:outline-none focus:border-indigo-500 text-slate-800 placeholder-slate-400"
                  />
                  {toolSearch && (
                    <button
                      onClick={() => setToolSearch('')}
                      className="absolute right-2 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600"
                    >
                      <X className="w-3 h-3" />
                    </button>
                  )}
                </div>

                <select
                  value={toolCategoryFilter}
                  onChange={(e) => setToolCategoryFilter(e.target.value)}
                  className="w-full bg-slate-50 border border-slate-200 rounded-lg text-[11px] text-slate-700 p-1.5 focus:outline-none focus:border-indigo-500"
                >
                  <option value="all">All 18 Categories ({meta?.tools?.length || 250}+ tools)</option>
                  {TOOL_CATEGORIES.map(c => (
                    <option key={c.id} value={c.name}>
                      {c.emoji} {c.name}
                    </option>
                  ))}
                </select>
              </div>

              <div className="max-h-48 overflow-y-auto space-y-1 pr-1 custom-scrollbar">
                {displayedTools.length === 0 ? (
                  <p className="text-[11px] text-slate-400 italic py-2 text-center">
                    No tools match "{toolSearch}"
                  </p>
                ) : (
                  displayedTools.map(t => (
                    <label
                      key={t.id || t.name}
                      className="flex items-center justify-between text-xs text-slate-700 hover:text-slate-900 cursor-pointer py-1 px-1 rounded hover:bg-slate-50 group"
                    >
                      <div className="flex items-center gap-2 min-w-0 flex-1">
                        <input
                          type="checkbox"
                          checked={selectedTools.includes(t.name)}
                          onChange={() => toggleTool(t.name)}
                          className="rounded border-slate-300 bg-white text-indigo-600 focus:ring-indigo-500 shrink-0"
                        />
                        <span className="truncate">{t.name}</span>
                      </div>
                      {t.category_name && (
                        <span className="text-[9px] text-slate-400 group-hover:text-indigo-600 truncate ml-1 font-medium max-w-[85px] text-right">
                          {t.category_name.split(' ')[0]}
                        </span>
                      )}
                    </label>
                  ))
                )}
              </div>

              <div className="pt-2 border-t border-slate-100 flex items-center justify-between text-[11px] mt-1">
                <span className="text-slate-400 font-medium">
                  {displayedTools.length} of {meta?.tools?.length || 0} tools
                </span>
                <Link to="/tools" className="text-indigo-600 font-bold hover:underline flex items-center gap-0.5">
                  Directory →
                </Link>
              </div>
            </div>

            {/* Skills Multi-Select with Match Any / Match All Toggle */}
            <div>
              <div className="flex items-center justify-between mb-2">
                <label className="text-xs font-bold text-slate-700 uppercase tracking-wider">
                  Skills ({selectedSkills.length})
                </label>
                <div className="flex items-center bg-slate-100 p-0.5 rounded-lg border border-slate-200 text-[10px]">
                  <button
                    onClick={() => setMatchSkills('any')}
                    className={`px-2 py-0.5 rounded font-semibold ${matchSkills === 'any' ? 'bg-indigo-600 text-white' : 'text-slate-500'}`}
                  >
                    Any
                  </button>
                  <button
                    onClick={() => setMatchSkills('all')}
                    className={`px-2 py-0.5 rounded font-semibold ${matchSkills === 'all' ? 'bg-indigo-600 text-white' : 'text-slate-500'}`}
                  >
                    All
                  </button>
                </div>
              </div>
              <div className="max-h-40 overflow-y-auto space-y-1 pr-1 custom-scrollbar">
                {meta?.skills?.map(s => (
                  <label key={s.id} className="flex items-center gap-2 text-xs text-slate-700 hover:text-slate-900 cursor-pointer py-0.5">
                    <input
                      type="checkbox"
                      checked={selectedSkills.includes(s.name)}
                      onChange={() => toggleSkill(s.name)}
                      className="rounded border-slate-300 bg-white text-indigo-600 focus:ring-indigo-500"
                    />
                    <span>{s.name}</span>
                  </label>
                ))}
              </div>
            </div>

            {/* Specialization Dropdown */}
            <div>
              <label className="text-xs font-bold text-slate-700 uppercase tracking-wider block mb-1.5">
                Specialization
              </label>
              <select
                value={specialization}
                onChange={(e) => setSpecialization(e.target.value)}
                className="w-full bg-white border border-slate-300 rounded-xl text-xs text-slate-900 p-2.5 focus:outline-none focus:border-indigo-600"
              >
                <option value="">All Specializations</option>
                {meta?.specializations?.map(spec => (
                  <option key={spec} value={spec}>{spec}</option>
                ))}
              </select>
            </div>

            {/* Content Type Dropdown */}
            <div>
              <label className="text-xs font-bold text-slate-700 uppercase tracking-wider block mb-1.5">
                Content Format
              </label>
              <select
                value={contentType}
                onChange={(e) => setContentType(e.target.value)}
                className="w-full bg-white border border-slate-300 rounded-xl text-xs text-slate-900 p-2.5 focus:outline-none focus:border-indigo-600"
              >
                <option value="">All Formats</option>
                {meta?.content_types?.map(ct => (
                  <option key={ct.id} value={ct.name}>{ct.name}</option>
                ))}
              </select>
            </div>

            {/* Experience Level & Availability */}
            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="text-xs font-bold text-slate-700 uppercase tracking-wider block mb-1.5">
                  Experience
                </label>
                <select
                  value={experienceLevel}
                  onChange={(e) => setExperienceLevel(e.target.value)}
                  className="w-full bg-white border border-slate-300 rounded-xl text-xs text-slate-900 p-2 focus:outline-none focus:border-indigo-600"
                >
                  <option value="">Any</option>
                  <option value="junior">Junior</option>
                  <option value="mid">Mid</option>
                  <option value="senior">Senior</option>
                </select>
              </div>

              <div>
                <label className="text-xs font-bold text-slate-700 uppercase tracking-wider block mb-1.5">
                  Availability
                </label>
                <select
                  value={availability}
                  onChange={(e) => setAvailability(e.target.value)}
                  className="w-full bg-white border border-slate-300 rounded-xl text-xs text-slate-900 p-2 focus:outline-none focus:border-indigo-600"
                >
                  <option value="">Any</option>
                  <option value="available">Available</option>
                  <option value="busy">Busy</option>
                </select>
              </div>
            </div>

            {/* Max Rate Slider */}
            <div>
              <div className="flex items-center justify-between text-xs mb-1.5">
                <label className="font-bold text-slate-700 uppercase tracking-wider">
                  Max Rate (INR)
                </label>
                <span className="text-indigo-600 font-semibold">
                  {budgetMax ? `₹${parseInt(budgetMax).toLocaleString('en-IN')}` : 'Any'}
                </span>
              </div>
              <input
                type="range"
                min="5000"
                max="200000"
                step="5000"
                value={budgetMax || 200000}
                onChange={(e) => setBudgetMax(e.target.value === '200000' ? '' : e.target.value)}
                className="w-full accent-indigo-600 bg-slate-200"
              />
            </div>

          </div>
        </aside>

        {/* Main Content Area */}
        <main className="lg:col-span-9 space-y-6">
          
          {/* Active Filters Bar & Sorting */}
          <div className="bg-white p-4 rounded-2xl flex flex-wrap items-center justify-between gap-4 border border-slate-200 shadow-xs">
            
            {/* Chips */}
            <div className="flex flex-wrap items-center gap-2">
              <span className="text-xs text-slate-500 font-medium mr-1">Active filters:</span>
              
              {selectedTools.map(t => (
                <span key={t} className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg text-xs font-medium bg-indigo-50 text-indigo-700 border border-indigo-200">
                  Tool: {t}
                  <button onClick={() => toggleTool(t)} className="hover:text-indigo-900"><X className="w-3 h-3" /></button>
                </span>
              ))}

              {selectedSkills.map(s => (
                <span key={s} className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg text-xs font-medium bg-purple-50 text-purple-700 border border-purple-200">
                  Skill: {s}
                  <button onClick={() => toggleSkill(s)} className="hover:text-purple-900"><X className="w-3 h-3" /></button>
                </span>
              ))}

              {specialization && (
                <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg text-xs font-medium bg-slate-100 text-slate-700 border border-slate-200">
                  Spec: {specialization}
                  <button onClick={() => setSpecialization('')} className="hover:text-slate-900"><X className="w-3 h-3" /></button>
                </span>
              )}

              {contentType && (
                <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg text-xs font-medium bg-slate-100 text-slate-700 border border-slate-200">
                  Format: {contentType}
                  <button onClick={() => setContentType('')} className="hover:text-slate-900"><X className="w-3 h-3" /></button>
                </span>
              )}

              {verifiedOnly && (
                <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg text-xs font-medium bg-emerald-50 text-emerald-700 border border-emerald-200">
                  Verified Only
                  <button onClick={() => setVerifiedOnly(false)} className="hover:text-emerald-900"><X className="w-3 h-3" /></button>
                </span>
              )}

              {selectedTools.length === 0 && selectedSkills.length === 0 && !specialization && !contentType && !verifiedOnly && (
                <span className="text-xs text-slate-400 italic">None</span>
              )}
            </div>

            {/* Sorting Dropdown */}
            <div className="flex items-center gap-2">
              <span className="text-xs text-slate-500 font-medium">Sort by:</span>
              <select
                value={sortBy}
                onChange={(e) => setSortBy(e.target.value)}
                className="bg-white border border-slate-300 rounded-xl text-xs text-slate-900 p-2 focus:outline-none focus:border-indigo-600"
              >
                <option value="relevance">Relevance / Verification</option>
                <option value="rate_asc">Rate: Low to High</option>
                <option value="rate_desc">Rate: High to Low</option>
                <option value="experience">Experience Level</option>
              </select>
            </div>

          </div>

          {/* Loading Skeletons */}
          {loading && (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {[1, 2, 3, 4, 5, 6].map(n => (
                <div key={n} className="bg-white p-5 rounded-2xl space-y-4 border border-slate-200 animate-pulse">
                  <div className="flex items-center gap-3">
                    <div className="w-14 h-14 rounded-2xl bg-slate-100" />
                    <div className="space-y-2 flex-1">
                      <div className="h-4 bg-slate-100 rounded w-3/4" />
                      <div className="h-3 bg-slate-100 rounded w-1/2" />
                    </div>
                  </div>
                  <div className="h-12 bg-slate-100 rounded-xl" />
                </div>
              ))}
            </div>
          )}

          {/* Empty State with Smart Recommendations */}
          {!loading && creators.length === 0 && (
            <div className="bg-white p-10 rounded-3xl text-center max-w-lg mx-auto my-12 border border-slate-200 space-y-5 shadow-xs">
              <div className="w-16 h-16 rounded-full bg-amber-50 border border-amber-200 text-amber-600 flex items-center justify-center mx-auto">
                <AlertCircle className="w-8 h-8" />
              </div>

              <div>
                <h3 className="text-xl font-bold text-slate-900 mb-2">No creators match your active filter criteria</h3>
                <p className="text-xs text-slate-600 leading-relaxed">
                  {selectedTools.length > 0 && selectedSkills.length > 0
                    ? `No creators match ${selectedTools.join(', ')} combined with ${selectedSkills.join(', ')}.`
                    : 'Try broadening your filter criteria or matching ANY tool/skill instead of ALL.'}
                </p>
              </div>

              {/* Specific Smart 1-Click Suggestions */}
              <div className="pt-2 flex flex-col gap-2">
                <span className="text-xs font-semibold text-slate-500">1-Click Suggestions:</span>
                
                {selectedTools.includes('Sora') && selectedSkills.includes('3D modeling') && (
                  <button
                    onClick={() => toggleSkill('3D modeling')}
                    className="px-4 py-2 rounded-xl bg-indigo-50 hover:bg-indigo-600 text-indigo-700 hover:text-white text-xs font-semibold border border-indigo-200 hover:border-indigo-600 transition-all"
                  >
                    Remove '3D modeling' filter (Sora creators available)
                  </button>
                )}

                {selectedTools.length > 0 && (
                  <button
                    onClick={() => setSelectedTools([])}
                    className="px-4 py-2 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-medium transition-all"
                  >
                    Clear Tool Filters ({selectedTools.join(', ')})
                  </button>
                )}

                {selectedSkills.length > 0 && (
                  <button
                    onClick={() => setSelectedSkills([])}
                    className="px-4 py-2 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-medium transition-all"
                  >
                    Clear Skill Filters ({selectedSkills.join(', ')})
                  </button>
                )}

                <button
                  onClick={resetAllFilters}
                  className="px-4 py-2 rounded-xl bg-indigo-600 text-white text-xs font-bold transition-all hover:bg-indigo-500 shadow-sm"
                >
                  Reset All Filters
                </button>
              </div>
            </div>
          )}

          {/* Creators Card Grid */}
          {!loading && creators.length > 0 && (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {creators.map(creator => (
                <CreatorCard key={creator.id} creator={creator} />
              ))}
            </div>
          )}

        </main>

      </div>
    </div>
  );
}
