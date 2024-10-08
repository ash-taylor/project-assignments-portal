'use client';

import { AxiosError } from 'axios';
import { useCallback, useContext, useEffect, useState } from 'react';

import AuthContext from '@/context/AuthContext';
import { useToast } from '@/hooks/use-toast';
import { getUsers } from '@/lib/api';
import { UserWithProjectResponse } from '@/models/Relations';
import { LoadingSpinner } from '../ui/loading-spinner';
import User from './user';

const ViewUsers = () => {
  const [users, setUsers] = useState<UserWithProjectResponse[] | undefined>(
    undefined
  );
  const [isReady, setIsReady] = useState<boolean>(false);

  const { isAdmin, logout } = useContext(AuthContext);
  const { toast } = useToast();

  const fetchUsers = useCallback(async () => {
    try {
      if (!isAdmin())
        return toast({
          variant: 'destructive',
          title: 'Error Fetching Users',
          description: 'You must have admin rights to perform this action',
        });
      const response = await getUsers(true);

      setUsers(response.data);

      setIsReady(true);
    } catch (error) {
      if (error instanceof AxiosError) {
        if (error.response?.status === 401) {
          toast({
            title: 'Session Expired',
            description: 'Your credentials have expired, you must log in again',
            variant: 'destructive',
          });
          setTimeout(() => {
            return logout();
          }, 2000);
        } else if (error.response?.status === 403) {
          toast({
            variant: 'destructive',
            title: 'Error Fetching Users',
            description: 'You must have admin rights to perform this action',
          });
        } else {
          toast({
            variant: 'destructive',
            title: 'Error Fetching Users',
            description: error.message,
          });
        }
      }
    }
  }, [isAdmin, logout, toast]);

  const handleRefresh = () => {
    setUsers(undefined);
    setIsReady(false);
    fetchUsers();
  };

  useEffect(() => {
    fetchUsers();
  }, [fetchUsers]);

  return (
    <>
      {isReady ? (
        users?.map((user, idx) => (
          <User key={idx} member={user} handleRefresh={handleRefresh} />
        ))
      ) : (
        <div className="flex items-center justify-center h-full w-full">
          <LoadingSpinner message="Loading team..." />
        </div>
      )}
    </>
  );
};
export default ViewUsers;
