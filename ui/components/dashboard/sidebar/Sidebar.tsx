'use client';

import {
  FilePlusIcon,
  FilesIcon,
  GroupIcon,
  HandshakeIcon,
  LayoutDashboardIcon,
  UsersRoundIcon,
} from 'lucide-react';
import { Fragment } from 'react';

import {
  Command,
  CommandGroup,
  CommandItem,
  CommandList,
  CommandSeparator,
} from '@/components/ui/command';
import UserItem from './user/UserItem';

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
          text: 'Project Assignments Overview',
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
      group: 'Team',
      items: [
        {
          link: '/manage-users',
          icon: <UsersRoundIcon />,
          text: 'Manage Team',
        },
      ],
    },
  ];
  return (
    <div className="flex flex-col gap-4 p-4 min-h-screen bg-white">
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
    </div>
  );
};
export default Sidebar;
