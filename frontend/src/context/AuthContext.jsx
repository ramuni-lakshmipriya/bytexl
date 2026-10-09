import React, { createContext, useContext, useState, useEffect } from 'react';
import { getMe, loginApi, loginDemoApi, signupCreatorApi, signupBrandApi, logoutApi, getAuthConfigStatus } from '../api';

const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [authConfig, setAuthConfig] = useState({
    google_configured: false,
    facebook_configured: false,
    instagram_configured: false
  });

  const checkAuth = async () => {
    try {
      const u = await getMe();
      setUser(u);
    } catch (e) {
      setUser(null);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    checkAuth();
    getAuthConfigStatus()
      .then(cfg => setAuthConfig(cfg))
      .catch(() => {});
  }, []);

  const login = async (email, password) => {
    const u = await loginApi(email, password);
    setUser(u);
    return u;
  };

  const loginDemo = async (role) => {
    const u = await loginDemoApi(role);
    setUser(u);
    return u;
  };

  const signupCreator = async (data) => {
    const u = await signupCreatorApi(data);
    setUser(u);
    return u;
  };

  const signupBrand = async (data) => {
    const u = await signupBrandApi(data);
    setUser(u);
    return u;
  };

  const logout = async () => {
    await logoutApi();
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{
      user,
      setUser,
      loading,
      authConfig,
      login,
      loginDemo,
      signupCreator,
      signupBrand,
      logout,
      checkAuth
    }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}
