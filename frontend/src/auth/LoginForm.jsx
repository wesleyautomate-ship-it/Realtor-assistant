import React, { useState } from 'react';
import { useAuth } from './AuthContext';

const LoginForm = ({ onSwitchToRegister, onSwitchToForgotPassword, selectedRole = 'client' }) => {
  const [formData, setFormData] = useState({
    email: '',
    password: ''
  });
  const [showPassword, setShowPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [errors, setErrors] = useState({});

  const { login, error, clearError } = useAuth();

  // Role display information
  const roleInfo = {
    client: { name: 'Client', icon: '👤', description: 'Property buyers, sellers, and investors' },
    agent: { name: 'Agent', icon: '🏠', description: 'Real estate agents and brokers' },
    employee: { name: 'Employee', icon: '👨‍💼', description: 'Company staff and employees' },
    admin: { name: 'Admin', icon: '⚙️', description: 'System administrators and managers' }
  };

  const currentRole = roleInfo[selectedRole] || roleInfo.client;

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
    
    // Clear field error when user starts typing
    if (errors[name]) {
      setErrors(prev => ({
        ...prev,
        [name]: ''
      }));
    }
    
    // Clear auth error when user starts typing
    if (error) {
      clearError();
    }
  };

  const validateForm = () => {
    const newErrors = {};

    if (!formData.email) {
      newErrors.email = 'Email is required';
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      newErrors.email = 'Please enter a valid email address';
    }

    if (!formData.password) {
      newErrors.password = 'Password is required';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!validateForm()) {
      return;
    }

    setIsLoading(true);
    
    try {
      const result = await login(formData.email, formData.password);
      if (!result.success) {
        // Error is already set in the auth context
      }
    } catch (err) {
      console.error('Login error:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleTogglePasswordVisibility = () => {
    setShowPassword(!showPassword);
  };

  return (
    <div className="auth-container">
      <div className="auth-card">
        <div className="text-center mb-8">
          <div className="w-16 h-16 bg-gradient-to-br from-primary-500 to-primary-300 rounded-full flex items-center justify-center text-3xl mx-auto mb-4">
            {currentRole.icon}
          </div>
          <h1 className="text-3xl font-bold bg-gradient-to-r from-primary-500 to-primary-300 bg-clip-text text-transparent">
            Welcome Back
          </h1>
          <p className="text-text-secondary mt-2">
            Sign in as {currentRole.name}
          </p>
          <p className="text-text-tertiary text-sm mt-1">
            {currentRole.description}
          </p>
        </div>

        {error && (
          <div className="mb-6 p-4 bg-error-100 border border-error-300 rounded-lg">
            <div className="flex items-center gap-2 text-error-800">
              <span>⚠️</span>
              <span className="text-sm">{error}</span>
            </div>
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label htmlFor="email" className="block text-sm font-medium text-text-secondary mb-2">
              Email Address
            </label>
            <div className="relative">
              <input
                type="email"
                id="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                className={`input w-full pl-10 ${errors.email ? 'border-error-500' : ''}`}
                placeholder="Enter your email"
                disabled={isLoading}
              />
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <span className="text-text-tertiary">📧</span>
              </div>
            </div>
            {errors.email && (
              <p className="mt-1 text-sm text-error-500">{errors.email}</p>
            )}
          </div>

          <div>
            <label htmlFor="password" className="block text-sm font-medium text-text-secondary mb-2">
              Password
            </label>
            <div className="relative">
              <input
                type={showPassword ? 'text' : 'password'}
                id="password"
                name="password"
                value={formData.password}
                onChange={handleChange}
                className={`input w-full pl-10 pr-10 ${errors.password ? 'border-error-500' : ''}`}
                placeholder="Enter your password"
                disabled={isLoading}
              />
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <span className="text-text-tertiary">🔒</span>
              </div>
              <button
                type="button"
                onClick={handleTogglePasswordVisibility}
                className="absolute inset-y-0 right-0 pr-3 flex items-center text-text-tertiary hover:text-text-secondary"
                disabled={isLoading}
              >
                {showPassword ? '🙈' : '👁️'}
              </button>
            </div>
            {errors.password && (
              <p className="mt-1 text-sm text-error-500">{errors.password}</p>
            )}
          </div>

          <div className="flex items-center justify-between">
            <label className="flex items-center">
              <input
                type="checkbox"
                className="w-4 h-4 text-primary-500 bg-surface border-border rounded focus:ring-primary-500"
              />
              <span className="ml-2 text-sm text-text-secondary">Remember me</span>
            </label>
            <button
              type="button"
              onClick={onSwitchToForgotPassword}
              className="text-sm text-primary-500 hover:text-primary-400 transition-colors"
              disabled={isLoading}
            >
              Forgot password?
            </button>
          </div>

          <button
            type="submit"
            disabled={isLoading}
            className="btn btn-primary w-full"
          >
            {isLoading ? (
              <div className="flex items-center gap-2">
                <div className="w-4 h-4 border-2 border-current border-t-transparent rounded-full animate-spin"></div>
                Signing in...
              </div>
            ) : (
              'Sign In'
            )}
          </button>
        </form>

        <div className="mt-8 text-center">
          <p className="text-text-secondary">
            Don't have an account?{' '}
            <button
              onClick={onSwitchToRegister}
              className="text-primary-500 hover:text-primary-400 transition-colors font-medium"
              disabled={isLoading}
            >
              Sign up here
            </button>
          </p>
        </div>

        <div className="mt-6 pt-6 border-t border-border">
          <div className="text-center">
            <p className="text-xs text-text-tertiary mb-3">
              Secure login powered by Dubai Real Estate AI
            </p>
            <div className="flex items-center justify-center gap-2 text-xs text-text-tertiary">
              <span>🔒</span>
              <span>256-bit encryption</span>
              <span>•</span>
              <span>GDPR compliant</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LoginForm;
