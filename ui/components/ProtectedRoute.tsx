'use client';

import { useContext, useEffect, useState } from 'react';

import AuthContext from '@/app/context/AuthContext';
import { LoadingSpinner } from '@/components/ui/loading-spinner';

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
    <div className="min-h-screen flex flex-col items-center justify-center">
      <LoadingSpinner className="p-3 m-5" />
      <p className="text-base text-muted-foreground">
        Loading user dashboard...
      </p>
    </div>
  ) : (
    children
  );
};

export default ProtectedRoute;
