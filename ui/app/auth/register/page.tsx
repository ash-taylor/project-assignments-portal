'use client';

import RegisterForm from '@/components/auth/register-form';
import AuthContext from '@/context/AuthContext';
import { useRouter } from 'next/navigation';
import { useContext, useEffect, useState } from 'react';

const RegisterPage = () => {
  const { user } = useContext(AuthContext);
  const [isReady, setIsReady] = useState<boolean>(false);
  const router = useRouter();

  useEffect(() => {
    if (user) return router.push('/dashboard');

    setIsReady(true);
  }, [router, user]);

  return isReady && <RegisterForm />;
};

export default RegisterPage;
