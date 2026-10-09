import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Sparkles, CheckCircle2, ArrowRight, Loader2 } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { fetchCreatorById, fetchMeta } from '../api';

export function CompleteProfilePage() {
  const navigate = useNavigate();
  const { user } = useAuth();
  
  const [headline, setHeadline] = useState('');
  const [bio, setBio] = useState('');
  const [rateMin, setRateMin] = useState(15000);
  const [rateMax, setRateMax] = useState(45000);
  const [availability, setAvailability] = useState('available');

  const [saving, setSaving] = useState(false);

  useEffect(() => {
    if (user && user.creator_id) {
      fetchCreatorById(user.creator_id)
        .then(cr => {
          if (cr.headline) setHeadline(cr.headline);
          if (cr.bio) setBio(cr.bio);
          if (cr.rate_min_inr) setRateMin(cr.rate_min_inr);
          if (cr.rate_max_inr) setRateMax(cr.rate_max_inr);
          if (cr.availability) setAvailability(cr.availability);
        })
        .catch(() => {});
    }
  }, [user]);

  const handleSubmit = (e) => {
    e.preventDefault();
    setSaving(true);
    setTimeout(() => {
      setSaving(false);
      navigate('/dashboard');
    }, 600);
  };

  return (
    <div className="max-w-2xl mx-auto px-4 py-12">
      <div className="bg-white rounded-3xl p-8 border border-slate-200 shadow-xs space-y-6">
        
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-2xl bg-purple-50 border border-purple-200 text-purple-600 flex items-center justify-center">
            <Sparkles className="w-5 h-5" />
          </div>
          <div>
            <h1 className="text-2xl font-bold text-slate-900">Complete Your Creator Profile</h1>
            <p className="text-xs text-slate-500">Refine your bio, rate range, and availability to start receiving brief matches.</p>
          </div>
        </div>

        <form onSubmit={handleSubmit} className="space-y-5">
          
          <div>
            <label className="text-xs font-bold text-slate-700 block mb-1">Headline</label>
            <input
              type="text"
              value={headline}
              onChange={(e) => setHeadline(e.target.value)}
              placeholder="e.g. Short films and ad spots with cinematic AI pipelines"
              className="w-full px-3.5 py-2.5 rounded-xl bg-white border border-slate-300 text-slate-900 text-xs focus:outline-none focus:border-purple-600"
            />
          </div>

          <div>
            <label className="text-xs font-bold text-slate-700 block mb-1">Bio / Creative Vision</label>
            <textarea
              rows="4"
              value={bio}
              onChange={(e) => setBio(e.target.value)}
              placeholder="Describe your creative experience, workflow, and visual style..."
              className="w-full px-3.5 py-2.5 rounded-xl bg-white border border-slate-300 text-slate-900 text-xs focus:outline-none focus:border-purple-600"
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="text-xs font-bold text-slate-700 block mb-1">Min Rate (INR)</label>
              <input
                type="number"
                value={rateMin}
                onChange={(e) => setRateMin(parseInt(e.target.value) || 0)}
                className="w-full px-3.5 py-2 rounded-xl bg-white border border-slate-300 text-slate-900 text-xs focus:outline-none focus:border-purple-600"
              />
            </div>

            <div>
              <label className="text-xs font-bold text-slate-700 block mb-1">Max Rate (INR)</label>
              <input
                type="number"
                value={rateMax}
                onChange={(e) => setRateMax(parseInt(e.target.value) || 0)}
                className="w-full px-3.5 py-2 rounded-xl bg-white border border-slate-300 text-slate-900 text-xs focus:outline-none focus:border-purple-600"
              />
            </div>
          </div>

          <div>
            <label className="text-xs font-bold text-slate-700 block mb-1">Availability Status</label>
            <select
              value={availability}
              onChange={(e) => setAvailability(e.target.value)}
              className="w-full px-3.5 py-2 rounded-xl bg-white border border-slate-300 text-slate-900 text-xs focus:outline-none focus:border-purple-600"
            >
              <option value="available">Available for new briefs</option>
              <option value="busy">Currently busy</option>
            </select>
          </div>

          <div className="pt-4 flex items-center justify-between">
            <button
              type="button"
              onClick={() => navigate('/dashboard')}
              className="text-xs text-slate-500 hover:text-slate-800 font-medium"
            >
              Skip for now
            </button>

            <button
              type="submit"
              disabled={saving}
              className="px-6 py-2.5 rounded-xl bg-purple-600 hover:bg-purple-500 text-white font-bold text-xs shadow-md flex items-center gap-2"
            >
              {saving ? <Loader2 className="w-4 h-4 animate-spin" /> : <>Save & Go to Dashboard <ArrowRight className="w-4 h-4" /></>}
            </button>
          </div>

        </form>

      </div>
    </div>
  );
}
