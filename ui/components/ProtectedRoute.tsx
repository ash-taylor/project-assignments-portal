'use client';

import { useContext, useEffect } from 'react';

import AuthContext from '@/app/context/AuthContext';
import { LoadingScreen } from './ui/loading-screen';
import { useRouter } from 'next/navigation';

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
