import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '../ui/card';
import { CircleXIcon } from 'lucide-react';
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
import { deleteProject } from '@/lib/api';
import { useState } from 'react';
import { useToast } from '@/hooks/use-toast';
import { AxiosError } from 'axios';
import { ProjectResponse } from '@/models/Project';
import { ProjectWithUserResponse } from '@/models/Relations';

interface CustomerProps {
  project: ProjectResponse | ProjectWithUserResponse;
  handleRefresh: () => void;
}

const Project = ({ project, handleRefresh }: CustomerProps) => {
  const [isReady, setIsReady] = useState<boolean>(true);
  const { toast } = useToast();

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
        toast({
          variant: 'destructive',
          title: 'Error Deleting Project',
          description: error.message,
        });
      }
    }
  };
  return (
    <Card className="m-4">
      <CardHeader>
        <div className="flex justify-between items-center">
          <CardTitle>{project.name}</CardTitle>
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
        <CardDescription>Customer: {project.customer.name}</CardDescription>
      </CardHeader>

      <CardContent>
        {isReady ? project.details : 'Deleting project...'}
      </CardContent>
    </Card>
  );
};

export default Project;
