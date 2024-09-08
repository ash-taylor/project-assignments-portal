'use client';

import {
  FilePlusIcon,
  FilesIcon,
  GroupIcon,
  HandshakeIcon,
  LayoutDashboardIcon,
  UserRoundPlusIcon,
  UsersRoundIcon,
} from 'lucide-react';
import UserItem from './user/UserItem';

import { Fragment } from 'react';
import {
  Command,
  CommandGroup,
  CommandItem,
  CommandList,
  CommandSeparator,
} from '@/components/ui/command';

interface SidebarProps {
  onNavigate: (link: string) => void;
}

const Sidebar = ({ onNavigate }: SidebarProps) => {
  const handleNavigation = (link: string) => {
    onNavigate(link);
  };

  const menuList = [
    {
      group: 'Dashboard',
      items: [
        {
          link: '/dashboard',
          icon: <LayoutDashboardIcon />,
          text: 'Dashboard',
        },
      ],
    },
    {
      group: 'Customers',
      items: [
        {
          link: '/add-customer',
          icon: <HandshakeIcon />,
          text: 'Add New Customer',
        },
        {
          link: '/view-customers',
          icon: <GroupIcon />,
          text: 'View All Customers',
        },
      ],
    },
    {
      group: 'Projects',
      items: [
        {
          link: '/add-project',
          icon: <FilePlusIcon />,
          text: 'Add New Project',
        },
        {
          link: '/view-projects',
          icon: <FilesIcon />,
          text: 'View All Projects',
        },
      ],
    },
    {
      group: 'Users',
      items: [
        {
          link: '/add-user',
          icon: <UserRoundPlusIcon />,
          text: 'Add New User',
        },
        {
          link: '/view-users',
          icon: <UsersRoundIcon />,
          text: 'View All Users',
        },
      ],
    },
  ];
  return (
    <div className="fixed flex flex-col gap-4 min-w-[300px] p-4 min-h-screen">
      <UserItem />
      <div className="grow">
        <Command style={{ overflow: 'visible' }}>
          <CommandList style={{ overflow: 'visible' }}>
            {menuList.map((menu, key: number) => (
              <Fragment key={key}>
                <CommandSeparator />
                <CommandGroup heading={menu.group}>
                  {menu.items.map((option, idx) => (
                    <CommandItem
                      key={idx}
                      className={`flex gap-2 cursor-pointer`}
                      onSelect={() => handleNavigation(option.link)}
                    >
                      {option.icon}
                      {option.text}
                    </CommandItem>
                  ))}
                </CommandGroup>
              </Fragment>
            ))}
          </CommandList>
        </Command>
      </div>

      <div>Log out</div>
    </div>
  );
};
export default Sidebar;
