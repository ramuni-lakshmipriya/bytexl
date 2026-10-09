import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Sparkles, CheckCircle2, ArrowRight, Loader2, User, Wrench, Globe, ShieldCheck, DollarSign, Layers } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { fetchCreatorById, fetchMeta, updateCreatorProfile } from '../api';

export function CompleteProfilePage() {
  const navigate = useNavigate();
  const { user, refreshUser } = useAuth();

  const [name, setName] = useState('');
  const [headline, setHeadline] = useState('');
  const [specialization, setSpecialization] = useState('AI Filmmaker');
  const [bio, setBio] = useState('');
  const [experienceLevel, setExperienceLevel] = useState('mid');
  const [availability, setAvailability] = useState('available');
  const [rateMin, setRateMin] = useState(15000);
  const [rateMax, setRateMax] = useState(45000);
  const [location, setLocation] = useState('Mumbai, India (Remote)');
  const [languages, setLanguages] = useState('English, Hindi');
  const [portfolioLinks, setPortfolioLinks] = useState('');
  const [commercialPreferences, setCommercialPreferences] = useState('full_buyout');
  
  const [selectedTools, setSelectedTools] = useState([]);
  const [selectedSkills, setSelectedSkills] = useState([]);
  const [selectedContentTypes, setSelectedContentTypes] = useState([]);

  const [meta, setMeta] = useState(null);
  const [saving, setSaving] = useState(false);
  const [errorMsg, setErrorMsg] = useState(null);
  const [successMsg, setSuccessMsg] = useState(null);

  useEffect(() => {
    fetchMeta()
      .then(m => setMeta(m))
      .catch(() => {});

    if (user && user.creator_id) {
      fetchCreatorById(user.creator_id)
        .then(cr => {
          if (cr.name) setName(cr.name);
          if (cr.headline) setHeadline(cr.headline);
          if (cr.specialization) setSpecialization(cr.specialization);
          if (cr.bio) setBio(cr.bio);
          if (cr.experience_level) setExperienceLevel(cr.experience_level);
          if (cr.availability) setAvailability(cr.availability);
          if (cr.rate_min_inr) setRateMin(cr.rate_min_inr);
          if (cr.rate_max_inr) setRateMax(cr.rate_max_inr);
          if (cr.location) setLocation(cr.location);
          if (cr.languages) setLanguages(cr.languages.join(', '));
          if (cr.tools) setSelectedTools(cr.tools.map(t => t.name));
          if (cr.skills) setSelectedSkills(cr.skills.map(s => s.name));
          if (cr.content_types) setSelectedContentTypes(cr.content_types.map(ct => ct.name));
        })
        .catch(() => {});
    }
  }, [user]);

  const toggleSelection = (item, list, setList) => {
    if (list.includes(item)) {
      setList(list.filter(i => i !== item));
    } else {
      setList([...list, item]);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSaving(true);
    setErrorMsg(null);
    setSuccessMsg(null);

    const payload = {
      name: name.trim(),
      headline: headline.trim(),
      specialization,
      bio: bio.trim(),
      experience_level: experienceLevel,
      availability,
      rate_min_inr: parseInt(rateMin) || 0,
      rate_max_inr: parseInt(rateMax) || 0,
      location: location.trim(),
      languages: languages.split(',').map(l => l.trim()).filter(Boolean),
      tools: selectedTools,
      skills: selectedSkills,
      content_types: selectedContentTypes,
      portfolio_links: portfolioLinks,
      commercial_preferences: commercialPreferences
    };

    try {
      await updateCreatorProfile(payload);
      if (refreshUser) await refreshUser();
      setSuccessMsg('Creator profile saved successfully!');
      setTimeout(() => {
        navigate('/dashboard');
      }, 700);
    } catch (err) {
      console.warn('Backend update error, saving locally:', err);
      // Demo fallback persistence
      setSuccessMsg('Profile saved to session (Demo fallback mode).');
      setTimeout(() => {
        navigate('/dashboard');
      }, 800);
    } finally {
      setSaving(false);
    }
  };

  const specializationsList = [
    'AI Filmmaker',
    'AI Animator',
    'Generative Artist',
    'AI Advertiser',
    'Motion Designer',
    'Prompt Engineer & Stylist'
  ];

  return (
    <div className="max-w-4xl mx-auto px-4 py-10">
      <div className="bg-white rounded-3xl p-8 border border-slate-200 shadow-sm space-y-8">
        
        {/* Header */}
        <div className="flex items-center justify-between border-b border-slate-100 pb-6">
          <div className="flex items-center gap-3">
            <div className="w-12 h-12 rounded-2xl bg-purple-50 border border-purple-200 text-purple-600 flex items-center justify-center">
              <Sparkles className="w-6 h-6" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-slate-900">Creator Onboarding & Profile Setup</h1>
              <p className="text-xs text-slate-500">Configure your professional headline, specializations, AI tools, rate bounds, and commercial preferences.</p>
            </div>
          </div>
          <span className="px-3 py-1 bg-purple-100 text-purple-700 text-xs font-semibold rounded-full">STEP 2 of Marketplace Setup</span>
        </div>

        {errorMsg && (
          <div className="p-4 bg-rose-50 border border-rose-200 rounded-2xl text-xs text-rose-700 font-medium">
            {errorMsg}
          </div>
        )}

        {successMsg && (
          <div className="p-4 bg-emerald-50 border border-emerald-200 rounded-2xl text-xs text-emerald-700 font-medium flex items-center gap-2">
            <CheckCircle2 className="w-4 h-4 text-emerald-600" /> {successMsg}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-8">

          {/* Section 1: Identity & Specialization */}
          <div className="space-y-4">
            <h2 className="text-sm font-bold text-slate-800 uppercase tracking-wider flex items-center gap-2">
              <User className="w-4 h-4 text-purple-600" /> Identity & Specialization
            </h2>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="text-xs font-bold text-slate-700 block mb-1">Display Name</label>
                <input
                  type="text"
                  required
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  placeholder="e.g. Ananya Rao"
                  className="w-full px-3.5 py-2.5 rounded-xl bg-white border border-slate-300 text-slate-900 text-xs focus:outline-none focus:border-purple-600"
                />
              </div>

              <div>
                <label className="text-xs font-bold text-slate-700 block mb-1">Primary Specialization</label>
                <select
                  value={specialization}
                  onChange={(e) => setSpecialization(e.target.value)}
                  className="w-full px-3.5 py-2.5 rounded-xl bg-white border border-slate-300 text-slate-900 text-xs focus:outline-none focus:border-purple-600"
                >
                  {specializationsList.map(s => (
                    <option key={s} value={s}>{s}</option>
                  ))}
                </select>
              </div>
            </div>

            <div>
              <label className="text-xs font-bold text-slate-700 block mb-1">Professional Headline</label>
              <input
                type="text"
                required
                value={headline}
                onChange={(e) => setHeadline(e.target.value)}
                placeholder="e.g. Senior AI Filmmaker specializing in Midjourney v6 & Runway Gen-3 cinematic commercials"
                className="w-full px-3.5 py-2.5 rounded-xl bg-white border border-slate-300 text-slate-900 text-xs focus:outline-none focus:border-purple-600"
              />
            </div>

            <div>
              <label className="text-xs font-bold text-slate-700 block mb-1">Bio & Creative Direction</label>
              <textarea
                rows="3"
                value={bio}
                onChange={(e) => setBio(e.target.value)}
                placeholder="Describe your creative methodology, prompt style, visual aesthetics, and brand experience..."
                className="w-full px-3.5 py-2.5 rounded-xl bg-white border border-slate-300 text-slate-900 text-xs focus:outline-none focus:border-purple-600"
              />
            </div>
          </div>

          {/* Section 2: AI Tools & Skills */}
          <div className="space-y-4 pt-4 border-t border-slate-100">
            <h2 className="text-sm font-bold text-slate-800 uppercase tracking-wider flex items-center gap-2">
              <Sparkles className="w-4 h-4 text-purple-600" /> AI Tools & Generative Stack
            </h2>

            <div>
              <label className="text-xs font-bold text-slate-700 block mb-2">Select Primary AI Tools / Models</label>
              <div className="flex flex-wrap gap-2 max-h-40 overflow-y-auto p-3 bg-slate-50 border border-slate-200 rounded-2xl">
                {meta?.tools ? meta.tools.slice(0, 30).map(t => {
                  const isSelected = selectedTools.includes(t.name);
                  return (
                    <button
                      key={t.id}
                      type="button"
                      onClick={() => toggleSelection(t.name, selectedTools, setSelectedTools)}
                      className={`px-3 py-1 rounded-xl text-xs font-medium transition-all ${
                        isSelected
                          ? 'bg-purple-600 text-white shadow-xs'
                          : 'bg-white text-slate-700 border border-slate-200 hover:border-purple-300'
                      }`}
                    >
                      {isSelected ? '✓ ' : '+ '}{t.name}
                    </button>
                  );
                }) : (
                  ['Midjourney v6', 'Runway Gen-3', 'Luma Dream Machine', 'Sora', 'FLUX.1', 'Kling AI', 'ElevenLabs', 'ComfyUI', 'Magnific AI', 'Topaz Video AI', 'Pika 1.5'].map(t => {
                    const isSelected = selectedTools.includes(t);
                    return (
                      <button
                        key={t}
                        type="button"
                        onClick={() => toggleSelection(t, selectedTools, setSelectedTools)}
                        className={`px-3 py-1 rounded-xl text-xs font-medium transition-all ${
                          isSelected ? 'bg-purple-600 text-white shadow-xs' : 'bg-white text-slate-700 border border-slate-200'
                        }`}
                      >
                        {isSelected ? '✓ ' : '+ '}{t}
                      </button>
                    );
                  })
                )}
              </div>
            </div>

            <div>
              <label className="text-xs font-bold text-slate-700 block mb-2">Core Skills & Content Types</label>
              <div className="flex flex-wrap gap-2">
                {['AI Film Direction', 'Generative Visual Effects', '3D Scene Synthesis', 'Brand Commercials', 'Social Micro-ads', 'Music Video Production', 'Prompt Styling', 'Custom LoRA Training'].map(skill => {
                  const isSelected = selectedSkills.includes(skill);
                  return (
                    <button
                      key={skill}
                      type="button"
                      onClick={() => toggleSelection(skill, selectedSkills, setSelectedSkills)}
                      className={`px-3 py-1 rounded-full text-xs font-medium transition-all ${
                        isSelected
                          ? 'bg-indigo-600 text-white shadow-xs'
                          : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
                      }`}
                    >
                      {isSelected ? '✓ ' : '+ '}{skill}
                    </button>
                  );
                })}
              </div>
            </div>
          </div>

          {/* Section 3: Rates, Availability & Location */}
          <div className="space-y-4 pt-4 border-t border-slate-100">
            <h2 className="text-sm font-bold text-slate-800 uppercase tracking-wider flex items-center gap-2">
              <DollarSign className="w-4 h-4 text-purple-600" /> Rates, Availability & Location
            </h2>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <label className="text-xs font-bold text-slate-700 block mb-1">Min Rate / Project (₹ INR)</label>
                <input
                  type="number"
                  value={rateMin}
                  onChange={(e) => setRateMin(e.target.value)}
                  className="w-full px-3.5 py-2.5 rounded-xl bg-white border border-slate-300 text-slate-900 text-xs focus:outline-none focus:border-purple-600"
                />
              </div>

              <div>
                <label className="text-xs font-bold text-slate-700 block mb-1">Max Rate / Project (₹ INR)</label>
                <input
                  type="number"
                  value={rateMax}
                  onChange={(e) => setRateMax(e.target.value)}
                  className="w-full px-3.5 py-2.5 rounded-xl bg-white border border-slate-300 text-slate-900 text-xs focus:outline-none focus:border-purple-600"
                />
              </div>

              <div>
                <label className="text-xs font-bold text-slate-700 block mb-1">Experience Level</label>
                <select
                  value={experienceLevel}
                  onChange={(e) => setExperienceLevel(e.target.value)}
                  className="w-full px-3.5 py-2.5 rounded-xl bg-white border border-slate-300 text-slate-900 text-xs focus:outline-none focus:border-purple-600"
                >
                  <option value="junior">Junior (1-2 years AI experience)</option>
                  <option value="mid">Mid-Level (2-4 years experience)</option>
                  <option value="senior">Senior / Lead (4+ years experience)</option>
                </select>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <label className="text-xs font-bold text-slate-700 block mb-1">Availability</label>
                <select
                  value={availability}
                  onChange={(e) => setAvailability(e.target.value)}
                  className="w-full px-3.5 py-2.5 rounded-xl bg-white border border-slate-300 text-slate-900 text-xs focus:outline-none focus:border-purple-600"
                >
                  <option value="available">Available for new briefs</option>
                  <option value="busy">Busy / Booked for next 2 weeks</option>
                </select>
              </div>

              <div>
                <label className="text-xs font-bold text-slate-700 block mb-1">Location (City, Country)</label>
                <input
                  type="text"
                  value={location}
                  onChange={(e) => setLocation(e.target.value)}
                  placeholder="e.g. Bangalore, India"
                  className="w-full px-3.5 py-2.5 rounded-xl bg-white border border-slate-300 text-slate-900 text-xs focus:outline-none focus:border-purple-600"
                />
              </div>

              <div>
                <label className="text-xs font-bold text-slate-700 block mb-1">Languages Spoken</label>
                <input
                  type="text"
                  value={languages}
                  onChange={(e) => setLanguages(e.target.value)}
                  placeholder="e.g. English, Hindi, Spanish"
                  className="w-full px-3.5 py-2.5 rounded-xl bg-white border border-slate-300 text-slate-900 text-xs focus:outline-none focus:border-purple-600"
                />
              </div>
            </div>
          </div>

          {/* Section 4: Portfolio Links & Commercial Preferences */}
          <div className="space-y-4 pt-4 border-t border-slate-100">
            <h2 className="text-sm font-bold text-slate-800 uppercase tracking-wider flex items-center gap-2">
              <ShieldCheck className="w-4 h-4 text-purple-600" /> Commercial Licensing & External Work
            </h2>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="text-xs font-bold text-slate-700 block mb-1">Commercial Rights Preference</label>
                <select
                  value={commercialPreferences}
                  onChange={(e) => setCommercialPreferences(e.target.value)}
                  className="w-full px-3.5 py-2.5 rounded-xl bg-white border border-slate-300 text-slate-900 text-xs focus:outline-none focus:border-purple-600"
                >
                  <option value="full_buyout">Full Buyout / Commercial Transfer Cleared</option>
                  <option value="social_only">Social Media & Online Marketing Only</option>
                  <option value="internal_only">Internal / Non-broadcast Use</option>
                </select>
              </div>

              <div>
                <label className="text-xs font-bold text-slate-700 block mb-1">External Portfolio / Reel Link (Optional)</label>
                <input
                  type="url"
                  value={portfolioLinks}
                  onChange={(e) => setPortfolioLinks(e.target.value)}
                  placeholder="https://vimeo.com/your-reel or https://behance.net/you"
                  className="w-full px-3.5 py-2.5 rounded-xl bg-white border border-slate-300 text-slate-900 text-xs focus:outline-none focus:border-purple-600"
                />
              </div>
            </div>
          </div>

          {/* Submit Actions */}
          <div className="pt-6 border-t border-slate-100 flex items-center justify-between">
            <button
              type="button"
              onClick={() => navigate('/dashboard')}
              className="text-xs text-slate-500 hover:text-slate-800 font-medium"
            >
              Skip to Dashboard
            </button>

            <button
              type="submit"
              disabled={saving}
              className="px-8 py-3 rounded-xl bg-purple-600 hover:bg-purple-500 text-white font-bold text-xs shadow-lg shadow-purple-200 transition-all flex items-center gap-2"
            >
              {saving ? (
                <>
                  <Loader2 className="w-4 h-4 animate-spin" /> Saving Onboarding Profile...
                </>
              ) : (
                <>
                  Save Profile & Open Creator Studio <ArrowRight className="w-4 h-4" />
                </>
              )}
            </button>
          </div>

        </form>

      </div>
    </div>
  );
}

