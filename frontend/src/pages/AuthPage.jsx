import { useTheme } from '../context/ThemeContext';
import AuthForm from '../components/AuthForm';
import { login, register } from '../api/auth';
import { useState } from 'react';
import { MoonIcon, SunIcon } from '@heroicons/react/24/outline';

export default function AuthPage() {
  const { isDarkMode, toggleTheme } = useTheme();
  const [loading, setLoading] = useState(false);

  const handleLogin = async (username, password) => {
    setLoading(true);
    try {
      const response = await login(username, password);
      // Handle successful login (e.g., save token, redirect)
      console.log('Login successful:', response);
      return response;
    } catch (error) {
      throw error;
    } finally {
      setLoading(false);
    }
  };

  const handleRegister = async (email, username, password) => {
    setLoading(true);
    try {
      const response = await register(email, username, password);
      // Handle successful registration
      console.log('Registration successful:', response);
      return response;
    } catch (error) {
      throw error;
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center p-4 bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-900 dark:to-gray-800 transition-colors duration-500">
      {/* Theme Toggle */}
      <button
        onClick={toggleTheme}
        className="fixed top-4 right-4 p-2 rounded-full bg-white dark:bg-gray-800 shadow-lg hover:shadow-xl transition-all duration-300"
        aria-label="Toggle theme"
      >
        {isDarkMode ? (
          <SunIcon className="h-6 w-6 text-yellow-500" />
        ) : (
          <MoonIcon className="h-6 w-6 text-gray-700" />
        )}
      </button>

      {/* Logo or Brand */}
      <div className="mb-8 text-center">
        <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-600 to-blue-400 bg-clip-text text-transparent">
          Crypto Asset Marketplace
        </h1>
      </div>

      {/* Auth Form */}
      <AuthForm
        onLogin={handleLogin}
        onRegister={handleRegister}
        loading={loading}
      />

      {/* Footer */}
      <footer className="mt-8 text-sm text-gray-600 dark:text-gray-400">
        © 2025 Crypto Asset Marketplace. All rights reserved.
      </footer>
    </div>
  );
}