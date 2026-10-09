import React, { useState, useEffect } from 'react';
import { Briefcase, CheckCircle2, Clock, Send, ShieldCheck, DollarSign, AlertCircle, ExternalLink, Loader2, RefreshCw } from 'lucide-react';
import { fetchMyApplications, fetchBriefApplications, updateApplicationStatus, submitDelivery } from '../api';

export function EngagementTracker({ user, briefId = null }) {
  const [applications, setApplications] = useState([]);
  const [loading, setLoading] = useState(true);
  const [activeDeliveryApp, setActiveDeliveryApp] = useState(null);
  const [deliveryUrl, setDeliveryUrl] = useState('');
  const [deliveryNotes, setDeliveryNotes] = useState('');
  const [revisionFeedback, setRevisionFeedback] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [actionSuccess, setActionSuccess] = useState(null);

  const loadData = async () => {
    setLoading(true);
    try {
      if (user?.role === 'creator') {
        const apps = await fetchMyApplications();
        setApplications(apps);
      } else if (briefId) {
        const apps = await fetchBriefApplications(briefId);
        setApplications(apps);
      }
    } catch (err) {
      console.warn('Failed to load applications:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, [user, briefId]);

  const handleStatusUpdate = async (appId, newStatus, feedback = '') => {
    setSubmitting(true);
    try {
      await updateApplicationStatus(appId, { status: newStatus, revision_feedback: feedback });
      setActionSuccess(`Application status updated to ${newStatus.replace('_', ' ')}!`);
      await loadData();
      setTimeout(() => setActionSuccess(null), 3000);
    } catch (err) {
      console.error(err);
    } finally {
      setSubmitting(false);
    }
  };

  const handleDeliverySubmit = async (e) => {
    e.preventDefault();
    if (!activeDeliveryApp) return;

    setSubmitting(true);
    try {
      await submitDelivery(activeDeliveryApp.id, {
        delivery_url: deliveryUrl,
        delivery_notes: deliveryNotes
      });
      setActionSuccess('Delivery URL submitted to brand!');
      setActiveDeliveryApp(null);
      setDeliveryUrl('');
      setDeliveryNotes('');
      await loadData();
      setTimeout(() => setActionSuccess(null), 3000);
    } catch (err) {
      console.error(err);
    } finally {
      setSubmitting(false);
    }
  };

  const formatCurrency = (amount) => {
    if (!amount) return 'N/A';
    return `₹${amount.toLocaleString('en-IN')}`;
  };

  if (loading) {
    return (
      <div className="p-6 bg-white rounded-3xl border border-slate-200 text-center text-xs text-slate-500">
        <Loader2 className="w-5 h-5 animate-spin mx-auto text-purple-600 mb-2" />
        Loading campaign applications and engagements...
      </div>
    );
  }

  return (
    <div className="space-y-6">
      
      {actionSuccess && (
        <div className="p-4 bg-emerald-50 border border-emerald-200 text-emerald-800 rounded-2xl text-xs font-bold flex items-center gap-2">
          <CheckCircle2 className="w-4 h-4 text-emerald-600" />
          {actionSuccess}
        </div>
      )}

      {/* Creator View: My Applications & Engagements */}
      {user?.role === 'creator' && (
        <div className="space-y-4">
          <h3 className="text-lg font-bold text-slate-900 flex items-center gap-2">
            <Briefcase className="w-5 h-5 text-purple-600" />
            My Campaign Applications & Live Engagements ({applications.length})
          </h3>

          {applications.length === 0 ? (
            <div className="bg-white p-8 rounded-3xl border border-slate-200 text-center text-xs text-slate-500">
              You haven't applied to any campaign briefs yet. Browse open briefs on the Marketplace to apply!
            </div>
          ) : (
            <div className="space-y-4">
              {applications.map(app => (
                <div key={app.id} className="bg-white p-6 rounded-3xl border border-slate-200 shadow-xs space-y-4">
                  
                  <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-100 pb-3">
                    <div>
                      <span className="text-xs text-slate-400 font-mono">App ID: {app.id}</span>
                      <h4 className="font-bold text-base text-slate-900">{app.brief_title}</h4>
                    </div>

                    <div className="flex items-center gap-2">
                      <span className={`px-3 py-1 rounded-full text-xs font-extrabold uppercase border ${
                        app.status === 'completed' ? 'bg-emerald-50 text-emerald-700 border-emerald-200' :
                        app.status === 'delivered' ? 'bg-indigo-50 text-indigo-700 border-indigo-200' :
                        app.status === 'accepted' || app.status === 'in_progress' ? 'bg-purple-50 text-purple-700 border-purple-200' :
                        app.status === 'shortlisted' ? 'bg-amber-50 text-amber-700 border-amber-200' :
                        'bg-slate-100 text-slate-600 border-slate-200'
                      }`}>
                        Status: {app.status.replace('_', ' ')}
                      </span>

                      <span className="px-2.5 py-1 rounded-full text-[10px] font-semibold bg-emerald-100/60 text-emerald-800 border border-emerald-200">
                        🛡️ {app.payment_status === 'payment_released' ? 'Payment Released (Simulated)' : 'Payment Escrow Held (Simulated)'}
                      </span>
                    </div>
                  </div>

                  <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 text-xs bg-slate-50 p-3 rounded-2xl border border-slate-100">
                    <div>
                      <span className="text-slate-400 block font-medium">Proposed Rate</span>
                      <span className="font-bold text-slate-800">{formatCurrency(app.proposed_rate_inr)}</span>
                    </div>
                    <div>
                      <span className="text-slate-400 block font-medium">Est. Delivery Time</span>
                      <span className="font-bold text-slate-800">{app.estimated_days} days</span>
                    </div>
                    <div>
                      <span className="text-slate-400 block font-medium">Applied Date</span>
                      <span className="font-bold text-slate-800">{new Date(app.created_at).toLocaleDateString()}</span>
                    </div>
                  </div>

                  {app.pitch && (
                    <p className="text-xs text-slate-600 italic bg-purple-50/40 p-3 rounded-xl border border-purple-100">
                      "{app.pitch}"
                    </p>
                  )}

                  {/* Delivery Info */}
                  {app.delivery_url && (
                    <div className="p-3 bg-indigo-50 border border-indigo-200 rounded-xl text-xs space-y-1">
                      <div className="font-bold text-indigo-900 flex items-center gap-1.5">
                        <Send className="w-3.5 h-3.5 text-indigo-600" /> Submitted Delivery:
                      </div>
                      <a href={app.delivery_url} target="_blank" rel="noreferrer" className="text-indigo-600 underline font-mono break-all flex items-center gap-1">
                        {app.delivery_url} <ExternalLink className="w-3 h-3" />
                      </a>
                      {app.delivery_notes && <p className="text-slate-600">{app.delivery_notes}</p>}
                    </div>
                  )}

                  {app.revision_feedback && (
                    <div className="p-3 bg-amber-50 border border-amber-200 rounded-xl text-xs text-amber-900 space-y-1">
                      <div className="font-bold flex items-center gap-1.5">
                        <AlertCircle className="w-3.5 h-3.5 text-amber-600" /> Revision Requested by Brand:
                      </div>
                      <p>{app.revision_feedback}</p>
                    </div>
                  )}

                  {/* Delivery Action Button */}
                  {(app.status === 'accepted' || app.status === 'in_progress' || app.status === 'revision_requested') && (
                    <button
                      onClick={() => setActiveDeliveryApp(app)}
                      className="px-4 py-2 bg-purple-600 hover:bg-purple-500 text-white font-bold text-xs rounded-xl shadow-xs flex items-center gap-2"
                    >
                      <Send className="w-3.5 h-3.5" /> Submit Delivery URL & Assets
                    </button>
                  )}

                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* Brand View: Applicants List */}
      {user?.role === 'brand' && (
        <div className="space-y-4">
          <h3 className="text-lg font-bold text-slate-900 flex items-center justify-between">
            <span>Applicants for this Brief ({applications.length})</span>
            <span className="text-xs font-normal text-slate-500">Escrow payments simulated for hackathon evaluation</span>
          </h3>

          {applications.length === 0 ? (
            <div className="bg-white p-6 rounded-3xl border border-slate-200 text-center text-xs text-slate-500">
              No creators have applied to this brief yet. High match score creators are notified!
            </div>
          ) : (
            <div className="space-y-4">
              {applications.map(app => (
                <div key={app.id} className="bg-white p-6 rounded-3xl border border-slate-200 shadow-xs space-y-4">
                  
                  <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-100 pb-3">
                    <div className="flex items-center gap-3">
                      <img
                        src={app.creator_avatar || 'https://picsum.photos/seed/creator/100'}
                        alt={app.creator_name}
                        className="w-12 h-12 rounded-2xl object-cover border border-slate-200"
                      />
                      <div>
                        <h4 className="font-bold text-base text-slate-900">{app.creator_name}</h4>
                        <p className="text-xs text-slate-500">{app.creator_headline}</p>
                      </div>
                    </div>

                    <div className="flex items-center gap-2">
                      <span className={`px-3 py-1 rounded-full text-xs font-extrabold uppercase border ${
                        app.status === 'completed' ? 'bg-emerald-50 text-emerald-700 border-emerald-200' :
                        app.status === 'delivered' ? 'bg-indigo-50 text-indigo-700 border-indigo-200' :
                        app.status === 'accepted' ? 'bg-purple-50 text-purple-700 border-purple-200' :
                        'bg-slate-100 text-slate-600 border-slate-200'
                      }`}>
                        {app.status.replace('_', ' ')}
                      </span>
                    </div>
                  </div>

                  <p className="text-xs text-slate-700 bg-slate-50 p-3 rounded-xl border border-slate-200">
                    <strong className="text-slate-900 block mb-0.5">Pitch Proposal:</strong>
                    "{app.pitch}"
                  </p>

                  <div className="flex items-center justify-between text-xs text-slate-600 bg-purple-50/40 p-3 rounded-xl border border-purple-100">
                    <span>Proposed Rate: <strong className="text-purple-900 font-extrabold">{formatCurrency(app.proposed_rate_inr)}</strong></span>
                    <span>Timeline: <strong className="text-purple-900 font-bold">{app.estimated_days} days</strong></span>
                    <span className="text-emerald-700 font-semibold">🛡️ Escrow {app.payment_status}</span>
                  </div>

                  {/* Delivery URL Display */}
                  {app.delivery_url && (
                    <div className="p-4 bg-indigo-50 border border-indigo-200 rounded-2xl text-xs space-y-2">
                      <div className="font-bold text-indigo-900 flex items-center justify-between">
                        <span>Submitted Delivery Media:</span>
                        <span className="text-[10px] text-indigo-700 uppercase bg-indigo-100 px-2 py-0.5 rounded font-mono">Ready for Review</span>
                      </div>
                      <a href={app.delivery_url} target="_blank" rel="noreferrer" className="text-indigo-600 underline font-mono break-all flex items-center gap-1">
                        {app.delivery_url} <ExternalLink className="w-3 h-3" />
                      </a>
                      {app.delivery_notes && <p className="text-slate-700 font-medium">Notes: {app.delivery_notes}</p>}
                    </div>
                  )}

                  {/* Brand Decision Actions */}
                  <div className="pt-2 flex flex-wrap items-center gap-2">
                    {app.status === 'applied' && (
                      <>
                        <button
                          onClick={() => handleStatusUpdate(app.id, 'shortlisted')}
                          disabled={submitting}
                          className="px-3.5 py-2 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-800 text-xs font-bold"
                        >
                          Shortlist Applicant
                        </button>
                        <button
                          onClick={() => handleStatusUpdate(app.id, 'accepted')}
                          disabled={submitting}
                          className="px-4 py-2 rounded-xl bg-purple-600 hover:bg-purple-500 text-white text-xs font-bold shadow-xs"
                        >
                          Accept & Hire Creator (Escrow Held)
                        </button>
                      </>
                    )}

                    {app.status === 'shortlisted' && (
                      <button
                        onClick={() => handleStatusUpdate(app.id, 'accepted')}
                        disabled={submitting}
                        className="px-4 py-2 rounded-xl bg-purple-600 hover:bg-purple-500 text-white text-xs font-bold shadow-xs"
                      >
                        Accept & Hire Creator
                      </button>
                    )}

                    {(app.status === 'delivered' || app.status === 'in_progress' || app.status === 'accepted') && (
                      <>
                        <button
                          onClick={() => {
                            const note = prompt('Enter revision notes for creator:');
                            if (note) handleStatusUpdate(app.id, 'revision_requested', note);
                          }}
                          disabled={submitting}
                          className="px-3.5 py-2 rounded-xl bg-amber-100 hover:bg-amber-200 text-amber-900 text-xs font-bold"
                        >
                          Request Revision
                        </button>

                        <button
                          onClick={() => handleStatusUpdate(app.id, 'completed')}
                          disabled={submitting}
                          className="px-4 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-bold shadow-md shadow-emerald-200"
                        >
                          Approve Work & Release Payment (Simulated)
                        </button>
                      </>
                    )}
                  </div>

                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* Delivery Submit Modal */}
      {activeDeliveryApp && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/60 backdrop-blur-xs p-4">
          <div className="bg-white rounded-3xl max-w-lg w-full p-6 border border-slate-200 shadow-2xl space-y-4">
            <h3 className="text-lg font-bold text-slate-900">Submit Delivery for {activeDeliveryApp.brief_title}</h3>
            
            <form onSubmit={handleDeliverySubmit} className="space-y-3 text-xs">
              <div>
                <label className="font-bold text-slate-700 block mb-1">Final Video / Asset Delivery URL *</label>
                <input
                  type="url"
                  required
                  value={deliveryUrl}
                  onChange={(e) => setDeliveryUrl(e.target.value)}
                  placeholder="https://vimeo.com/... or Google Drive / Frame.io link"
                  className="w-full px-3.5 py-2.5 rounded-xl border border-slate-300 focus:outline-none focus:border-purple-600 font-mono"
                />
              </div>

              <div>
                <label className="font-bold text-slate-700 block mb-1">Delivery Notes & Keyframe Log</label>
                <textarea
                  rows="3"
                  value={deliveryNotes}
                  onChange={(e) => setDeliveryNotes(e.target.value)}
                  placeholder="Notes for brand review, aspect ratio formats included, or prompt notes..."
                  className="w-full px-3.5 py-2.5 rounded-xl border border-slate-300 focus:outline-none focus:border-purple-600"
                />
              </div>

              <div className="pt-3 flex items-center justify-end gap-3">
                <button
                  type="button"
                  onClick={() => setActiveDeliveryApp(null)}
                  className="px-4 py-2 text-slate-500 font-semibold"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={submitting}
                  className="px-5 py-2 rounded-xl bg-purple-600 hover:bg-purple-500 text-white font-bold shadow-md"
                >
                  {submitting ? <Loader2 className="w-4 h-4 animate-spin" /> : 'Submit Delivery'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

    </div>
  );
}
