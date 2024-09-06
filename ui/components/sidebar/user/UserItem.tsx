'use client';

import { useContext } from 'react';

import { Avatar, AvatarFallback } from '@/components/ui/avatar';
import AuthContext from '@/context/AuthContext';

const UserItem = () => {
  const { user } = useContext(AuthContext);

  return (
    <div className="min-h-15 h-15 flex items-center border rounded-[10px] p-1">
      <Avatar>
        <AvatarFallback>
          {user!.firstName[0] + user!.lastName[0]}
        </AvatarFallback>
      </Avatar>

      <div className="p-1 ml-2">
        <h4 className="text-2xl font-semibold tracking-tight">
          {user?.username}
        </h4>
        <p className="text-xs text-muted-foreground">
          {user?.admin ? 'admin account' : 'user account'}
        </p>
      </div>
    </div>
  );
};

export default UserItem;
