'use client';

import {
  Command,
  CommandItem,
  CommandList,
  CommandGroup,
  CommandSeparator,
} from '@/components/ui/command';
import UserItem from '@/components/sidebar/user/UserItem';

const Sidebar = () => {
  return (
    <div className="flex flex-col gap-2 w-[300px] min-w-[300px] border-r min-h-screen p-4">
      <UserItem />
      <div className="grow">
        <Command>
          <CommandList>
            <CommandGroup heading="Customers">
              <CommandItem>Add Customer</CommandItem>
              <CommandItem>View Customers</CommandItem>
            </CommandGroup>
            <CommandSeparator />
            <CommandGroup heading="Projects">
              <CommandItem>Add Project</CommandItem>
              <CommandItem>View Projects</CommandItem>
            </CommandGroup>
            <CommandSeparator />
            <CommandGroup heading="Users">
              <CommandItem>Add User</CommandItem>
              <CommandItem>View Users</CommandItem>
            </CommandGroup>
          </CommandList>
        </Command>
      </div>
      <div>Settings</div>
    </div>
  );
};

export default Sidebar;
