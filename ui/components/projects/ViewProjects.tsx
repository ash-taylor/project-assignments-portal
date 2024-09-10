'use client';

import { AxiosError } from 'axios';
import { useCallback, useContext, useEffect, useState } from 'react';

import { useToast } from '@/hooks/use-toast';
import { getProjects } from '@/lib/api';
import { ProjectWithUserResponse } from '@/models/Relations';
import Project from './project';
import { LoadingSpinner } from '../ui/loading-spinner';
import AuthContext from '@/context/AuthContext';

const ViewProjects = () => {
  const [projects, setProjects] = useState<
    ProjectWithUserResponse[] | undefined
  >(undefined);
  const [isReady, setIsReady] = useState<boolean>(false);

  const { toast } = useToast();
  const { logout } = useContext(AuthContext);

  const fetchProjects = useCallback(async () => {
    try {
      const response = await getProjects(true);

      setProjects(response.data);

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
        } else {
          toast({
            variant: 'destructive',
            title: 'Error Fetching Projects',
            description: error.message,
          });
        }
      }
    }
  }, [logout, toast]);

  const handleRefresh = () => {
    setProjects(undefined);
    setIsReady(false);
    fetchProjects();
  };

  useEffect(() => {
    fetchProjects();
  }, [fetchProjects]);

  return (
    <>
      {isReady ? (
        projects?.map((project, idx) => (
          <Project key={idx} project={project} handleRefresh={handleRefresh} />
        ))
      ) : (
        <div className="flex items-center justify-center h-full w-full">
          <LoadingSpinner message="Loading projects..." />
        </div>
      )}
    </>
  );
};
export default ViewProjects;
