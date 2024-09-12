import { AxiosError } from 'axios';
import { CircleXIcon, PencilIcon, UserPlus2Icon } from 'lucide-react';
import { SelectGroup } from '@radix-ui/react-select';
import { useContext, useState } from 'react';

import AuthContext from '@/context/AuthContext';
import { useToast } from '@/hooks/use-toast';
import {
  assignProjectToUser,
  deleteProject,
  deleteUser,
  getUsers,
  unassignProjectFromUser,
} from '@/lib/api';
import { ProjectResponse, ProjectStatus } from '@/models/Project';
import { UserRole } from '@/models/User';
import { UserWithProjectResponse } from '@/models/Relations';

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
import { Button } from '../ui/button';
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
import { LoadingSpinner } from '../ui/loading-spinner';
import { ScrollArea } from '../ui/scroll-area';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectLabel,
  SelectTrigger,
  SelectValue,
} from '../ui/select';
import { Separator } from '../ui/separator';

interface UserProps {
  user: UserWithProjectResponse;
  handleRefresh: () => void;
}

const User = ({ user, handleRefresh }: UserProps) => {
  const [isDeleting, setIsDeleting] = useState<boolean>(false);

  const { toast } = useToast();

  const { logout } = useContext(AuthContext);

  const handleDelete = async () => {
    try {
      setIsDeleting(true);

      await deleteUser(user.id);

      toast({
        title: 'Success',
        description: `${user.user_name} deleted`,
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
            return logout();
          }, 2000);
        } else {
          toast({
            variant: 'destructive',
            title: 'Error Deleting User',
            description: error.message,
          });
        }
      }
    }
  };

  const renderContent = () => {
    let projectDetails = null;

    if (user.project) {
      projectDetails = (
        <div className="flex justify-between items-center">
          <div>
            <p className="text-base">Project Name: {user.project.name}</p>
          </div>
          {user.project.details && `Project Details: ${user.project.details}`}
          <div>
            <p className="text-base">Project Status: {user.project.status}</p>
          </div>
        </div>
      );
    }

    return (
      <div>
        {projectDetails
          ? projectDetails
          : 'User not currently assigned to any project'}
      </div>
    );
  };

  return (
    <Card className="m-4">
      <CardHeader>
        <div className="flex justify-between items-center">
          <CardTitle>
            {user.first_name} {user.last_name}
          </CardTitle>
          <div className="flex gap-2">
            <AlertDialog>
              <AlertDialogTrigger>
                <Button variant="destructive" size="icon" disabled={isDeleting}>
                  {isDeleting ? <LoadingSpinner /> : <CircleXIcon />}
                </Button>
              </AlertDialogTrigger>
              <AlertDialogContent>
                <AlertDialogHeader>
                  <AlertDialogTitle>Are you sure?</AlertDialogTitle>
                  <AlertDialogDescription>
                    This action cannot be undone. This will permanently delete
                    user: {user.first_name} {user.last_name}.
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
        <CardDescription>Username: {user.user_name}</CardDescription>
        <CardDescription>Role: {user.role}</CardDescription>
        <CardDescription>Email: {user.email}</CardDescription>
      </CardHeader>

      <CardContent>{renderContent()}</CardContent>
    </Card>
  );
};

export default User;
