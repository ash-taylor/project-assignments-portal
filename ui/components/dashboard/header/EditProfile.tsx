'use client';

import { AxiosError } from 'axios';
import { useContext, useState } from 'react';

import { Button } from '@/components/ui/button';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import AuthContext from '@/context/AuthContext';
import { useToast } from '@/hooks/use-toast';
import { updateUser } from '@/lib/api';
import { UserRole, UserUpdate } from '@/models/User';

interface EditProfileProps {
  isDialogOpen: boolean;
  setIsDialogOpen: (value: boolean) => void;
}

const EditProfile = ({ isDialogOpen, setIsDialogOpen }: EditProfileProps) => {
  const { user, logout } = useContext(AuthContext);

  const [isUpdating, setIsUpdating] = useState<boolean>(false);
  const [userInfo, setUserInfo] = useState<{
    username?: string;
    role?: UserRole;
    firstName?: string;
    lastName?: string;
    email?: string;
  }>({
    username: user?.username,
    role: user?.role as UserRole,
    firstName: user?.firstName,
    lastName: user?.lastName,
    email: user?.email,
  });

  const { toast } = useToast();

  const handleUpdateUser = async (userId: string, user: UserUpdate) => {
    try {
      setIsUpdating(true);
      const response = await updateUser(user);

      toast({
        title: 'User updated successfully',
        description: 'Your profile has been updated',
      });

      setUserInfo({
        username: response.data.user_name,
        role: response.data.role as UserRole,
        firstName: response.data.first_name,
        lastName: response.data.last_name,
        email: response.data.email,
      });
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
            title: 'Error - Cannot Update User!',
            description: `You do not have permission to update this user!`,
            variant: 'destructive',
          });
        } else if (error.response?.status === 404) {
          toast({
            title: 'Error - Cannot Find User!',
            description: `User not found!`,
            variant: 'destructive',
          });
        } else if (error.response?.status === 409) {
          toast({
            title: 'Error - Cannot Update User!',
            description: `User email already exists!`,
            variant: 'destructive',
          });
        } else {
          toast({
            title: 'Error updating user',
            description: 'Something went wrong',
            variant: 'destructive',
          });
        }
      }
    } finally {
      setIsUpdating(false);
    }
  };

  return (
    <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
      <DialogContent className="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle>Edit profile</DialogTitle>
          <DialogDescription>
            Make changes to your profile here. <br />
            Click save when you&apos;re done.
          </DialogDescription>
        </DialogHeader>
        <div className="grid gap-4 py-4">
          <div className="grid grid-cols-4 items-center gap-4">
            <Label htmlFor="username" className="text-right">
              Username
            </Label>
            <Input
              id="username"
              value={userInfo.username}
              className="col-span-3"
              disabled
            />
          </div>
          <div className="grid grid-cols-4 items-center gap-4">
            <Label htmlFor="name" className="text-right">
              User Role
            </Label>
            <Input
              disabled
              id="role"
              value={userInfo?.role}
              className="col-span-3"
            />
          </div>
          <div className="grid grid-cols-4 items-center gap-4">
            <Label htmlFor="name" className="text-right">
              First Name
            </Label>
            <Input
              id="firstName"
              value={userInfo.firstName}
              onChange={(e) =>
                setUserInfo({ ...userInfo, firstName: e.target.value })
              }
              className="col-span-3"
              type="text"
            />
          </div>
          <div className="grid grid-cols-4 items-center gap-4">
            <Label htmlFor="name" className="text-right">
              Last Name
            </Label>
            <Input
              id="lastName"
              value={userInfo.lastName}
              onChange={(e) =>
                setUserInfo({ ...userInfo, lastName: e.target.value })
              }
              className="col-span-3"
              type="text"
            />
          </div>
          <div className="grid grid-cols-4 items-center gap-4">
            <Label htmlFor="name" className="text-right">
              Email
            </Label>
            <Input
              id="email"
              value={userInfo.email}
              onChange={(e) =>
                setUserInfo({ ...userInfo, email: e.target.value })
              }
              className="col-span-3"
              type="email"
            />
          </div>
        </div>
        <DialogFooter>
          <Button
            type="submit"
            onClick={() =>
              handleUpdateUser(user!.id, {
                first_name: userInfo.firstName!,
                last_name: userInfo.lastName!,
                email: userInfo.email!,
              })
            }
            disabled={isUpdating}
          >
            {isUpdating ? 'Updating User...' : 'Save Changes'}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
};
export default EditProfile;
