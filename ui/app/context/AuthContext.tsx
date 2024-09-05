'use client';

import { useRouter } from 'next/navigation';
import {
  createContext,
  useCallback,
  useEffect,
  useMemo,
  useState,
} from 'react';
import axios from 'axios';
import { User, UserResponse } from '@/app/models/User';
import { z } from 'zod';
import { LoginSchema, RegisterSchema } from '@/schema';
import { LoadingScreen } from '@/components/ui/loading-screen';

interface LoginResponse {
  access_token: string;
  token_type: 'Bearer';
}

type AuthContextType = {
  user: User | null;
  fetchUser: () => Promise<void>;
  login: (data: z.infer<typeof LoginSchema>) => Promise<void>;
  logout: () => void;
  register: (data: z.infer<typeof RegisterSchema>) => Promise<void>;
};

const loginRoute = '/auth/login';

const AuthContext = createContext<AuthContextType>({} as AuthContextType);

export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
  const [isReady, setIsReady] = useState<boolean>(false);
  const [user_, setUser] = useState<User | null>(null);
  const user = useMemo(() => user_, [user_]);
  const router = useRouter();

  const fetchUser = useCallback(async () => {
    try {
      const response = await axios.get<UserResponse>('api/users/me', {
        withCredentials: true,
      });

      if (response.status !== 200) {
        setUser(null);
        router.push(loginRoute);
      }

      const fetchedUser = new User(
        response.data.active,
        response.data.id,
        response.data.user_name,
        response.data.first_name,
        response.data.last_name,
        response.data.admin,
        response.data.role,
        response.data.email,
        response.data.project_id,
        response.data.project
      );

      if (JSON.stringify(user) !== JSON.stringify(fetchedUser))
        setUser(fetchedUser);

      router.push('/');
    } catch (error) {
      console.error('failed to fetch user', user);
      router.push(loginRoute);
    }
  }, [router, user]);

  const register = useCallback(
    async (data: z.infer<typeof RegisterSchema>) => {
      try {
        const body = JSON.stringify(data);
        const response = await axios.post<LoginResponse>('/api/user', body, {
          headers: { 'Content-Type': 'application/json' },
        });

        if (response.status !== 200) {
          console.error('Unable to create user', response);
          router.push(loginRoute);
          return;
        }

        router.push('/');
      } catch (error) {
        console.error('Create user failed', error);
        router.push(loginRoute);
      }
    },
    [router]
  );

  const login = useCallback(
    async (data: z.infer<typeof LoginSchema>) => {
      try {
        const response = await axios.post('/api/login', data, {
          headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        });

        if (response.status === 401) return router.push(loginRoute);

        router.push('/');
      } catch (error) {
        console.error('Login Failed', error);
        setUser(null);
      }
    },
    [router]
  );

  const logout = useCallback(async () => {
    try {
      await axios.post('/api/logout');
      setUser(null);
      router.push(loginRoute);
    } catch (error) {
      console.error('Logout failed', error);
    }
  }, [router]);

  useEffect(() => {
    const checkAuth = async () => {
      if (!user) await fetchUser();
      setIsReady(true);
    };

    checkAuth();
  }, [user, fetchUser]);

  return (
    <AuthContext.Provider value={{ user, fetchUser, login, logout, register }}>
      {isReady ? (
        children
      ) : (
        <LoadingScreen message="Loading Project Assignment Portal" />
      )}
    </AuthContext.Provider>
  );
};

export default AuthContext;
