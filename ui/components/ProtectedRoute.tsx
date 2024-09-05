'use client';

import { useContext, useEffect, useState } from 'react';

import AuthContext from '@/app/context/AuthContext';
import { LoadingSpinner } from '@/components/ui/loading-spinner';
import { LoadingScreen } from './ui/loading-screen';

const ProtectedRoute = ({ children }: { children: React.ReactNode }) => {
  const { user, fetchUser } = useContext(AuthContext);
  const [isLoading, setIsLoading] = useState<boolean>(true);

  useEffect(() => {
    const checkAuth = async () => {
      setIsLoading(true);
      if (!user) {
        try {
          await fetchUser();
        } catch (error) {
          console.error('Error fetching user:', error);
        }
      }
      setIsLoading(false);
    };

    checkAuth();
  }, [fetchUser, user]);

  return isLoading ? (
    <LoadingScreen message="Loading user dashboard..." />
  ) : (
    children
  );
};

export default ProtectedRoute;
