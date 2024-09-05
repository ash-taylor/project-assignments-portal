'use client';

import { useContext } from 'react';

import AuthContext from '@/app/context/AuthContext';
import ProtectedRoute from '@/components/ProtectedRoute';

export default function Home() {
  const { user } = useContext(AuthContext);

  return (
    <main className="flex min-h-screen flex-col items-center justify-between">
      <ProtectedRoute>
        <div className="h-full flex-col justify-center">
          Hello World - {user ? `${user.username} is logged in` : 'Loading...'}
        </div>
      </ProtectedRoute>
    </main>
  );
}
