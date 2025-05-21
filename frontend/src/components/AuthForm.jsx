import { useState } from 'react';
import { ArrowPathIcon } from '@heroicons/react/24/outline';

export default function AuthForm({ onLogin, onRegister, loading }) {
  const [mode, setMode] = useState('login');
  const [loginData, setLoginData] = useState({ username: '', password: '' });
  const [registerData, setRegisterData] = useState({ email: '', username: '', password: '' });
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [isFlipping, setIsFlipping] = useState(false);

  const handleToggle = () => {
    setError('');
    setSuccess('');
    setIsFlipping(true);
    setTimeout(() => {
      setMode(mode === 'login' ? 'register' : 'login');
      setIsFlipping(false);
    }, 300);
  };

  const handleLogin = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');
    try {
      await onLogin(loginData.username, loginData.password);
      setSuccess('Login successful!');
    } catch (err) {
      setError(err.response?.data?.detail || 'Login failed');
    }
  };

  const handleRegister = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');
    try {
      await onRegister(registerData.email, registerData.username, registerData.password);
      setSuccess('Registration successful! You can now log in.');
      setMode('login');
    } catch (err) {
      setError(err.response?.data?.detail || 'Registration failed');
    }
  };

  const renderInput = (type, placeholder, value, onChange, autoComplete = 'off') => (
    <div className="relative w-full">
      <input
        type={type}
        placeholder={placeholder}
        value={value}
        onChange={onChange}
        autoComplete={autoComplete}
        className={`w-full p-3 pl-4 rounded-lg border border-gray-300 dark:border-gray-600 
          bg-gray-50 dark:bg-gray-800 text-gray-900 dark:text-white 
          placeholder-gray-500 dark:placeholder-gray-400 focus:ring-2 
          focus:ring-blue-500 dark:focus:ring-blue-400 focus:border-transparent 
          transition-all duration-300 ${error ? 'border-red-500 dark:border-red-400' : ''}`}
        required
      />
    </div>
  );

  return (
    <div className={`w-full max-w-2xl mx-auto bg-white dark:bg-gray-900 rounded-xl 
      shadow-xl overflow-hidden flex flex-col md:flex-row transform 
      transition-all duration-500 ${isFlipping ? 'scale-95 opacity-90' : 'scale-100 opacity-100'}`}>
      {/* Toggle Panel */}
      <div className={`md:w-1/2 flex flex-col justify-center items-center p-8 
        bg-gradient-to-br from-blue-500 to-blue-700 dark:from-gray-800 dark:to-gray-700 
        text-white transform transition-all duration-500 
        ${isFlipping ? 'translate-y-2 md:translate-x-2' : 'translate-y-0 md:translate-x-0'}`}>
        <h2 className="text-3xl font-bold mb-2 text-center">
          {mode === 'login' ? 'Welcome Back!' : 'Join Us!'}
        </h2>
        <p className="mb-6 text-lg opacity-80 text-center">
          {mode === 'login' ? 'Sign in to your account' : 'Create a new account'}
        </p>
        <button
          onClick={handleToggle}
          disabled={loading}
          className="mt-4 px-6 py-2 bg-white/10 backdrop-blur-sm text-white font-semibold rounded-lg 
            shadow-lg hover:bg-white/20 transform transition-all duration-300 hover:scale-105 
            active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed">
          {mode === 'login' ? 'Need an account? Register' : 'Already have an account? Login'}
        </button>
      </div>

      {/* Form Panel */}
      <div className="md:w-1/2 p-8 flex flex-col justify-center">
        <form onSubmit={mode === 'login' ? handleLogin : handleRegister} 
          className="flex flex-col gap-4">
          {mode === 'register' && renderInput(
            'email',
            'Email',
            registerData.email,
            e => setRegisterData({ ...registerData, email: e.target.value }),
            'email'
          )}
          {renderInput(
            'text',
            'Username',
            mode === 'login' ? loginData.username : registerData.username,
            e => mode === 'login'
              ? setLoginData({ ...loginData, username: e.target.value })
              : setRegisterData({ ...registerData, username: e.target.value }),
            'username'
          )}
          {renderInput(
            'password',
            'Password',
            mode === 'login' ? loginData.password : registerData.password,
            e => mode === 'login'
              ? setLoginData({ ...loginData, password: e.target.value })
              : setRegisterData({ ...registerData, password: e.target.value }),
            'current-password'
          )}
          <button
            type="submit"
            disabled={loading}
            className="relative bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 
              rounded-lg transform transition-all duration-300 hover:shadow-lg active:scale-95 
              disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center">
            {loading && (
              <ArrowPathIcon className="animate-spin h-5 w-5 mr-2" />
            )}
            {loading ? 'Please wait...' : mode === 'login' ? 'Login' : 'Register'}
          </button>

          {error && (
            <div className="text-red-500 text-center p-2 bg-red-50 dark:bg-red-900/20 
              rounded-lg transition-all duration-300">
              {error}
            </div>
          )}
          {success && (
            <div className="text-green-600 dark:text-green-400 text-center p-2 bg-green-50 
              dark:bg-green-900/20 rounded-lg transition-all duration-300">
              {success}
            </div>
          )}
        </form>
      </div>
    </div>
  );
}