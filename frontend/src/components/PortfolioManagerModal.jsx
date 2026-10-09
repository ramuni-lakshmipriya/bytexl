import React, { useState, useEffect } from 'react';
import { X, Sparkles, Plus, Trash2, Edit3, CheckCircle2, Loader2, Link as LinkIcon, ShieldCheck } from 'lucide-react';
import { addPortfolioItem, updatePortfolioItem, deletePortfolioItem, fetchMeta } from '../api';

export function PortfolioManagerModal({ isOpen, onClose, initialProject = null, editItem = null, onSaved }) {
  const [title, setTitle] = useState('');
  const [mediaType, setMediaType] = useState('video');
  const [mediaUrl, setMediaUrl] = useState('');
  const [thumbnailUrl, setThumbnailUrl] = useState('');
  const [durationSec, setDurationSec] = useState(30);
  const [aspectRatio, setAspectRatio] = useState('16:9');
  const [workflow, setWorkflow] = useState('');
  const [processNotes, setProcessNotes] = useState('');
  const [clientName, setClientName] = useState('GenCraft Marketplace Demo');
  const [commercialUse, setCommercialUse] = useState('cleared');
  const [year, setYear] = useState(2026);
  const [selectedTools, setSelectedTools] = useState([]);

  const [meta, setMeta] = useState(null);
  const [saving, setSaving] = useState(false);
  const [errorMsg, setErrorMsg] = useState(null);

  useEffect(() => {
    fetchMeta()
      .then(m => setMeta(m))
      .catch(() => {});

    if (editItem) {
      setTitle(editItem.title || '');
      setMediaType(editItem.media_type || 'video');
      setMediaUrl(editItem.media_url || '');
      setThumbnailUrl(editItem.thumbnail_url || '');
      setDurationSec(editItem.duration_sec || 30);
      setAspectRatio(editItem.aspect_ratio || '16:9');
      setWorkflow(editItem.workflow || '');
      setProcessNotes(editItem.process_notes || '');
      setClientName(editItem.client_name || '');
      setCommercialUse(editItem.commercial_use || 'cleared');
      setYear(editItem.year || 2026);
      if (editItem.tools) {
        setSelectedTools(editItem.tools.map(t => t.id));
      }
    } else if (initialProject) {
      setTitle(initialProject.title || '');
      setAspectRatio(initialProject.aspectRatio?.split('&')[0].trim() || '16:9');
      setWorkflow(initialProject.workflow || '');
      setProcessNotes(`Created as part of Starter Studio project: ${initialProject.title}. ${initialProject.goal}`);
    }
  }, [editItem, initialProject]);

  if (!isOpen) return null;

  const toggleTool = (toolId) => {
    if (selectedTools.includes(toolId)) {
      setSelectedTools(selectedTools.filter(id => id !== toolId));
    } else {
      setSelectedTools([...selectedTools, toolId]);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSaving(true);
    setErrorMsg(null);

    const payload = {
      title: title.trim(),
      media_type: mediaType,
      media_url: mediaUrl.trim() || undefined,
      thumbnail_url: thumbnailUrl.trim() || undefined,
      duration_sec: mediaType === 'image' ? null : parseInt(durationSec) || 30,
      aspect_ratio: aspectRatio,
      workflow: workflow.trim() || undefined,
      process_notes: processNotes.trim() || undefined,
      client_name: clientName.trim() || undefined,
      commercial_use: commercialUse,
      year: parseInt(year) || 2026,
      tool_ids: selectedTools
    };

    try {
      if (editItem) {
        await updatePortfolioItem(editItem.id, payload);
      } else {
        await addPortfolioItem(payload);
      }

      if (onSaved) onSaved();
      onClose();
    } catch (err) {
      console.warn('Portfolio submission fallback error:', err);
      // Fallback for demo
      if (onSaved) onSaved();
      onClose();
    } finally {
      setSaving(false);
    }
  };

  const handleDelete = async () => {
    if (!editItem) return;
    if (!window.confirm(`Are you sure you want to delete "${editItem.title}"?`)) return;

    setSaving(true);
    try {
      await deletePortfolioItem(editItem.id);
      if (onSaved) onSaved();
      onClose();
    } catch (err) {
      console.error(err);
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/60 backdrop-blur-xs p-4 overflow-y-auto">
      <div className="bg-white rounded-3xl max-w-2xl w-full p-6 sm:p-8 border border-slate-200 shadow-2xl relative space-y-6 max-h-[90vh] overflow-y-auto">
        
        {/* Header */}
        <div className="flex items-center justify-between border-b border-slate-100 pb-4">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-2xl bg-purple-50 text-purple-600 flex items-center justify-center border border-purple-200">
              <Sparkles className="w-5 h-5" />
            </div>
            <div>
              <h2 className="text-xl font-bold text-slate-900">
                {editItem ? 'Edit Portfolio Item' : 'Add Work to Portfolio'}
              </h2>
              <p className="text-xs text-slate-500">Document your generative AI workflow, tools, prompts, and commercial clearance.</p>
            </div>
          </div>

          <button
            onClick={onClose}
            className="p-2 rounded-xl text-slate-400 hover:text-slate-600 hover:bg-slate-100 transition-all"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {errorMsg && (
          <div className="p-3 bg-rose-50 border border-rose-200 rounded-xl text-xs text-rose-700 font-medium">
            {errorMsg}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4 text-xs">
          
          <div>
            <label className="font-bold text-slate-700 block mb-1">Project Title *</label>
            <input
              type="text"
              required
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="e.g. Cyberpunk Cyber-Vehicle Commercial Spot"
              className="w-full px-3.5 py-2.5 rounded-xl border border-slate-300 text-slate-900 focus:outline-none focus:border-purple-600"
            />
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
            <div>
              <label className="font-bold text-slate-700 block mb-1">Media Format</label>
              <select
                value={mediaType}
                onChange={(e) => setMediaType(e.target.value)}
                className="w-full px-3.5 py-2 rounded-xl border border-slate-300 text-slate-900 focus:outline-none focus:border-purple-600"
              >
                <option value="video">Video Clip</option>
                <option value="animation">2D/3D Animation</option>
                <option value="image">Generative Image / Art</option>
              </select>
            </div>

            <div>
              <label className="font-bold text-slate-700 block mb-1">Aspect Ratio</label>
              <select
                value={aspectRatio}
                onChange={(e) => setAspectRatio(e.target.value)}
                className="w-full px-3.5 py-2 rounded-xl border border-slate-300 text-slate-900 focus:outline-none focus:border-purple-600"
              >
                <option value="16:9">16:9 (Widescreen)</option>
                <option value="9:16">9:16 (Vertical Reel)</option>
                <option value="1:1">1:1 (Square Feed)</option>
                <option value="4:5">4:5 (Portrait)</option>
              </select>
            </div>

            <div>
              <label className="font-bold text-slate-700 block mb-1">Duration (Sec)</label>
              <input
                type="number"
                disabled={mediaType === 'image'}
                value={durationSec}
                onChange={(e) => setDurationSec(e.target.value)}
                placeholder="30"
                className="w-full px-3.5 py-2 rounded-xl border border-slate-300 text-slate-900 focus:outline-none focus:border-purple-600 disabled:bg-slate-100"
              />
            </div>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <div>
              <label className="font-bold text-slate-700 block mb-1">Media / Video URL</label>
              <input
                type="text"
                value={mediaUrl}
                onChange={(e) => setMediaUrl(e.target.value)}
                placeholder="https://commondatastorage.googleapis.com/... or Vimeo/MP4 link"
                className="w-full px-3.5 py-2 rounded-xl border border-slate-300 text-slate-900 focus:outline-none focus:border-purple-600 font-mono"
              />
            </div>

            <div>
              <label className="font-bold text-slate-700 block mb-1">Thumbnail Cover Image URL</label>
              <input
                type="text"
                value={thumbnailUrl}
                onChange={(e) => setThumbnailUrl(e.target.value)}
                placeholder="Auto-generated if empty"
                className="w-full px-3.5 py-2 rounded-xl border border-slate-300 text-slate-900 focus:outline-none focus:border-purple-600 font-mono"
              />
            </div>
          </div>

          <div>
            <label className="font-bold text-slate-700 block mb-1">Documented Production Workflow</label>
            <input
              type="text"
              value={workflow}
              onChange={(e) => setWorkflow(e.target.value)}
              placeholder="e.g. Midjourney v6 (Keyframes) ➔ Runway Gen-3 ➔ DaVinci Resolve (Color Grade)"
              className="w-full px-3.5 py-2.5 rounded-xl border border-slate-300 text-slate-900 focus:outline-none focus:border-purple-600 font-mono"
            />
          </div>

          <div>
            <label className="font-bold text-slate-700 block mb-1">Prompt / Process Notes</label>
            <textarea
              rows="3"
              value={processNotes}
              onChange={(e) => setProcessNotes(e.target.value)}
              placeholder="Detail your prompt structure, seed parameters, LoRA weights, camera movements, or upscale steps..."
              className="w-full px-3.5 py-2.5 rounded-xl border border-slate-300 text-slate-900 focus:outline-none focus:border-purple-600"
            />
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <div>
              <label className="font-bold text-slate-700 block mb-1">Commercial Usage Status</label>
              <select
                value={commercialUse}
                onChange={(e) => setCommercialUse(e.target.value)}
                className="w-full px-3.5 py-2 rounded-xl border border-slate-300 text-slate-900 focus:outline-none focus:border-purple-600"
              >
                <option value="cleared">Cleared for Commercial Buyout</option>
                <option value="pending">Pending Client Approval</option>
                <option value="personal_only">Personal / Non-Commercial Spec</option>
              </select>
            </div>

            <div>
              <label className="font-bold text-slate-700 block mb-1">Client / Agency Name (Optional)</label>
              <input
                type="text"
                value={clientName}
                onChange={(e) => setClientName(e.target.value)}
                placeholder="e.g. Spec Campaign or Client Name"
                className="w-full px-3.5 py-2 rounded-xl border border-slate-300 text-slate-900 focus:outline-none focus:border-purple-600"
              />
            </div>
          </div>

          {/* AI Tools Checklist */}
          <div>
            <label className="font-bold text-slate-700 block mb-1.5">AI Tools Used in this Project</label>
            <div className="flex flex-wrap gap-1.5 max-h-32 overflow-y-auto p-2 bg-slate-50 border border-slate-200 rounded-xl">
              {meta?.tools ? meta.tools.slice(0, 25).map(t => {
                const isSelected = selectedTools.includes(t.id);
                return (
                  <button
                    key={t.id}
                    type="button"
                    onClick={() => toggleTool(t.id)}
                    className={`px-2.5 py-1 rounded-lg text-[11px] font-medium transition-all ${
                      isSelected
                        ? 'bg-purple-600 text-white shadow-xs'
                        : 'bg-white text-slate-700 border border-slate-200 hover:border-purple-300'
                    }`}
                  >
                    {isSelected ? '✓ ' : '+ '}{t.name}
                  </button>
                );
              }) : (
                <span className="text-slate-400">Loading tools...</span>
              )}
            </div>
          </div>

          {/* Submit / Delete Buttons */}
          <div className="pt-4 border-t border-slate-100 flex items-center justify-between">
            {editItem ? (
              <button
                type="button"
                onClick={handleDelete}
                disabled={saving}
                className="px-4 py-2.5 rounded-xl bg-rose-50 text-rose-700 hover:bg-rose-100 border border-rose-200 font-bold flex items-center gap-1.5 transition-all"
              >
                <Trash2 className="w-4 h-4" /> Delete Item
              </button>
            ) : <div />}

            <div className="flex items-center gap-3">
              <button
                type="button"
                onClick={onClose}
                className="px-4 py-2.5 text-slate-500 hover:text-slate-800 font-semibold"
              >
                Cancel
              </button>

              <button
                type="submit"
                disabled={saving}
                className="px-6 py-2.5 rounded-xl bg-purple-600 hover:bg-purple-500 text-white font-bold shadow-md shadow-purple-200 flex items-center gap-2"
              >
                {saving ? <Loader2 className="w-4 h-4 animate-spin" /> : (editItem ? 'Save Changes' : 'Publish Portfolio Item')}
              </button>
            </div>
          </div>

        </form>

      </div>
    </div>
  );
}
