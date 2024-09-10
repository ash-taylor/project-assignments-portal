import { AxiosError } from 'axios';
import { CircleXIcon, PencilIcon } from 'lucide-react';
import { useRouter } from 'next/navigation';
import { useState } from 'react';

import { useToast } from '@/hooks/use-toast';
import { deleteProject } from '@/lib/api';
import { ProjectResponse, ProjectStatus } from '@/models/Project';
import { ProjectWithUserResponse } from '@/models/Relations';
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogTrigger,
} from '../ui/alert-dialog';
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '../ui/card';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '../ui/dialog';
import ProjectForm from './project-form';

interface CustomerProps {
  project: ProjectResponse | ProjectWithUserResponse;
  handleRefresh: () => void;
}

const Project = ({ project, handleRefresh }: CustomerProps) => {
  const [isReady, setIsReady] = useState<boolean>(true);

  const { toast } = useToast();
  const router = useRouter();

  const handleDelete = async () => {
    try {
      setIsReady(false);
      await deleteProject(project.id);
      toast({
        title: 'Success',
        description: `${project.name} deleted`,
      });
      handleRefresh();
    } catch (error) {
      if (error instanceof AxiosError) {
        if (error.response?.status === 401) {
          toast({
            title: 'Session Expired',
            description: 'Your credentials have expired, you must log in again',
            variant: 'destructive',
          });
          setTimeout(() => {
            return router.push('/auth/login');
          }, 3000);
        } else {
          toast({
            variant: 'destructive',
            title: 'Error Deleting Project',
            description: error.message,
          });
        }
      }
    }
  };
  return (
    <Card className="m-4">
      <CardHeader>
        <div className="flex justify-between items-center">
          <CardTitle>{project.name}</CardTitle>
          <div className="flex gap-2">
            <Dialog>
              <DialogTrigger>
                <PencilIcon />
              </DialogTrigger>
              <DialogContent>
                <DialogHeader>
                  <DialogTitle>Edit Project</DialogTitle>
                  <DialogDescription>
                    Make changes to the project here
                  </DialogDescription>
                </DialogHeader>
                <ProjectForm
                  formType="edit"
                  projectId={project.id}
                  projectName={project.name}
                  projectStatus={project.status as ProjectStatus}
                  projectDetails={project.details}
                  customerId={project.customer.id}
                  handleRefresh={handleRefresh}
                />
              </DialogContent>
            </Dialog>
            <AlertDialog>
              <AlertDialogTrigger>
                <CircleXIcon />
              </AlertDialogTrigger>
              <AlertDialogContent>
                <AlertDialogHeader>
                  <AlertDialogTitle>Are you sure?</AlertDialogTitle>
                  <AlertDialogDescription>
                    This action cannot be undone. This will permanently delete
                    {project.name}.
                  </AlertDialogDescription>
                </AlertDialogHeader>
                <AlertDialogFooter>
                  <AlertDialogCancel>Cancel</AlertDialogCancel>
                  <AlertDialogAction onClick={handleDelete}>
                    Continue
                  </AlertDialogAction>
                </AlertDialogFooter>
              </AlertDialogContent>
            </AlertDialog>
          </div>
        </div>
        <CardDescription>Customer: {project.customer.name}</CardDescription>
        <CardDescription>Status: {project.status}</CardDescription>
      </CardHeader>

      <CardContent>
        {isReady
          ? project.details || 'No project details exist'
          : 'Deleting project...'}
      </CardContent>
    </Card>
  );
};

export default Project;
