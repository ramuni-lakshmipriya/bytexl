import React, { useState } from 'react';
import { ShieldCheck, FileCode, ExternalLink } from 'lucide-react';

export function VerificationBadge({ type, size = 'md' }) {
  const [showTooltip, setShowTooltip] = useState(false);

  const configs = {
    tools: {
      icon: ShieldCheck,
      label: 'Tools Verified',
      color: 'text-indigo-700 bg-indigo-50 border-indigo-200',
      tooltip: 'Tools Verified: Creator active tool stack and licences have been verified by platform admins.'
    },
    workflow: {
      icon: FileCode,
      label: 'Workflow Documented',
      color: 'text-purple-700 bg-purple-50 border-purple-200',
      tooltip: 'Workflow Documented: Detailed step-by-step AI prompt & rendering process attached to portfolio work.'
    },
    past_work: {
      icon: ExternalLink,
      label: 'Past Work Linked',
      color: 'text-emerald-700 bg-emerald-50 border-emerald-200',
      tooltip: 'Past Work Linked: Creator has published commercial or live client campaigns linked to external sources.'
    }
  };

  const config = configs[type];
  if (!config) return null;

  const Icon = config.icon;

  const iconSizes = {
    sm: 'w-3.5 h-3.5',
    md: 'w-4 h-4',
    lg: 'w-5 h-5'
  };

  return (
    <div 
      className="relative inline-block"
      onMouseEnter={() => setShowTooltip(true)}
      onMouseLeave={() => setShowTooltip(false)}
    >
      <span className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold border ${config.color} transition-all cursor-help`}>
        <Icon className={iconSizes[size]} />
        <span>{config.label}</span>
      </span>

      {showTooltip && (
        <div className="absolute bottom-full mb-2 left-1/2 -translate-x-1/2 w-56 p-2.5 bg-slate-900 text-white text-xs rounded-lg shadow-xl z-50 pointer-events-none transition-opacity duration-150">
          {config.tooltip}
          <div className="absolute top-full left-1/2 -translate-x-1/2 border-4 border-transparent border-t-slate-900" />
        </div>
      )}
    </div>
  );
}
