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
