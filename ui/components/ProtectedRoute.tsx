'use client';

import { useRouter } from 'next/navigation';
import { useContext, useEffect } from 'react';

import AuthContext from '@/context/AuthContext';
import { LoadingScreen } from '@/components/ui/loading-screen';

const ProtectedRoute = ({ children }: { children: React.ReactNode }) => {
  const { user } = useContext(AuthContext);
  const router = useRouter();

  useEffect(() => {
    if (!user) router.push('/auth/login');
  }, [router, user]);

  return user ? (
    children
  ) : (
    <LoadingScreen message="Loading user dashboard..." />
  );
};

export default ProtectedRoute;
