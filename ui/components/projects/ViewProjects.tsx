'use client';

import { AxiosError } from 'axios';
import { useRouter } from 'next/navigation';
import { useCallback, useEffect, useState } from 'react';

import { useToast } from '@/hooks/use-toast';
import { getProjects } from '@/lib/api';
import { ProjectWithUserResponse } from '@/models/Relations';
import Project from './project';
import { LoadingSpinner } from '../ui/loading-spinner';

const ViewProjects = () => {
  const [projects, setProjects] = useState<
    ProjectWithUserResponse[] | undefined
  >(undefined);
  const [isReady, setIsReady] = useState<boolean>(false);

  const { toast } = useToast();
  const router = useRouter();

  const fetchProjects = useCallback(
    async (users?: boolean) => {
      try {
        const response = await getProjects(users);

        setProjects(response.data);

        setIsReady(true);
      } catch (error) {
        if (error instanceof AxiosError) {
          if (error.response?.status === 401) {
            toast({
              title: 'Session Expired',
              description:
                'Your credentials have expired, you must log in again',
              variant: 'destructive',
            });
            setTimeout(() => {
              router.push('/auth/login');
            }, 3000);
          } else {
            toast({
              variant: 'destructive',
              title: 'Error Fetching Projects',
              description: error.message,
            });
          }
        }
      }
    },
    [router, toast]
  );

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
