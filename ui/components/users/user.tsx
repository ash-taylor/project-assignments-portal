import { AxiosError } from 'axios';
import { CircleXIcon } from 'lucide-react';
import { useContext, useState } from 'react';

import AuthContext from '@/context/AuthContext';
import { useToast } from '@/hooks/use-toast';
import { deleteUser } from '@/lib/api';
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
import { LoadingSpinner } from '../ui/loading-spinner';

interface UserProps {
  member: UserWithProjectResponse;
  handleRefresh: () => void;
}

const User = ({ member, handleRefresh }: UserProps) => {
  const [isDeleting, setIsDeleting] = useState<boolean>(false);

  const { toast } = useToast();

  const { user, logout } = useContext(AuthContext);

  const handleDelete = async () => {
    try {
      setIsDeleting(true);

      await deleteUser(member.id);

      toast({
        title: 'Success',
        description: `${member.user_name} deleted${
          user?.id === member.id ? '. You will now be logged out.' : ''
        }`,
      });

      if (user?.id === member.id) {
        setTimeout(() => {
          return logout();
        }, 2000);
      }

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

    if (member.project) {
      projectDetails = (
        <div className="flex justify-between items-center">
          <div>
            <p className="text-base">Project Name: {member.project.name}</p>
          </div>
          {member.project.details &&
            `Project Details: ${member.project.details}`}
          <div>
            <p className="text-base">Project Status: {member.project.status}</p>
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
            {member.first_name} {member.last_name}
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
                    {user?.id === member.id
                      ? 'Deleting your own account will log you out. This action cannot be undone. You will be permanently deleted from the system.'
                      : `This action cannot be undone. This will permanently delete
                    user: ${member.first_name} ${member.last_name}.`}
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
        <CardDescription>Username: {member.user_name}</CardDescription>
        <CardDescription>Role: {member.role}</CardDescription>
        <CardDescription>Email: {member.email}</CardDescription>
      </CardHeader>

      <CardContent>{renderContent()}</CardContent>
    </Card>
  );
};

export default User;
