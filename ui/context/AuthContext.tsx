'use client';

import axios, { AxiosError, AxiosResponse } from 'axios';
import { useRouter } from 'next/navigation';
import {
  createContext,
  useCallback,
  useEffect,
  useMemo,
  useState,
} from 'react';
import { z } from 'zod';

import { LoadingScreen } from '@/components/ui/loading-screen';
import { createUser, logInUser, logOutUser, whoAmI } from '@/lib/api';
import { User } from '@/models/User';
import { LoginSchema, RegisterSchema } from '@/schema';

type AuthContextType = {
  user: User | null;
  fetchUser: () => Promise<void>;
  login: (
    data: z.infer<typeof LoginSchema>
  ) => Promise<AxiosResponse | undefined>;
  logout: () => void;
  register: (
    data: z.infer<typeof RegisterSchema>
  ) => Promise<AxiosResponse | undefined>;
  isAdmin: () => boolean;
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
      const response = await whoAmI();

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

      return router.push('/dashboard');
    } catch (error) {
      setUser(null);
    }
  }, [router, user]);

  const register = useCallback(
    async (data: z.infer<typeof RegisterSchema>) => {
      try {
        await createUser(data);

        await fetchUser();
      } catch (error) {
        if (error instanceof AxiosError) {
          router.push(loginRoute);
          return error.response;
        }
      }
    },
    [fetchUser, router]
  );

  const login = useCallback(
    async (data: z.infer<typeof LoginSchema>) => {
      try {
        await logInUser(data);

        await fetchUser();
      } catch (error) {
        if (error instanceof AxiosError) {
          router.push(loginRoute);
          return error.response;
        }
      }
    },
    [fetchUser, router]
  );

  const logout = useCallback(async () => {
    try {
      await logOutUser();
    } finally {
      setUser(null);
      return router.push(loginRoute);
    }
  }, [router]);

  const isAdmin = useCallback(() => {
    return user?.admin || false;
  }, [user?.admin]);

  useEffect(() => {
    axios.defaults.baseURL = window.location.origin;
    const checkAuth = async () => {
      if (!user) await fetchUser();
      setIsReady(true);
    };
    checkAuth();
  }, [user, fetchUser]);

  return (
    <AuthContext.Provider
      value={{ user, fetchUser, isAdmin, login, logout, register }}
    >
      {isReady ? (
        children
      ) : (
        <LoadingScreen message="Loading Project Assignment Portal" />
      )}
    </AuthContext.Provider>
  );
};
export default AuthContext;
