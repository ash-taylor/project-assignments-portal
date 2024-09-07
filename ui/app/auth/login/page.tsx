'use client';

import { useRouter } from 'next/navigation';
import { useContext, useEffect, useState } from 'react';

import LoginForm from '@/components/auth/login-form';
import AuthContext from '@/context/AuthContext';

const LoginPage = () => {
  const { user } = useContext(AuthContext);
  const [isReady, setIsReady] = useState(false);
  const router = useRouter();

  useEffect(() => {
    if (user) return router.push('/dashboard');

    setIsReady(true);
  }, [router, user]);

  return isReady && <LoginForm />;
};

export default LoginPage;
