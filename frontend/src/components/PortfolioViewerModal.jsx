import React from 'react';
import { X, Play, Clock, Monitor, Cpu, User, FileText, Workflow } from 'lucide-react';

export function PortfolioViewerModal({ item, onClose }) {
  if (!item) return null;

  const commStatusStyles = {
    cleared: 'bg-emerald-50 text-emerald-700 border-emerald-200',
    pending: 'bg-amber-50 text-amber-700 border-amber-200',
    personal_only: 'bg-rose-50 text-rose-700 border-rose-200'
  };

  const commLabels = {
    cleared: 'Commercial Use Cleared',
    pending: 'Commercial Clearance Pending',
    personal_only: 'Personal / Non-Commercial Only'
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/40 backdrop-blur-sm animate-fade-in">
      <div 
        className="relative w-full max-w-4xl max-h-[90vh] overflow-y-auto bg-white rounded-3xl border border-slate-200 shadow-2xl p-6 sm:p-8 text-slate-900"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Close Button */}
        <button
          onClick={onClose}
          className="absolute top-5 right-5 p-2 rounded-full bg-slate-100 hover:bg-slate-200 text-slate-600 hover:text-slate-900 transition-colors"
        >
          <X className="w-5 h-5" />
        </button>

        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
          
          {/* Left: Media Preview */}
          <div className="lg:col-span-7 flex flex-col gap-4">
            <div className="relative rounded-2xl overflow-hidden bg-slate-100 border border-slate-200 shadow-inner group flex items-center justify-center min-h-[300px]">
              <img
                src={item.thumbnail_url || 'https://picsum.photos/seed/portfolio/800/450'}
                alt={item.title}
                className="w-full h-auto max-h-[450px] object-contain"
              />
              {item.media_type === 'video' && (
                <div className="absolute inset-0 bg-slate-900/30 flex items-center justify-center">
                  <div className="w-16 h-16 rounded-full bg-indigo-600 text-white flex items-center justify-center shadow-lg transform group-hover:scale-110 transition-transform">
                    <Play className="w-8 h-8 fill-current translate-x-0.5" />
                  </div>
                </div>
              )}
            </div>

            {/* Media Metadata Pills */}
            <div className="flex flex-wrap items-center gap-2 text-xs">
              <span className="px-3 py-1 rounded-lg bg-indigo-50 text-indigo-700 border border-indigo-200 font-semibold uppercase">
                {item.media_type}
              </span>
              {item.aspect_ratio && (
                <span className="px-3 py-1 rounded-lg bg-slate-100 text-slate-700 border border-slate-200 flex items-center gap-1 font-medium">
                  <Monitor className="w-3.5 h-3.5 text-slate-500" />
                  {item.aspect_ratio}
                </span>
              )}
              {item.duration_sec && (
                <span className="px-3 py-1 rounded-lg bg-slate-100 text-slate-700 border border-slate-200 flex items-center gap-1 font-medium">
                  <Clock className="w-3.5 h-3.5 text-slate-500" />
                  {item.duration_sec} sec
                </span>
              )}
              {item.year && (
                <span className="px-3 py-1 rounded-lg bg-slate-100 text-slate-600 border border-slate-200">
                  {item.year}
                </span>
              )}
            </div>
          </div>

          {/* Right: Item Details & AI Workflow Breakdown */}
          <div className="lg:col-span-5 flex flex-col justify-between">
            <div>
              <div className="flex items-center gap-2 mb-2">
                <span className={`px-2.5 py-1 rounded-full text-xs font-semibold border ${commStatusStyles[item.commercial_use]}`}>
                  {commLabels[item.commercial_use]}
                </span>
              </div>

              <h2 className="text-2xl font-bold text-slate-900 mb-2">{item.title}</h2>

              {item.client_name && (
                <div className="text-xs text-slate-500 flex items-center gap-1.5 mb-4">
                  <User className="w-3.5 h-3.5 text-indigo-600" />
                  <span>Client / Brand: <strong className="text-slate-800">{item.client_name}</strong></span>
                </div>
              )}

              {/* Tools Used */}
              {item.tools && item.tools.length > 0 && (
                <div className="mb-5">
                  <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider block mb-2 flex items-center gap-1.5">
                    <Cpu className="w-4 h-4 text-indigo-600" />
                    Tools Utilized
                  </span>
                  <div className="flex flex-wrap gap-1.5">
                    {item.tools.map(t => (
                      <span key={t.id} className="px-2.5 py-1 rounded-lg text-xs font-medium bg-slate-100 text-indigo-700 border border-slate-200">
                        {t.name}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              {/* Workflow Pipeline */}
              {item.workflow && (
                <div className="mb-5 bg-purple-50/60 border border-purple-100 rounded-xl p-3.5">
                  <span className="text-xs font-semibold text-purple-900 uppercase tracking-wider block mb-1.5 flex items-center gap-1.5">
                    <Workflow className="w-4 h-4 text-purple-600" />
                    AI Workflow Pipeline
                  </span>
                  <p className="text-xs font-mono text-purple-800 bg-white p-2 rounded-lg border border-purple-200">
                    {item.workflow}
                  </p>
                </div>
              )}

              {/* Process Notes */}
              {item.process_notes && (
                <div className="mb-5">
                  <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider block mb-1.5 flex items-center gap-1.5">
                    <FileText className="w-4 h-4 text-indigo-600" />
                    Creative Process Notes
                  </span>
                  <p className="text-xs text-slate-700 leading-relaxed bg-slate-50 p-3 rounded-xl border border-slate-200">
                    {item.process_notes}
                  </p>
                </div>
              )}
            </div>

            <div className="pt-4 border-t border-slate-200 flex justify-end">
              <button
                onClick={onClose}
                className="px-5 py-2 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-800 text-xs font-semibold transition-colors"
              >
                Close Viewer
              </button>
            </div>

          </div>

        </div>
      </div>
    </div>
  );
}
