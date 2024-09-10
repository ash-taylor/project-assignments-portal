'use client';

import { useToast } from '@/hooks/use-toast';
import { getProjects } from '@/lib/api';
import { ProjectWithUserResponse } from '@/models/Relations';
import { AxiosError } from 'axios';
import { useCallback, useEffect, useState } from 'react';
import { LoadingSpinner } from '../ui/loading-spinner';
import Project from './project';

const ViewProjects = () => {
  const [projects, setProjects] = useState<
    ProjectWithUserResponse[] | undefined
  >(undefined);
  const [isReady, setIsReady] = useState<boolean>(false);
  const { toast } = useToast();

  const fetchProjects = useCallback(
    async (users?: boolean) => {
      try {
        const response = await getProjects(users);

        setProjects(response.data);

        setIsReady(true);
      } catch (error) {
        if (error instanceof AxiosError) {
          toast({
            variant: 'destructive',
            title: 'Error Fetching Projects',
            description: error.message,
          });
        }
      }
    },
    [toast]
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
