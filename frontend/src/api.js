const API_BASE = '/api';

async function request(url, options = {}) {
  options.credentials = 'include';
  options.headers = {
    'Content-Type': 'application/json',
    ...(options.headers || {})
  };

  const res = await fetch(`${API_BASE}${url}`, options);
  if (!res.ok) {
    const errData = await res.json().catch(() => ({}));
    throw new Error(errData.detail || `Request failed with status ${res.status}`);
  }
  return res.json();
}

export async function fetchMeta() {
  return request('/meta');
}

export async function fetchCreators(params = {}) {
  const query = new URLSearchParams();
  Object.entries(params).forEach(([key, val]) => {
    if (val !== undefined && val !== null && val !== '') {
      if (Array.isArray(val)) {
        val.forEach(item => query.append(key, item));
      } else {
        query.append(key, val);
      }
    }
  });
  return request(`/creators?${query.toString()}`);
}

export async function fetchCreatorById(id) {
  return request(`/creators/${id}`);
}

export async function fetchBriefs(status = null) {
  const query = status ? `?status=${status}` : '';
  return request(`/briefs${query}`);
}

export async function fetchBriefById(id) {
  return request(`/briefs/${id}`);
}

export async function createBrief(briefData) {
  return request('/briefs', {
    method: 'POST',
    body: JSON.stringify(briefData)
  });
}

export async function draftBriefAI(prompt) {
  return request('/briefs/draft', {
    method: 'POST',
    body: JSON.stringify({ prompt })
  });
}

export async function fetchBriefMatches(briefId) {
  return request(`/briefs/${briefId}/matches`);
}

// --- Auth APIs ---
export async function getAuthConfigStatus() {
  return request('/auth/config-status');
}

export async function getMe() {
  return request('/auth/me');
}

export async function loginApi(email, password) {
  return request('/auth/login', {
    method: 'POST',
    body: JSON.stringify({ email, password })
  });
}

export async function loginDemoApi(role) {
  return request('/auth/login/demo', {
    method: 'POST',
    body: JSON.stringify({ role })
  });
}

export async function signupCreatorApi(creatorData) {
  return request('/auth/signup/creator', {
    method: 'POST',
    body: JSON.stringify(creatorData)
  });
}

export async function signupBrandApi(brandData) {
  return request('/auth/signup/brand', {
    method: 'POST',
    body: JSON.stringify(brandData)
  });
}

export async function logoutApi() {
  return request('/auth/logout', { method: 'POST' });
}

export async function fetchDashboard() {
  return request('/dashboard');
}

// --- Creator Profile & Onboarding ---
export async function updateCreatorProfile(data) {
  return request('/creators/me', {
    method: 'PUT',
    body: JSON.stringify(data)
  });
}

// --- Creator Portfolio CRUD ---
export async function addPortfolioItem(data) {
  return request('/creators/me/portfolio', {
    method: 'POST',
    body: JSON.stringify(data)
  });
}

export async function updatePortfolioItem(itemId, data) {
  return request(`/creators/me/portfolio/${itemId}`, {
    method: 'PUT',
    body: JSON.stringify(data)
  });
}

export async function deletePortfolioItem(itemId) {
  return request(`/creators/me/portfolio/${itemId}`, {
    method: 'DELETE'
  });
}

// --- Starter Studio ---
export async function fetchStudioProjects() {
  return request('/creators/me/studio-projects');
}

export async function saveStudioProject(data) {
  return request('/creators/me/studio-projects', {
    method: 'POST',
    body: JSON.stringify(data)
  });
}

// --- Engagement Workflow ---
export async function applyToBrief(briefId, data) {
  return request(`/briefs/${briefId}/apply`, {
    method: 'POST',
    body: JSON.stringify(data)
  });
}

export async function fetchBriefApplications(briefId) {
  return request(`/briefs/${briefId}/applications`);
}

export async function fetchMyApplications() {
  return request('/briefs/applications/my');
}

export async function updateApplicationStatus(appId, data) {
  return request(`/briefs/applications/${appId}`, {
    method: 'PUT',
    body: JSON.stringify(data)
  });
}

export async function submitDelivery(appId, data) {
  return request(`/briefs/applications/${appId}/deliver`, {
    method: 'POST',
    body: JSON.stringify(data)
  });
}

