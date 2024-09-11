'use client';

import { Avatar, AvatarFallback } from '@/components/ui/avatar';
import AuthContext from '@/context/AuthContext';
import { useContext } from 'react';

const UserItem = () => {
  const { user } = useContext(AuthContext);

  return (
    <div className="min-h-15 h-15 flex items-center p-1">
      <Avatar>
        <AvatarFallback>
          {user!.firstName[0] + user!.lastName[0]}
        </AvatarFallback>
      </Avatar>

      <div className="p-1 ml-2">
        <h4 className="text-2xl font-semibold tracking-tight">
          Hey {user?.firstName}!
        </h4>
        <p className="text-xs text-muted-foreground">
          {user?.username} - [{user?.role}]
        </p>
      </div>
    </div>
  );
};
export default UserItem;
