import React, { useState, useEffect } from 'react';
import { Sparkles, CheckCircle2, PlusCircle, ArrowRight, Play, FileVideo, Image as ImageIcon, Wand2, BookOpen, Layers, Check, ExternalLink, Loader2 } from 'lucide-react';
import { saveStudioProject, fetchStudioProjects } from '../api';

const STARTER_PROJECTS = [
  {
    id: 'sp_1',
    title: 'Product Advertisement',
    type: 'Commercial Ad',
    category: 'AI Advertiser',
    aspectRatio: '16:9 & 9:16',
    duration: '30 seconds',
    whyFits: 'Matches high-demand brand briefs for luxury, fashion, & consumer tech visual spots.',
    goal: 'Create a 30s photorealistic product reveal video using prompt-to-video motion pipelines.',
    deliverables: ['16:9 Landscape 4K Master', '9:16 Vertical Reel', 'Prompt & Motion Process Document'],
    workflow: 'Midjourney v6 (Keyframes) ➔ Runway Gen-3 / Luma Dream Machine ➔ Topaz Video AI (Upscale) ➔ DaVinci Resolve',
    checklist: ['Concept & Moodboard', 'Draft keyframe prompts', 'Generate video motion clips', 'Color grade & sound design', 'Export final 4K cut']
  },
  {
    id: 'sp_2',
    title: 'Cinematic AI Microfilm',
    type: 'Microfilm / Sci-Fi',
    category: 'AI Filmmaker',
    aspectRatio: '16:9',
    duration: '60 seconds',
    whyFits: 'Demonstrates narrative storytelling, character consistency, and cinematic atmosphere.',
    goal: 'Direct a 60-second sci-fi or drama cinematic trailer featuring consistent AI character generation.',
    deliverables: ['16:9 Cinematic Video Cut', 'Voiceover Audio Stems', 'Character LoRA Setup Notes'],
    workflow: 'FLUX.1 / Midjourney ➔ Kling AI / Sora ➔ ElevenLabs (Voiceover) ➔ Udio (Music) ➔ Premier Pro',
    checklist: ['Script & voiceover audio', 'Generate consistent character sheets', 'Animate camera moves', 'Mix audio & SFX', 'Publish teaser']
  },
  {
    id: 'sp_3',
    title: 'Animated Explainer',
    type: '2D/3D Motion Animation',
    category: 'AI Animator',
    aspectRatio: '1:1',
    duration: '45 seconds',
    whyFits: 'SaaS and Web3 creative agencies regularly hire AI animators for product walkthrough reels.',
    goal: 'Synthesize a high-energy animated video explaining a modern tech concept.',
    deliverables: ['1:1 Square Video', 'Vector Graphic Assets Pack', 'Step-by-step Workflow Summary'],
    workflow: 'Recraft AI (Vectors) ➔ Luma / Pika 1.5 ➔ After Effects Composite',
    checklist: ['Storyboard script', 'Vector asset generation', 'Motion interpolation', 'Soundtrack sync', 'Final export']
  },
  {
    id: 'sp_4',
    title: 'Social-Media Campaign',
    type: 'Multi-Format Promo Pack',
    category: 'Motion Designer',
    aspectRatio: '9:16 & 4:5',
    duration: '3x 15s Shorts',
    whyFits: 'Proves agency readiness by supplying cohesive multi-channel content for social campaigns.',
    goal: 'Produce a 3-part vertical video campaign with matching high-impact image ad cards.',
    deliverables: ['3x Vertical Reel Cuts', '5x Feed Visual Posters', 'Campaign Prompt Guide'],
    workflow: 'Ideogram (Typography) ➔ Runway Gen-3 ➔ Canva Magic Studio ➔ CapCut',
    checklist: ['Hook copy & caption draft', 'Typography poster renders', 'Vertical clip generation', 'Social caption styling', 'Package campaign']
  },
  {
    id: 'sp_5',
    title: 'Generative Art Collection',
    type: 'Visual Fine Art',
    category: 'Generative Artist',
    aspectRatio: '4:5',
    duration: 'Static & Motion Art',
    whyFits: 'Establishes your unique aesthetic identity and prompt engineering styling expertise.',
    goal: 'Curate a 5-piece thematic generative art exhibition showcasing advanced controlnet & upscaling.',
    deliverables: ['5x 8K Rendered Artwork Pieces', 'Magnific AI Upscale Details', 'Prompt Exhibition Notes'],
    workflow: 'Stable Diffusion XL / ComfyUI ➔ ControlNet ➔ Magnific AI 8K Upscaler',
    checklist: ['Curate art theme & color palette', 'Generate base diffusion renders', 'Detail refinement with Magnific', 'Document prompt parameters', 'Publish collection']
  },
  {
    id: 'sp_6',
    title: 'Product Visualization',
    type: '3D Studio Rendering',
    category: 'Product Visualizer',
    aspectRatio: '16:9',
    duration: '15 seconds',
    whyFits: 'Demonstrates commercial lighting precision and studio product placement capability.',
    goal: 'Render a photorealistic studio product environment with dynamic lighting and camera rotation.',
    deliverables: ['15s 360 Product Turn Cut', '3x High-Res Still Shots'],
    workflow: 'Flair AI / Pebblely ➔ Luma Dream Machine ➔ DaVinci Resolve',
    checklist: ['Product cutout prep', 'Studio background lighting setup', 'Camera movement generation', 'Final composite & polish']
  }
];

export function StarterStudio({ creator, onOpenAddPortfolio }) {
  const [savedProjects, setSavedProjects] = useState([]);
  const [selectedProject, setSelectedProject] = useState(STARTER_PROJECTS[0]);
  const [loading, setLoading] = useState(false);
  const [projectStatusMap, setProjectStatusMap] = useState({});

  useEffect(() => {
    fetchStudioProjects()
      .then(projects => {
        setSavedProjects(projects);
        const map = {};
        projects.forEach(p => {
          map[p.title] = p.status;
        });
        setProjectStatusMap(map);
      })
      .catch(() => {});
  }, []);

  const handleToggleSaveProject = async (proj) => {
    setLoading(true);
    try {
      const res = await saveStudioProject({
        title: proj.title,
        project_type: proj.type,
        notes: `Deliverables: ${proj.deliverables.join(', ')}`
      });
      
      setProjectStatusMap(prev => ({
        ...prev,
        [proj.title]: res.status
      }));

      const updatedList = await fetchStudioProjects();
      setSavedProjects(updatedList);
    } catch (err) {
      console.warn('Saved locally in demo mode:', err);
      setProjectStatusMap(prev => ({
        ...prev,
        [proj.title]: prev[proj.title] === 'completed' ? 'in_progress' : 'completed'
      }));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white rounded-3xl p-6 sm:p-8 border border-slate-200 shadow-sm space-y-8">
      
      {/* Studio Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-100 pb-6">
        <div>
          <div className="flex items-center gap-2">
            <span className="px-2.5 py-0.5 rounded-full text-[10px] font-bold uppercase bg-purple-100 text-purple-700">
              Rule-Based & AI Tailored
            </span>
            <span className="text-xs text-slate-500">Personalized for {creator?.specialization || 'AI Creators'}</span>
          </div>
          <h2 className="text-2xl font-bold text-slate-900 mt-1">Creator Starter Studio 🚀</h2>
          <p className="text-xs text-slate-500">Build your high-converting portfolio with curated starter projects tailored to your tools and skills.</p>
        </div>

        <button
          onClick={() => onOpenAddPortfolio(selectedProject)}
          className="px-5 py-2.5 rounded-xl bg-purple-600 hover:bg-purple-500 text-white font-bold text-xs shadow-md shadow-purple-600/20 flex items-center gap-2 transition-all hover:scale-105 shrink-0"
        >
          <PlusCircle className="w-4 h-4" />
          Add Completed Work to Portfolio
        </button>
      </div>

      {/* Grid of 6 Starter Suggestions */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {STARTER_PROJECTS.map((proj) => {
          const isSelected = selectedProject.id === proj.id;
          const status = projectStatusMap[proj.title];
          const isDone = status === 'completed';
          const isInProgress = status === 'in_progress';

          return (
            <div
              key={proj.id}
              onClick={() => setSelectedProject(proj)}
              className={`p-5 rounded-2xl border transition-all cursor-pointer flex flex-col justify-between space-y-4 ${
                isSelected
                  ? 'bg-purple-50/60 border-purple-400 ring-2 ring-purple-200 shadow-md'
                  : 'bg-white border-slate-200 hover:border-slate-300 hover:shadow-xs'
              }`}
            >
              <div>
                <div className="flex items-center justify-between mb-2">
                  <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-slate-100 text-slate-600 uppercase">
                    {proj.type}
                  </span>
                  
                  {isDone ? (
                    <span className="px-2 py-0.5 rounded-full text-[10px] font-bold bg-emerald-100 text-emerald-700 flex items-center gap-1">
                      <Check className="w-3 h-3" /> Completed
                    </span>
                  ) : isInProgress ? (
                    <span className="px-2 py-0.5 rounded-full text-[10px] font-bold bg-amber-100 text-amber-700">
                      In Progress
                    </span>
                  ) : (
                    <span className="text-[10px] text-slate-400 font-mono">Starter #{proj.id.split('_')[1]}</span>
                  )}
                </div>

                <h3 className="font-bold text-base text-slate-900">{proj.title}</h3>
                <p className="text-xs text-slate-500 mt-1 line-clamp-2">{proj.goal}</p>
              </div>

              <div className="pt-3 border-t border-slate-100 flex items-center justify-between">
                <span className="text-[10px] font-semibold text-purple-700">
                  Ratio: {proj.aspectRatio}
                </span>

                <button
                  type="button"
                  onClick={(e) => {
                    e.stopPropagation();
                    handleToggleSaveProject(proj);
                  }}
                  disabled={loading}
                  className={`px-3 py-1.5 rounded-lg text-xs font-bold transition-all flex items-center gap-1 ${
                    isDone
                      ? 'bg-emerald-600 text-white hover:bg-emerald-500'
                      : isInProgress
                      ? 'bg-amber-500 text-white hover:bg-amber-400'
                      : 'bg-slate-900 text-white hover:bg-slate-800'
                  }`}
                >
                  {isDone ? 'Mark Active' : isInProgress ? 'Mark Complete' : 'Start Project'}
                </button>
              </div>
            </div>
          );
        })}
      </div>

      {/* Active Starter Project Detail Card */}
      {selectedProject && (
        <div className="bg-slate-900 text-white rounded-3xl p-6 sm:p-8 space-y-6 shadow-xl border border-slate-800">
          
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-800 pb-4">
            <div>
              <div className="flex items-center gap-2 mb-1">
                <span className="px-2.5 py-0.5 bg-purple-500/20 text-purple-300 text-[10px] font-extrabold uppercase rounded border border-purple-500/30">
                  {selectedProject.category} Project Guide
                </span>
                <span className="text-xs text-slate-400 font-mono">Target: {selectedProject.duration}</span>
              </div>
              <h3 className="text-xl font-bold text-white">{selectedProject.title} Blueprint</h3>
            </div>

            <button
              onClick={() => onOpenAddPortfolio(selectedProject)}
              className="px-4 py-2 bg-gradient-to-r from-purple-500 to-indigo-500 hover:from-purple-400 hover:to-indigo-400 text-white font-bold text-xs rounded-xl shadow-md flex items-center gap-2 shrink-0"
            >
              <Wand2 className="w-4 h-4" />
              Upload Result to Portfolio
            </button>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            
            {/* Left Column: Why Fits & Deliverables */}
            <div className="space-y-4">
              <div>
                <h4 className="text-xs font-bold uppercase tracking-wider text-purple-400 mb-1">Why This Project Fits Your Profile</h4>
                <p className="text-xs text-slate-300 leading-relaxed bg-slate-800/60 p-3 rounded-xl border border-slate-700/50">
                  {selectedProject.whyFits}
                </p>
              </div>

              <div>
                <h4 className="text-xs font-bold uppercase tracking-wider text-purple-400 mb-2">Recommended Deliverables</h4>
                <ul className="space-y-1.5">
                  {selectedProject.deliverables.map((item, idx) => (
                    <li key={idx} className="text-xs text-slate-300 flex items-center gap-2">
                      <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400 shrink-0" />
                      {item}
                    </li>
                  ))}
                </ul>
              </div>

              <div>
                <h4 className="text-xs font-bold uppercase tracking-wider text-purple-400 mb-1">Suggested Generative Workflow</h4>
                <p className="text-xs text-indigo-300 font-mono bg-indigo-950/50 p-2.5 rounded-xl border border-indigo-800/40">
                  {selectedProject.workflow}
                </p>
              </div>
            </div>

            {/* Right Column: Step-by-Step Checklist */}
            <div className="bg-slate-800/80 p-5 rounded-2xl border border-slate-700/60 space-y-3">
              <h4 className="text-xs font-bold uppercase tracking-wider text-purple-400 flex items-center justify-between">
                <span>Production Checklist</span>
                <span className="text-[10px] text-slate-400">5 Milestones</span>
              </h4>

              <div className="space-y-2">
                {selectedProject.checklist.map((step, idx) => (
                  <div key={idx} className="flex items-center gap-3 p-2 bg-slate-900/60 rounded-xl border border-slate-800 text-xs">
                    <div className="w-5 h-5 rounded-full bg-purple-900/60 text-purple-300 font-bold text-[10px] flex items-center justify-center shrink-0">
                      {idx + 1}
                    </div>
                    <span className="text-slate-200">{step}</span>
                  </div>
                ))}
              </div>

              <p className="text-[11px] text-slate-400 pt-2 italic">
                Notice: All suggestions are rule-based algorithms aligned with Kampus.VC creator standards.
              </p>
            </div>

          </div>

        </div>
      )}

    </div>
  );
}
