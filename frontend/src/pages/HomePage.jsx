import React from 'react';
import { Link } from 'react-router-dom';
import { Sparkles, ArrowRight, Zap, Target, Cpu } from 'lucide-react';

export function HomePage() {
  return (
    <div className="flex flex-col min-h-screen">

      {/* Hero Section */}
      <section className="relative overflow-hidden pt-16 pb-24 px-4 sm:px-6 lg:px-8">
        <div className="absolute top-1/4 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-gradient-to-tr from-indigo-200/50 via-purple-200/40 to-pink-200/30 rounded-full blur-3xl pointer-events-none -z-10" />

        <div className="max-w-5xl mx-auto text-center">
          <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-indigo-100 border border-indigo-200 text-indigo-700 text-xs font-semibold mb-6 shadow-xs">
            <Sparkles className="w-4 h-4 text-indigo-600" />
            Next-Gen AI Content Production Platform
          </div>

          <h1 className="text-4xl sm:text-6xl font-extrabold text-slate-900 tracking-tight leading-tight mb-6">
            Hire Top <span className="gradient-text">Generative AI Creators</span> & Animators
          </h1>

          <p className="text-lg sm:text-xl text-slate-600 max-w-3xl mx-auto mb-10 leading-relaxed font-normal">
            Connect your brand with elite AI filmmakers, 3D generative artists, and video prompt engineers. Complete commercial clearance, verified tool stacks, and intelligent brief matching.
          </p>

          <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
            <Link
              to="/creators"
              className="w-full sm:w-auto px-8 py-3.5 rounded-2xl bg-indigo-600 hover:bg-indigo-500 text-white font-bold text-base shadow-lg shadow-indigo-600/25 flex items-center justify-center gap-2.5 transition-all hover:scale-105"
            >
              Find AI Creators
              <ArrowRight className="w-5 h-5" />
            </Link>

            <Link
              to="/briefs/new"
              className="w-full sm:w-auto px-8 py-3.5 rounded-2xl bg-white hover:bg-slate-50 text-slate-800 font-bold text-base border border-slate-200 shadow-sm flex items-center justify-center gap-2.5 transition-all"
            >
              <Zap className="w-5 h-5 text-purple-600" />
              Build AI Brief
            </Link>
          </div>
        </div>
      </section>

      {/* Stats Counter Bar */}
      <section className="border-y border-slate-200 bg-white py-8 px-4">
        <div className="max-w-6xl mx-auto grid grid-cols-2 md:grid-cols-4 gap-8 text-center">
          <div>
            <div className="text-3xl font-extrabold text-indigo-600">26+</div>
            <div className="text-xs text-slate-500 font-semibold uppercase mt-1">Verified AI Creators</div>
          </div>
          <div>
            <div className="text-3xl font-extrabold text-indigo-600">100+</div>
            <div className="text-xs text-slate-500 font-semibold uppercase mt-1">Portfolio Items</div>
          </div>
          <div>
            <div className="text-3xl font-extrabold text-indigo-600">250+</div>
            <div className="text-xs text-slate-500 font-semibold uppercase mt-1">AI Tools Tracked (18 Categories)</div>
          </div>
          <div>
            <div className="text-3xl font-extrabold text-indigo-600">100%</div>
            <div className="text-xs text-slate-500 font-semibold uppercase mt-1">Commercial Clearance</div>
          </div>
        </div>
      </section>

      {/* AI Tools & Kampus.VC Archetypes Showcase */}
      <section className="py-16 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
        <div className="bg-gradient-to-br from-indigo-900 via-slate-900 to-purple-950 rounded-3xl p-8 sm:p-12 text-white relative overflow-hidden shadow-xl border border-indigo-500/20">
          <div className="absolute top-0 right-0 w-96 h-96 bg-indigo-500/10 rounded-full blur-3xl pointer-events-none" />

          <div className="max-w-3xl mb-10">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white/10 text-indigo-300 text-xs font-semibold mb-4 backdrop-blur-xs border border-white/10">
              <Sparkles className="w-3.5 h-3.5" />
              Comprehensive AI Creator Toolkit • Kampus.VC Research
            </div>
            <h2 className="text-3xl sm:text-4xl font-extrabold tracking-tight mb-4 text-white">
              Discover 250+ AI Tools across 18 Creator Disciplines
            </h2>
            <p className="text-slate-300 text-sm sm:text-base leading-relaxed">
              Explore generative video suites, neural voice cloners, AI avatar studios, and automated repurposing tools. Built for brand marketers and creative directors sourcing specialists on Kampus.VC.
            </p>
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-3.5 mb-8">
            {[
              { name: 'AI Video Creator', icon: '🎬', tools: 'Runway, Kling, Veo, Pika' },
              { name: 'AI Graphic Designer', icon: '🎨', tools: 'Midjourney, Ideogram, Canva' },
              { name: 'AI Script Writer', icon: '✍️', tools: 'ChatGPT, Claude, Jasper' },
              { name: 'AI Voice Artist', icon: '🎙️', tools: 'ElevenLabs, Murf, PlayHT' },
              { name: 'AI Music Producer', icon: '🎵', tools: 'Suno, Udio, AIVA' },
              { name: 'AI Influencer Creator', icon: '🤖', tools: 'HeyGen, Hedra, Synthesia' },
              { name: 'UGC Ad Creator', icon: '📣', tools: 'Creatify, Arcads, JoggAI' },
              { name: 'Social Media Manager', icon: '📱', tools: 'Buffer, Predis.ai, Metricool' },
              { name: 'AI Repurposing Expert', icon: '♻️', tools: 'CapCut, Descript, OpusClip' },
              { name: 'AI Marketing Strategist', icon: '📈', tools: 'Semrush, Surfer, BuzzSumo' }
            ].map(arch => (
              <Link
                key={arch.name}
                to={`/creators?specialization=${encodeURIComponent(arch.name)}`}
                className="p-3.5 rounded-2xl bg-white/5 hover:bg-white/10 border border-white/10 transition-all hover:scale-102 flex flex-col justify-between group"
              >
                <div>
                  <div className="text-2xl mb-1.5">{arch.icon}</div>
                  <div className="text-xs font-bold text-white group-hover:text-indigo-300 transition-colors">{arch.name}</div>
                </div>
                <div className="text-[10px] text-slate-400 mt-2 line-clamp-1">{arch.tools}</div>
              </Link>
            ))}
          </div>

          <div className="flex flex-col sm:flex-row items-center justify-between gap-4 pt-4 border-t border-white/10">
            <div className="text-xs text-slate-400">
              Benchmark standards aligned with <span className="text-slate-200">Buffer</span>, <span className="text-slate-200">VEED.io</span>, <span className="text-slate-200">Collabstr</span>, <span className="text-slate-200">CreatorIQ</span> & <span className="text-slate-200">Upfluence</span>.
            </div>
            <Link
              to="/tools"
              className="px-6 py-2.5 rounded-xl bg-indigo-500 hover:bg-indigo-400 text-white font-bold text-xs flex items-center gap-2 transition-all shadow-md shrink-0"
            >
              Explore 250+ Tools Directory
              <ArrowRight className="w-4 h-4" />
            </Link>
          </div>
        </div>
      </section>

      {/* Value Proposition Cards */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
        <div className="text-center mb-16">
          <h2 className="text-3xl font-bold text-slate-900 mb-3">Built for Modern Creative Pipelines</h2>
          <p className="text-slate-600 text-sm max-w-xl mx-auto">
            Eliminate friction when sourcing generative video, AI music, character animation, and photoreal product renders.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">

          <div className="glass-card p-6 rounded-3xl">
            <div className="w-12 h-12 rounded-2xl bg-indigo-50 border border-indigo-200 flex items-center justify-center mb-5 text-indigo-600">
              <Cpu className="w-6 h-6" />
            </div>
            <h3 className="text-lg font-bold text-slate-900 mb-2">Verified AI Tool Stacks</h3>
            <p className="text-xs text-slate-600 leading-relaxed">
              Every creator's toolset (Midjourney, Runway, Sora, ComfyUI, ElevenLabs, Kling) is documented with full process notes and commercial licence status.
            </p>
          </div>

          <div className="glass-card p-6 rounded-3xl">
            <div className="w-12 h-12 rounded-2xl bg-purple-50 border border-purple-200 flex items-center justify-center mb-5 text-purple-600">
              <Target className="w-6 h-6" />
            </div>
            <h3 className="text-lg font-bold text-slate-900 mb-2">Automated Match Scoring</h3>
            <p className="text-xs text-slate-600 leading-relaxed">
              Our 0-100 match algorithm evaluates tool overlap across 250+ tools, skill requirements, budget alignment, and verification signals for every campaign brief.
            </p>
          </div>

          <div className="glass-card p-6 rounded-3xl">
            <div className="w-12 h-12 rounded-2xl bg-pink-50 border border-pink-200 flex items-center justify-center mb-5 text-pink-600">
              <Sparkles className="w-6 h-6" />
            </div>
            <h3 className="text-lg font-bold text-slate-900 mb-2">Gemini AI Brief Builder</h3>
            <p className="text-xs text-slate-600 leading-relaxed">
              Turn a rough sentence into a production-ready brief prefilled with aspect ratios, commercial buyout options, required tools, and budget bounds.
            </p>
          </div>

        </div>
      </section>

    </div>
  );
}
