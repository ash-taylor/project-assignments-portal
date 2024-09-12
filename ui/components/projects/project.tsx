import { AxiosError } from 'axios';
import { CircleXIcon, PencilIcon, UserPlus2Icon } from 'lucide-react';
import { SelectGroup } from '@radix-ui/react-select';
import { useContext, useState } from 'react';

import AuthContext from '@/context/AuthContext';
import { useToast } from '@/hooks/use-toast';
import {
  assignProjectToUser,
  deleteProject,
  getUsers,
  unassignProjectFromUser,
} from '@/lib/api';
import { ProjectResponse, ProjectStatus } from '@/models/Project';
import { UserRole } from '@/models/User';
import {
  ProjectWithUserResponse,
  UserWithProjectResponse,
} from '@/models/Relations';
import ProjectForm from './project-form';
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
import {
  HoverCard,
  HoverCardContent,
  HoverCardTrigger,
} from '../ui/hover-card';

interface ProjectProps {
  project: ProjectResponse | ProjectWithUserResponse;
  handleRefresh: () => void;
}

const Project = ({ project, handleRefresh }: ProjectProps) => {
  const [isReady, setIsReady] = useState<boolean>(true);
  const [isDeleting, setIsDeleting] = useState<boolean>(false);
  const [users, setUsers] = useState<UserWithProjectResponse[]>();
  const [selectedUserId, setSelectedUserId] = useState<string | undefined>();
  const [usersLoaded, setUsersLoaded] = useState<boolean>(false);
  const [assigningUser, setAssigningUser] = useState<boolean>(false);

  const { isAdmin, logout } = useContext(AuthContext);
  const { toast } = useToast();

  const handleOpenUserAssign = async () => {
    try {
      setSelectedUserId(undefined);
      setUsersLoaded(false);

      const response = await getUsers(true);

      setUsers(response.data);

      setUsersLoaded(true);
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
            title: 'Error Fetching Users',
            description: 'You must have admin rights to perform this action',
            variant: 'destructive',
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
  };

  const handleDelete = async () => {
    try {
      setIsReady(false);
      setIsDeleting(true);

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
            return logout();
          }, 2000);
        } else if (error.response?.status === 403) {
          toast({
            title: 'Error Deleting Project',
            description: 'You must have admin rights to perform this action',
            variant: 'destructive',
          });
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

  const handleUserAssign = async () => {
    if (!selectedUserId) return toast({ title: 'No user selected' });

    try {
      setAssigningUser(true);
      await assignProjectToUser(selectedUserId, project.id);

      toast({
        title: 'Success',
        description: `User successfully assigned to project`,
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
        } else if (error.response?.status === 403) {
          toast({
            title: 'Error Assigning User to Project',
            description: 'You must have admin rights to perform this action',
            variant: 'destructive',
          });
        } else {
          toast({
            variant: 'destructive',
            title: 'Error Assigning User to Project',
            description: error.message,
          });
        }
      }
    }
  };

  const handleUserUnassign = async (userId: string) => {
    try {
      setAssigningUser(true);
      await unassignProjectFromUser(userId);

      toast({
        title: 'Success',
        description: `User successfully unassigned from project`,
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
          }, 3000);
        } else if (error.response?.status === 403) {
          toast({
            title: 'Error Unassigning User from Project',
            description: 'You must have admin rights to perform this action',
            variant: 'destructive',
          });
        } else {
          toast({
            variant: 'destructive',
            title: 'Error Unassigning User from Project',
            description: error.message,
          });
        }
      }
    }
  };

  const handleUserSelect = (value: string) => setSelectedUserId(value);

  function isProjectWithUserResponse(
    project: ProjectResponse | ProjectWithUserResponse
  ): project is ProjectWithUserResponse {
    return 'users' in project;
  }

  const renderContent = () => {
    const content = isReady
      ? project.details || 'No project details exist'
      : 'Deleting project...';

    let viewUsers = null;

    if (isProjectWithUserResponse(project) && project.users.length > 0) {
      viewUsers = (
        <Dialog>
          <DialogTrigger asChild>
            <Button variant="secondary">View Users</Button>
          </DialogTrigger>
          <DialogContent className="flex flex-col">
            <DialogHeader className="gap-2">
              <DialogTitle>
                Users assigned to Project: {project.name}
              </DialogTitle>
            </DialogHeader>
            <DialogDescription>
              View and remove users assigned to project: {project.name}
            </DialogDescription>
            <ScrollArea className="h-72 rounded-md border">
              <div className="p-4">
                {project.users.map((user) => (
                  <>
                    <div className="flex justify-between items-center">
                      <div key={user.id} className="text-sm">
                        {user.first_name} {user.last_name} - {user.role}
                      </div>
                      {
                        <HoverCard>
                          <HoverCardTrigger>
                            <Button
                              variant="destructive"
                              size="icon"
                              onClick={() => handleUserUnassign(user.id)}
                              disabled={!isAdmin() || assigningUser}
                            >
                              {assigningUser ? (
                                <LoadingSpinner />
                              ) : (
                                <CircleXIcon />
                              )}
                            </Button>
                          </HoverCardTrigger>
                          {!isAdmin() && (
                            <HoverCardContent>
                              <p className="text-sm">
                                Only admins can access this option
                              </p>
                            </HoverCardContent>
                          )}
                        </HoverCard>
                      }
                    </div>
                    <Separator className="my-2" />
                  </>
                ))}
              </div>
            </ScrollArea>
          </DialogContent>
        </Dialog>
      );
    }

    return (
      <div className="flex justify-between items-center">
        {content}
        {viewUsers ? viewUsers : ''}
      </div>
    );
  };
  return (
    <Card className="m-4">
      <CardHeader>
        <div className="flex justify-between items-center">
          <CardTitle>{project.name}</CardTitle>
          <div className="flex gap-2">
            <HoverCard>
              <HoverCardTrigger>
                <Dialog>
                  <DialogTrigger onClick={handleOpenUserAssign} asChild>
                    <Button variant="outline" size="icon" disabled={!isAdmin()}>
                      <UserPlus2Icon />
                    </Button>
                  </DialogTrigger>
                  <DialogContent>
                    <DialogHeader>
                      <DialogTitle>
                        Assign User to Project: {project.name}
                      </DialogTitle>
                    </DialogHeader>
                    <Select onValueChange={handleUserSelect}>
                      <SelectTrigger className="w-full">
                        <SelectValue placeholder="Select a user" />
                      </SelectTrigger>
                      <SelectContent>
                        {Object.values(UserRole).map((role, idx) => (
                          <SelectGroup key={idx}>
                            <SelectLabel>{role}</SelectLabel>
                            {usersLoaded ? (
                              users?.map(
                                (user, idx) =>
                                  user.role === role &&
                                  !user.project && (
                                    <SelectItem key={idx} value={user.id}>
                                      {user.first_name} {user.last_name}
                                    </SelectItem>
                                  )
                              )
                            ) : (
                              <SelectItem disabled value=" ">
                                Loading Users...
                              </SelectItem>
                            )}
                          </SelectGroup>
                        ))}
                      </SelectContent>
                    </Select>
                    {assigningUser ? (
                      <LoadingSpinner message="Assigning User to Project" />
                    ) : (
                      <Button
                        variant="default"
                        disabled={!selectedUserId ? true : false}
                        onClick={handleUserAssign}
                      >
                        Assign User
                      </Button>
                    )}
                  </DialogContent>
                </Dialog>
              </HoverCardTrigger>
              {!isAdmin() && (
                <HoverCardContent>
                  <p className="text-sm">Only admins can access this option</p>
                </HoverCardContent>
              )}
            </HoverCard>
            <HoverCard>
              <HoverCardTrigger>
                <Dialog>
                  <DialogTrigger asChild>
                    <Button variant="outline" size="icon" disabled={!isAdmin()}>
                      <PencilIcon />
                    </Button>
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
              </HoverCardTrigger>
              {!isAdmin() && (
                <HoverCardContent>
                  <p className="text-sm">Only admins can access this option</p>
                </HoverCardContent>
              )}
            </HoverCard>
            <HoverCard>
              <HoverCardTrigger>
                <AlertDialog>
                  <AlertDialogTrigger asChild>
                    <Button
                      variant="destructive"
                      size="icon"
                      disabled={!isAdmin()}
                    >
                      {isDeleting ? <LoadingSpinner /> : <CircleXIcon />}
                    </Button>
                  </AlertDialogTrigger>
                  <AlertDialogContent>
                    <AlertDialogHeader>
                      <AlertDialogTitle>Are you sure?</AlertDialogTitle>
                      <AlertDialogDescription>
                        This action cannot be undone. This will permanently
                        delete
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
              </HoverCardTrigger>
              {!isAdmin() && (
                <HoverCardContent>
                  <p className="text-sm">Only admins can access this option</p>
                </HoverCardContent>
              )}
            </HoverCard>
          </div>
        </div>
        <CardDescription>Customer: {project.customer.name}</CardDescription>
        <CardDescription>Status: {project.status}</CardDescription>
      </CardHeader>

      <CardContent>{renderContent()}</CardContent>
    </Card>
  );
};

export default Project;
