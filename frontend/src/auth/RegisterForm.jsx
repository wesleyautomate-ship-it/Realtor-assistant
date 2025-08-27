import React, { useState } from 'react';
import { useAuth } from './AuthContext';

const RegisterForm = ({ onSwitchToLogin, selectedRole = 'client' }) => {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    confirmPassword: '',
    first_name: '',
    last_name: '',
    role: selectedRole
  });
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [errors, setErrors] = useState({});
  const [passwordStrength, setPasswordStrength] = useState(0);

  const { register, error, clearError } = useAuth();

  // Role display information
  const roleInfo = {
    client: { name: 'Client', icon: '👤', description: 'Property buyers, sellers, and investors' },
    agent: { name: 'Agent', icon: '🏠', description: 'Real estate agents and brokers' },
    employee: { name: 'Employee', icon: '👨‍💼', description: 'Company staff and employees' },
    admin: { name: 'Admin', icon: '⚙️', description: 'System administrators and managers' }
  };

  const currentRole = roleInfo[selectedRole] || roleInfo.client;

  const validatePassword = (password) => {
    let strength = 0;
    const checks = {
      length: password.length >= 8,
      uppercase: /[A-Z]/.test(password),
      lowercase: /[a-z]/.test(password),
      number: /\d/.test(password),
      special: /[!@#$%^&*(),.?":{}|<>]/.test(password)
    };

    Object.values(checks).forEach(check => {
      if (check) strength += 20;
    });

    return strength;
  };

  const getPasswordStrengthColor = (strength) => {
    if (strength <= 40) return '#f44336';
    if (strength <= 60) return '#ff9800';
    if (strength <= 80) return '#ffc107';
    return '#4caf50';
  };

  const getPasswordStrengthText = (strength) => {
    if (strength <= 40) return 'Weak';
    if (strength <= 60) return 'Fair';
    if (strength <= 80) return 'Good';
    return 'Strong';
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
    
    // Update password strength
    if (name === 'password') {
      setPasswordStrength(validatePassword(value));
    }
    
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

    if (!formData.first_name) {
      newErrors.first_name = 'First name is required';
    }

    if (!formData.last_name) {
      newErrors.last_name = 'Last name is required';
    }

    if (!formData.email) {
      newErrors.email = 'Email is required';
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      newErrors.email = 'Please enter a valid email address';
    }

    if (!formData.password) {
      newErrors.password = 'Password is required';
    } else if (formData.password.length < 8) {
      newErrors.password = 'Password must be at least 8 characters long';
    }

    if (!formData.confirmPassword) {
      newErrors.confirmPassword = 'Please confirm your password';
    } else if (formData.password !== formData.confirmPassword) {
      newErrors.confirmPassword = 'Passwords do not match';
    }

    if (!formData.role) {
      newErrors.role = 'Please select a role';
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
      const result = await register(formData);
      if (!result.success) {
        // Error is already set in the auth context
      }
    } catch (err) {
      console.error('Registration error:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleTogglePasswordVisibility = () => {
    setShowPassword(!showPassword);
  };

  const handleToggleConfirmPasswordVisibility = () => {
    setShowConfirmPassword(!showConfirmPassword);
  };

  return (
    <div className="auth-container">
      <div className="auth-card">
        <div className="text-center mb-8">
          <div className="w-16 h-16 bg-gradient-to-br from-primary-500 to-primary-300 rounded-full flex items-center justify-center text-3xl mx-auto mb-4">
            {currentRole.icon}
          </div>
          <h1 className="text-3xl font-bold bg-gradient-to-r from-primary-500 to-primary-300 bg-clip-text text-transparent">
            Create Account
          </h1>
          <p className="text-text-secondary mt-2">
            Join as {currentRole.name}
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
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label htmlFor="first_name" className="block text-sm font-medium text-text-secondary mb-2">
                First Name
              </label>
              <input
                type="text"
                id="first_name"
                name="first_name"
                value={formData.first_name}
                onChange={handleChange}
                className={`input w-full ${errors.first_name ? 'border-error-500' : ''}`}
                placeholder="Enter your first name"
                disabled={isLoading}
              />
              {errors.first_name && (
                <p className="mt-1 text-sm text-error-500">{errors.first_name}</p>
              )}
            </div>

            <div>
              <label htmlFor="last_name" className="block text-sm font-medium text-text-secondary mb-2">
                Last Name
              </label>
              <input
                type="text"
                id="last_name"
                name="last_name"
                value={formData.last_name}
                onChange={handleChange}
                className={`input w-full ${errors.last_name ? 'border-error-500' : ''}`}
                placeholder="Enter your last name"
                disabled={isLoading}
              />
              {errors.last_name && (
                <p className="mt-1 text-sm text-error-500">{errors.last_name}</p>
              )}
            </div>
          </div>

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
            <label htmlFor="role" className="block text-sm font-medium text-text-secondary mb-2">
              Role
            </label>
            <select
              id="role"
              name="role"
              value={formData.role}
              onChange={handleChange}
              className={`input w-full ${errors.role ? 'border-error-500' : ''}`}
              disabled={true}
            >
              <option value="client">Client</option>
              <option value="agent">Real Estate Agent</option>
              <option value="employee">Employee</option>
              <option value="admin">Administrator</option>
            </select>
            <p className="mt-1 text-xs text-text-tertiary">
              Role is pre-selected based on your choice
            </p>
            {errors.role && (
              <p className="mt-1 text-sm text-error-500">{errors.role}</p>
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
            {formData.password && (
              <div className="mt-2">
                <div className="flex items-center justify-between mb-1">
                  <span className="text-xs text-text-secondary">Password strength:</span>
                  <span className="text-xs font-medium" style={{ color: getPasswordStrengthColor(passwordStrength) }}>
                    {getPasswordStrengthText(passwordStrength)}
                  </span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-1">
                  <div
                    className="h-1 rounded-full transition-all duration-300"
                    style={{
                      width: `${passwordStrength}%`,
                      backgroundColor: getPasswordStrengthColor(passwordStrength)
                    }}
                  ></div>
                </div>
              </div>
            )}
            {errors.password && (
              <p className="mt-1 text-sm text-error-500">{errors.password}</p>
            )}
          </div>

          <div>
            <label htmlFor="confirmPassword" className="block text-sm font-medium text-text-secondary mb-2">
              Confirm Password
            </label>
            <div className="relative">
              <input
                type={showConfirmPassword ? 'text' : 'password'}
                id="confirmPassword"
                name="confirmPassword"
                value={formData.confirmPassword}
                onChange={handleChange}
                className={`input w-full pl-10 pr-10 ${errors.confirmPassword ? 'border-error-500' : ''}`}
                placeholder="Confirm your password"
                disabled={isLoading}
              />
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <span className="text-text-tertiary">🔒</span>
              </div>
              <button
                type="button"
                onClick={handleToggleConfirmPasswordVisibility}
                className="absolute inset-y-0 right-0 pr-3 flex items-center text-text-tertiary hover:text-text-secondary"
                disabled={isLoading}
              >
                {showConfirmPassword ? '🙈' : '👁️'}
              </button>
            </div>
            {errors.confirmPassword && (
              <p className="mt-1 text-sm text-error-500">{errors.confirmPassword}</p>
            )}
          </div>

          <div className="flex items-center">
            <input
              type="checkbox"
              id="terms"
              className="w-4 h-4 text-primary-500 bg-surface border-border rounded focus:ring-primary-500"
              required
            />
            <label htmlFor="terms" className="ml-2 text-sm text-text-secondary">
              I agree to the{' '}
              <button type="button" className="text-primary-500 hover:text-primary-400 transition-colors">
                Terms of Service
              </button>{' '}
              and{' '}
              <button type="button" className="text-primary-500 hover:text-primary-400 transition-colors">
                Privacy Policy
              </button>
            </label>
          </div>

          <button
            type="submit"
            disabled={isLoading}
            className="btn btn-primary w-full"
          >
            {isLoading ? (
              <div className="flex items-center gap-2">
                <div className="w-4 h-4 border-2 border-current border-t-transparent rounded-full animate-spin"></div>
                Creating account...
              </div>
            ) : (
              'Create Account'
            )}
          </button>
        </form>

        <div className="mt-8 text-center">
          <p className="text-text-secondary">
            Already have an account?{' '}
            <button
              onClick={onSwitchToLogin}
              className="text-primary-500 hover:text-primary-400 transition-colors font-medium"
              disabled={isLoading}
            >
              Sign in here
            </button>
          </p>
        </div>

        <div className="mt-6 pt-6 border-t border-border">
          <div className="text-center">
            <p className="text-xs text-text-tertiary mb-3">
              Secure registration powered by Dubai Real Estate AI
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

export default RegisterForm;
