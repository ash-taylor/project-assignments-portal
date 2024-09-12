'use client';

import { UserRoundIcon } from 'lucide-react';
import { useContext, useState } from 'react';

import { Button } from '@/components/ui/button';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import AuthContext from '@/context/AuthContext';
import EditProfile from './EditProfile';

export default function Header() {
  const [isDialogOpen, setIsDialogOpen] = useState<boolean>(false);
  const [loggingOut, setLoggingOut] = useState<boolean>(false);

  const { logout, user } = useContext(AuthContext);

  const handleLogout = async (e: Event) => {
    e.preventDefault();
    setLoggingOut(true);
    logout();
  };

  const handleOpenDialog = (e: Event) => {
    e.preventDefault();
    setIsDialogOpen(true);
  };

  return (
    <div className="sticky top-0 z-40 flex justify-between items-center pt-7 pb-7 pl-8 pr-8 border-b bg-white min-w-[750px]">
      <h2 className="text-3xl font-medium tracking-tight transition-colors text-nowrap">
        Welcome {user?.firstName}!
      </h2>
      <h2 className="text-3xl font-semibold tracking-tight transition-colors text-nowrap">
        Project Assignments Portal
      </h2>

      <DropdownMenu>
        <DropdownMenuTrigger asChild>
          <Button variant="outline" size="icon">
            <UserRoundIcon className="h-4 w-4" />
          </Button>
        </DropdownMenuTrigger>
        <DropdownMenuContent align="end">
          <DropdownMenuLabel>My Account</DropdownMenuLabel>
          <DropdownMenuSeparator />
          <DropdownMenuItem
            className="cursor-pointer"
            onSelect={handleOpenDialog}
          >
            Edit Profile
          </DropdownMenuItem>
          <DropdownMenuItem className="cursor-pointer" onSelect={handleLogout}>
            {loggingOut ? 'Logging out user...' : 'Logout'}
          </DropdownMenuItem>
        </DropdownMenuContent>
      </DropdownMenu>
      <EditProfile
        isDialogOpen={isDialogOpen}
        setIsDialogOpen={setIsDialogOpen}
      />
    </div>
  );
}
