'use client';

import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import { Button } from '../ui/button';
import { UserRoundIcon } from 'lucide-react';
import { useContext, useState } from 'react';
import AuthContext from '@/context/AuthContext';

export default function Header() {
  const [loggingOut, setLoggingOut] = useState<boolean>(false);
  const { logout } = useContext(AuthContext);

  const handleLogout = async (e: Event) => {
    e.preventDefault();
    setLoggingOut(true);

    logout();
  };

  return (
    <div className="grid grid-cols-2 gap-4 pt-7 pb-7 pl-8 pr-8 border-b">
      <div className="flex items-center">
        <h2 className="text-3xl font-semibold tracking-tight transition-colors text-nowrap">
          Project Assignments Portal - Dashboard - Welcome!
        </h2>
      </div>

      <div className="flex items-center justify-end">
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button variant="outline" size="icon">
              <UserRoundIcon className="h-4 w-4" />
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent align="end">
            <DropdownMenuLabel>My Account</DropdownMenuLabel>
            <DropdownMenuSeparator />
            <DropdownMenuItem className="cursor-pointer">
              Profile
            </DropdownMenuItem>
            <DropdownMenuItem>Projects</DropdownMenuItem>
            <DropdownMenuItem
              className="cursor-pointer"
              onSelect={handleLogout}
            >
              {loggingOut ? 'Logging out user...' : 'Logout'}
            </DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      </div>
    </div>
  );
}
