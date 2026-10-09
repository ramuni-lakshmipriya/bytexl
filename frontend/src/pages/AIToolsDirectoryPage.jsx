import React, { useState, useEffect, useMemo } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import {
  Search, ExternalLink, ShieldCheck, AlertTriangle, Sparkles,
  Layers, Users, Filter, ArrowRight, CheckCircle2, Globe, Cpu,
  BookmarkPlus, Share2, Compass, Briefcase
} from 'lucide-react';
import { fetchMeta } from '../api';
import {
  TOOL_CATEGORIES, CREATOR_ARCHETYPES,
  MARKETPLACE_PLATFORMS, ALL_TOOLS_CATALOG
} from '../data/aiToolsData';

export function AIToolsDirectoryPage() {
  const navigate = useNavigate();
  const [meta, setMeta] = useState(null);
  const [search, setSearch] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [licenseFilter, setLicenseFilter] = useState('all'); // 'all', 'yes', 'plan_dependent'
  const [selectedArchetype, setSelectedArchetype] = useState('all');

  // Load backend meta (fall back gracefully to our rich catalog)
  useEffect(() => {
    fetchMeta()
      .then(data => setMeta(data))
      .catch(err => console.log('Using offline data fallback:', err));
  }, []);

  // Merge backend tools with fallback catalog if needed
  const tools = useMemo(() => {
    if (meta?.tools && meta.tools.length > 50) {
      return meta.tools;
    }
    return ALL_TOOLS_CATALOG;
  }, [meta]);

  const categories = useMemo(() => {
    if (meta?.tool_categories && meta.tool_categories.length > 0) {
      return meta.tool_categories;
    }
    return TOOL_CATEGORIES;
  }, [meta]);

  const archetypes = useMemo(() => {
    if (meta?.creator_archetypes && meta.creator_archetypes.length > 0) {
      return meta.creator_archetypes;
    }
    return CREATOR_ARCHETYPES;
  }, [meta]);

  const platforms = useMemo(() => {
    if (meta?.marketplace_sources && meta.marketplace_sources.length > 0) {
      return meta.marketplace_sources;
    }
    return MARKETPLACE_PLATFORMS;
  }, [meta]);

  // Filtered tools
  const filteredTools = useMemo(() => {
    return tools.filter(tool => {
      // Category match
      if (selectedCategory !== 'all' && tool.category !== selectedCategory) {
        return false;
      }
      // License match
      if (licenseFilter !== 'all' && tool.commercial_use !== licenseFilter) {
        return false;
      }
      // Archetype match
      if (selectedArchetype !== 'all' && tool.popular_archetype !== selectedArchetype) {
        return false;
      }
      // Search match
      if (search.trim()) {
        const q = search.toLowerCase();
        const matchName = tool.name?.toLowerCase().includes(q);
        const matchDesc = tool.description?.toLowerCase().includes(q);
        const matchCat = (tool.category_name || tool.category)?.toLowerCase().includes(q);
        const matchArch = tool.popular_archetype?.toLowerCase().includes(q);
        return matchName || matchDesc || matchCat || matchArch;
      }
      return true;
    });
  }, [tools, selectedCategory, licenseFilter, selectedArchetype, search]);

  const handleArchetypeSelect = (archName) => {
    if (selectedArchetype === archName) {
      setSelectedArchetype('all');
    } else {
      setSelectedArchetype(archName);
    }
  };

  const handleFindCreators = (toolName) => {
    navigate(`/creators?tools=${encodeURIComponent(toolName)}`);
  };

  const handleFindArchetypeCreators = (roleName) => {
    navigate(`/creators?specialization=${encodeURIComponent(roleName)}`);
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10 space-y-12">
      
      {/* 1. Header Hero Banner */}
      <section className="relative overflow-hidden rounded-3xl bg-gradient-to-br from-indigo-900 via-slate-900 to-purple-950 text-white p-8 sm:p-12 border border-indigo-800/40 shadow-2xl">
        <div className="absolute top-0 right-0 w-96 h-96 bg-purple-500/10 rounded-full blur-3xl pointer-events-none" />
        <div className="relative z-10 max-w-4xl space-y-4">
          
          <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-white/10 backdrop-blur-md border border-white/20 text-xs font-semibold text-indigo-200">
            <Sparkles className="w-4 h-4 text-amber-300" />
            <span>Kampus.VC x GenCraft Ecosystem • 250+ Verified AI Tools</span>
          </div>

          <h1 className="text-3xl sm:text-5xl font-black tracking-tight leading-tight">
            The Complete <span className="text-transparent bg-clip-text bg-gradient-to-r from-indigo-300 via-purple-300 to-pink-300">AI Creator Tools</span> Directory
          </h1>

          <p className="text-sm sm:text-base text-slate-300 leading-relaxed font-normal max-w-3xl">
            Explore 18 curated creator categories, discover commercial usage clearance benchmarks, and connect directly with elite creators skilled in every platform. Built for brands, creative directors, and generative filmmakers.
          </p>

          {/* Quick Metrics */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 pt-4 border-t border-white/10">
            <div>
              <div className="text-2xl font-black text-white">18</div>
              <div className="text-xs text-slate-400 font-medium">Content Categories</div>
            </div>
            <div>
              <div className="text-2xl font-black text-white">{tools.length}+</div>
              <div className="text-xs text-slate-400 font-medium">Curated AI Tools</div>
            </div>
            <div>
              <div className="text-2xl font-black text-white">10</div>
              <div className="text-xs text-slate-400 font-medium">Marketplace Archetypes</div>
            </div>
            <div>
              <div className="text-2xl font-black text-emerald-400">100%</div>
              <div className="text-xs text-slate-400 font-medium">Commercial Licence Tracking</div>
            </div>
          </div>

        </div>
      </section>

      {/* 2. Marketplace Discovery Archetypes (Kampus.VC Section) */}
      <section className="space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
          <div>
            <h2 className="text-xl font-extrabold text-slate-900 tracking-tight flex items-center gap-2">
              <Compass className="w-5 h-5 text-indigo-600" />
              10 Marketplace Creator Archetypes
            </h2>
            <p className="text-xs text-slate-500">
              Discovered from Kampus.VC research: hire talent structured around production pipelines.
            </p>
          </div>
          <span className="text-xs font-semibold text-indigo-600 bg-indigo-50 border border-indigo-200 px-3 py-1 rounded-full self-start">
            1-Click Talent Filter
          </span>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-3.5">
          {archetypes.map((arch) => {
            const isSelected = selectedArchetype === arch.name;
            return (
              <div
                key={arch.id}
                className={`p-4 rounded-2xl border transition-all text-left flex flex-col justify-between ${
                  isSelected
                    ? 'bg-indigo-600 text-white border-indigo-600 shadow-md scale-102 ring-2 ring-indigo-400'
                    : 'bg-white text-slate-900 border-slate-200 hover:border-indigo-300 hover:shadow-xs'
                }`}
              >
                <div>
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-2xl">{arch.icon}</span>
                    <button
                      onClick={() => handleArchetypeSelect(arch.name)}
                      className={`text-[10px] font-bold px-2 py-0.5 rounded-md ${
                        isSelected
                          ? 'bg-white/20 text-white'
                          : 'bg-slate-100 text-slate-600 hover:bg-indigo-50 hover:text-indigo-600'
                      }`}
                    >
                      {isSelected ? 'Active Filter' : 'Filter Tools'}
                    </button>
                  </div>
                  <h3 className={`font-bold text-sm tracking-tight ${isSelected ? 'text-white' : 'text-slate-900'}`}>
                    {arch.name}
                  </h3>
                  <p className={`text-[11px] leading-relaxed mt-1 line-clamp-2 ${isSelected ? 'text-indigo-100' : 'text-slate-500'}`}>
                    {arch.description}
                  </p>

                  {/* Key tools tags */}
                  <div className="flex flex-wrap gap-1 mt-2.5">
                    {arch.key_tools.slice(0, 3).map((kt) => (
                      <span
                        key={kt}
                        className={`text-[9px] px-1.5 py-0.5 rounded font-medium ${
                          isSelected ? 'bg-indigo-700 text-indigo-100' : 'bg-slate-100 text-slate-700'
                        }`}
                      >
                        {kt}
                      </span>
                    ))}
                  </div>
                </div>

                <button
                  onClick={() => handleFindArchetypeCreators(arch.name)}
                  className={`mt-3.5 w-full py-1.5 px-2 rounded-xl text-xs font-bold flex items-center justify-center gap-1.5 transition-colors ${
                    isSelected
                      ? 'bg-white text-indigo-900 hover:bg-indigo-50'
                      : 'bg-indigo-50 text-indigo-700 hover:bg-indigo-100 border border-indigo-200'
                  }`}
                >
                  <Users className="w-3.5 h-3.5" />
                  Find {arch.name.replace('AI ', '')}s
                </button>
              </div>
            );
          })}
        </div>
      </section>

      {/* 3. Search & Interactive Filter Controls */}
      <section className="bg-white p-6 rounded-3xl border border-slate-200 shadow-xs space-y-5">
        
        <div className="flex flex-col md:flex-row items-center justify-between gap-4">
          
          {/* Live Search */}
          <div className="relative w-full md:w-96">
            <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
            <input
              type="text"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Search 250+ tools by name, category, or workflow..."
              className="w-full pl-10 pr-4 py-2.5 rounded-xl bg-slate-50 border border-slate-300 text-slate-900 placeholder-slate-400 text-xs focus:outline-none focus:border-indigo-600 focus:bg-white"
            />
          </div>

          {/* Licensing & Filters */}
          <div className="flex items-center gap-3 w-full md:w-auto flex-wrap">
            
            <div className="flex items-center gap-1.5 text-xs font-medium text-slate-600 bg-slate-50 p-1 rounded-xl border border-slate-200">
              <span className="px-2 text-slate-400 text-[11px] font-bold">Licence:</span>
              <button
                onClick={() => setLicenseFilter('all')}
                className={`px-2.5 py-1 rounded-lg text-xs font-semibold ${
                  licenseFilter === 'all' ? 'bg-indigo-600 text-white' : 'text-slate-600 hover:text-slate-900'
                }`}
              >
                All
              </button>
              <button
                onClick={() => setLicenseFilter('yes')}
                className={`px-2.5 py-1 rounded-lg text-xs font-semibold ${
                  licenseFilter === 'yes' ? 'bg-emerald-600 text-white' : 'text-slate-600 hover:text-slate-900'
                }`}
              >
                Commercial Safe
              </button>
              <button
                onClick={() => setLicenseFilter('plan_dependent')}
                className={`px-2.5 py-1 rounded-lg text-xs font-semibold ${
                  licenseFilter === 'plan_dependent' ? 'bg-amber-600 text-white' : 'text-slate-600 hover:text-slate-900'
                }`}
              >
                Plan Dependent
              </button>
            </div>

            {(selectedCategory !== 'all' || selectedArchetype !== 'all' || licenseFilter !== 'all' || search) && (
              <button
                onClick={() => {
                  setSelectedCategory('all');
                  setSelectedArchetype('all');
                  setLicenseFilter('all');
                  setSearch('');
                }}
                className="text-xs text-rose-600 hover:underline font-bold px-2 py-1"
              >
                Reset Filters
              </button>
            )}

            <div className="text-xs text-slate-500 font-semibold px-2">
              Showing <strong>{filteredTools.length}</strong> tools
            </div>
          </div>

        </div>

        {/* 18 Category Chips (Horizontal Scrollable) */}
        <div className="border-t border-slate-100 pt-4">
          <div className="text-[11px] font-bold text-slate-400 uppercase tracking-wider mb-2 flex items-center gap-1.5">
            <Filter className="w-3.5 h-3.5" />
            Filter by 18 Creator Disciplines
          </div>
          <div className="flex items-center gap-2 overflow-x-auto pb-2 custom-scrollbar">
            <button
              onClick={() => setSelectedCategory('all')}
              className={`px-3 py-1.5 rounded-xl text-xs font-bold shrink-0 transition-all ${
                selectedCategory === 'all'
                  ? 'bg-slate-900 text-white shadow-xs'
                  : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
              }`}
            >
              All Categories ({tools.length})
            </button>
            {categories.map((cat) => (
              <button
                key={cat.id}
                onClick={() => setSelectedCategory(cat.id)}
                className={`px-3 py-1.5 rounded-xl text-xs font-bold shrink-0 transition-all flex items-center gap-1.5 ${
                  selectedCategory === cat.id
                    ? 'bg-indigo-600 text-white shadow-xs'
                    : 'bg-slate-100 text-slate-700 hover:bg-slate-200 border border-slate-200/60'
                }`}
              >
                <span>{cat.emoji || '⚡'}</span>
                <span>{cat.name}</span>
                <span className={`text-[10px] px-1 rounded ${selectedCategory === cat.id ? 'bg-indigo-700 text-white' : 'bg-slate-200 text-slate-600'}`}>
                  {cat.count || 20}
                </span>
              </button>
            ))}
          </div>
        </div>

      </section>

      {/* 4. Tool Catalog Cards Grid */}
      <section className="space-y-4">
        
        <div className="flex items-center justify-between">
          <h2 className="text-lg font-extrabold text-slate-900">
            {selectedCategory === 'all' ? 'All AI Tools' : categories.find(c => c.id === selectedCategory)?.name || 'Filtered Tools'}
            <span className="text-xs font-normal text-slate-500 ml-2">({filteredTools.length} results)</span>
          </h2>
        </div>

        {filteredTools.length === 0 ? (
          <div className="bg-white rounded-3xl p-12 text-center border border-slate-200 space-y-4">
            <AlertTriangle className="w-10 h-10 text-amber-500 mx-auto" />
            <h3 className="text-lg font-bold text-slate-800">No AI Tools match your active filters</h3>
            <p className="text-xs text-slate-500 max-w-md mx-auto">
              Try adjusting your search keyword or clearing the category and licence filters.
            </p>
            <button
              onClick={() => {
                setSelectedCategory('all');
                setSelectedArchetype('all');
                setLicenseFilter('all');
                setSearch('');
              }}
              className="px-4 py-2 bg-indigo-600 text-white rounded-xl text-xs font-bold"
            >
              Reset All Filters
            </button>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
            {filteredTools.map((tool, idx) => {
              const isCommercialSafe = tool.commercial_use === 'yes';
              return (
                <div
                  key={`${tool.name}-${idx}`}
                  className="bg-white rounded-2xl p-5 border border-slate-200 hover:border-indigo-300 hover:shadow-md transition-all flex flex-col justify-between group"
                >
                  <div className="space-y-2.5">
                    
                    {/* Header: Name + External Link */}
                    <div className="flex items-start justify-between gap-2">
                      <h3 className="font-extrabold text-slate-900 text-base group-hover:text-indigo-600 transition-colors flex items-center gap-1.5">
                        {tool.name}
                      </h3>
                      {tool.url && (
                        <a
                          href={tool.url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="text-slate-400 hover:text-indigo-600 p-1 hover:bg-slate-100 rounded-lg transition-colors shrink-0"
                          title="Visit official website"
                        >
                          <ExternalLink className="w-3.5 h-3.5" />
                        </a>
                      )}
                    </div>

                    {/* Badges: Category + Commercial Clearance */}
                    <div className="flex items-center gap-1.5 flex-wrap">
                      <span className="text-[10px] font-bold px-2 py-0.5 rounded-md bg-indigo-50 text-indigo-700 border border-indigo-100">
                        {tool.category_name || tool.category}
                      </span>

                      {isCommercialSafe ? (
                        <span className="text-[10px] font-semibold px-2 py-0.5 rounded-md bg-emerald-50 text-emerald-700 border border-emerald-200 flex items-center gap-1" title="Commercially cleared for full commercial buyout campaigns">
                          <ShieldCheck className="w-3 h-3 text-emerald-600" />
                          Commercial Safe
                        </span>
                      ) : (
                        <span className="text-[10px] font-semibold px-2 py-0.5 rounded-md bg-amber-50 text-amber-700 border border-amber-200 flex items-center gap-1" title="Plan-dependent commercial rights: verify creator's active plan subscription">
                          <AlertTriangle className="w-3 h-3 text-amber-600" />
                          Plan Dependent
                        </span>
                      )}
                    </div>

                    {/* Description */}
                    <p className="text-xs text-slate-600 leading-relaxed line-clamp-3">
                      {tool.description || 'Essential tool in generative workflows for AI creators and modern brands.'}
                    </p>

                    {/* Popular Archetype */}
                    {tool.popular_archetype && (
                      <div className="text-[10px] text-slate-500 font-medium flex items-center gap-1 pt-1">
                        <span className="text-slate-400">Featured in:</span>
                        <span className="font-semibold text-slate-700">{tool.popular_archetype}</span>
                      </div>
                    )}
                  </div>

                  {/* Actions */}
                  <div className="mt-4 pt-3 border-t border-slate-100 flex items-center gap-2">
                    <button
                      onClick={() => handleFindCreators(tool.name)}
                      className="w-full py-2 px-3 rounded-xl bg-slate-900 hover:bg-indigo-600 text-white font-bold text-xs flex items-center justify-center gap-1.5 transition-colors shadow-xs"
                    >
                      <Users className="w-3.5 h-3.5" />
                      Find Creators
                    </button>
                    {tool.url && (
                      <a
                        href={tool.url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="p-2 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-600 transition-colors"
                        title="Open Official Website"
                      >
                        <Globe className="w-3.5 h-3.5" />
                      </a>
                    )}
                  </div>

                </div>
              );
            })}
          </div>
        )}

      </section>

      {/* 5. Creator Marketplace Ecosystem & Industry Benchmarks */}
      <section className="bg-gradient-to-br from-slate-900 to-indigo-950 rounded-3xl p-8 sm:p-10 text-white space-y-8 border border-slate-800">
        <div>
          <span className="text-xs font-bold uppercase tracking-wider text-indigo-400">Industry Sources & Integrations</span>
          <h2 className="text-2xl sm:text-3xl font-black tracking-tight mt-1">
            Connected to Leading Influencer & Creator Platforms
          </h2>
          <p className="text-xs sm:text-sm text-slate-300 max-w-2xl mt-1 leading-relaxed">
            GenCraft & Kampus.VC bridge the gap between creative execution and global marketplace discovery. We benchmark against top platforms to verify rates, authenticity, and licensing clearance.
          </p>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-3.5">
          {platforms.map((plat) => (
            <div key={plat.name} className="bg-white/5 border border-white/10 rounded-2xl p-4 hover:bg-white/10 transition-all flex flex-col justify-between">
              <div>
                <div className="flex items-center justify-between mb-2">
                  <h3 className="font-bold text-sm text-white">{plat.name}</h3>
                  <a
                    href={plat.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-slate-400 hover:text-white"
                  >
                    <ExternalLink className="w-3.5 h-3.5" />
                  </a>
                </div>
                <span className="inline-block text-[9px] font-bold px-2 py-0.5 rounded bg-indigo-500/20 text-indigo-300 border border-indigo-400/30 mb-2">
                  {plat.badge}
                </span>
                <p className="text-[11px] text-slate-300 leading-relaxed line-clamp-3">
                  {plat.description}
                </p>
              </div>

              <a
                href={plat.url}
                target="_blank"
                rel="noopener noreferrer"
                className="mt-3 text-[11px] font-bold text-indigo-300 hover:text-white flex items-center gap-1"
              >
                Visit Platform <ArrowRight className="w-3 h-3" />
              </a>
            </div>
          ))}
        </div>
      </section>

    </div>
  );
}
