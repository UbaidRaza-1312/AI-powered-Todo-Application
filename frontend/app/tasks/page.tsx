// app/tasks/page.tsx
'use client';

import React, { useState, useEffect } from 'react';
import TaskList from '../../src/components/TaskManager/TaskList';
import UserService from '../../src/services/userService';

const TasksPage = () => {
  const [userData, setUserData] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchUserData = async () => {
      try {
        const userProfile = await UserService.getUserProfileWithStats();
        setUserData(userProfile);
      } catch (error) {
        console.error('Error fetching user data:', error);
        // Remove invalid token from both localStorage and cookies
        if (typeof window !== 'undefined') {
          localStorage.removeItem('access_token');
          document.cookie = 'access_token=; path=/; expires=Thu, 01 Jan 1970 00:00:01 GMT;';
        }
        window.location.href = '/auth/login';
      } finally {
        setLoading(false);
      }
    };

    fetchUserData();
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-900 via-purple-900 to-violet-900">
        <div className="text-2xl font-semibold text-white">Loading...</div>
      </div>
    );
  }

  if (!userData) {
    return null; // Redirect is happening in useEffect
  }

  return <TaskList userData={userData} />;
};

export default TasksPage;