// frontend/app/navbar.tsx

'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { useEffect, useState } from 'react';
import AuthService from '../src/services/authService';

export default function Navbar() {
  const pathname = usePathname();
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [checkedAuth, setCheckedAuth] = useState(false);

  useEffect(() => {
    // Check if user is logged in by checking for token in localStorage
    const token = localStorage.getItem('access_token');
    setIsLoggedIn(!!token);
    setCheckedAuth(true);
  }, [pathname]); // Re-check when pathname changes

  const handleLogout = async () => {
    try {
      await AuthService.logout();
      window.location.href = '/';
    } catch (error) {
      console.error('Logout error:', error);
      // Fallback to manual token removal if service fails
      localStorage.removeItem('access_token');
      document.cookie = 'access_token=; path=/; expires=Thu, 01 Jan 1970 00:00:01 GMT;';
      window.location.href = '/';
    }
  };

  return (
    <nav className="bg-gradient-to-br from-gray-900  to-violet-900 backdrop-blur-md text-white shadow-lg border-b border-gray-700/50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <Link href="/" className="text-xl font-bold text-white">
              Todo App
            </Link>
          </div>
          <div className="flex items-center">
            <div className="ml-4 flex space-x-4">
              {!checkedAuth ? (
                // Placeholder to maintain layout during hydration
                <div className="px-3 py-2 rounded-md text-sm font-medium text-gray-300">
                  Loading...
                </div>
              ) : isLoggedIn ? (
                <>
                  <Link
                    href="/tasks"
                    className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                      pathname === '/tasks'
                        ? 'bg-gray-700/50 text-white'
                        : 'text-gray-300 hover:bg-gray-700/50 hover:text-white'
                    }`}
                  >
                    Tasks
                  </Link>
                </>
              ) : (
                <>
                  <Link
                    href="/auth/login"
                    className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                      pathname === '/auth/login'
                        ? 'bg-gray-700/50 text-white'
                        : 'text-gray-300 hover:bg-gray-700/50 hover:text-white'
                    }`}
                  >
                    Login
                  </Link>
                  <Link
                    href="/auth/register"
                    className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                      pathname === '/auth/register'
                        ? 'bg-gray-700/50 text-white'
                        : 'text-gray-300 hover:bg-gray-700/50 hover:text-white'
                    }`}
                  >
                    Register
                  </Link>
                </>
              )}
            </div>
            {checkedAuth && isLoggedIn && (
              <button
                onClick={handleLogout}
                className="ml-4 px-3 py-2 rounded-md text-sm font-medium text-gray-300 hover:bg-gray-700/50 hover:text-white transition-colors"
              >
                Logout
              </button>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
}