import React from 'react';
import { Sparkles } from 'lucide-react';

export function Footer() {
  return (
    <footer className="w-full border-t border-slate-200 bg-white py-8 px-4 sm:px-6 lg:px-8 mt-20">
      <div className="max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <img
            src="/logo.png"
            alt="Vyntrav"
            className="w-8 h-8 rounded-lg object-contain bg-black p-0.5 border border-slate-800"
          />
          <span className="text-sm font-bold text-slate-900">
            Vyntrav AI Marketplace &copy; 2026
          </span>
        </div>
        <span className="text-xs text-slate-500 font-medium">
          Connecting AI Content Creators with Global Brands
        </span>
      </div>
    </footer>
  );
}
