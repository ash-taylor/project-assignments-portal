'use client';

import {
  FilePlusIcon,
  FilesIcon,
  GroupIcon,
  HandshakeIcon,
  LayoutDashboardIcon,
  UsersRoundIcon,
} from 'lucide-react';
import { Fragment, useContext } from 'react';

import {
  Command,
  CommandGroup,
  CommandItem,
  CommandList,
  CommandSeparator,
} from '@/components/ui/command';
import {
  HoverCard,
  HoverCardContent,
  HoverCardTrigger,
} from '@/components/ui/hover-card';
import AuthContext from '@/context/AuthContext';
import UserItem from './user/UserItem';
interface SidebarProps {
  onNavigate: (link: string) => void;
}

const Sidebar = ({ onNavigate }: SidebarProps) => {
  const { isAdmin } = useContext(AuthContext);

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
          admin: false,
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
          admin: true,
        },
        {
          link: '/view-customers',
          icon: <GroupIcon />,
          text: 'View All Customers',
          admin: false,
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
          admin: true,
        },
        {
          link: '/view-projects',
          icon: <FilesIcon />,
          text: 'View All Projects',
          admin: false,
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
          admin: true,
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
                    <HoverCard key={idx}>
                      <HoverCardTrigger>
                        <CommandItem
                          key={idx}
                          className={`flex gap-2 cursor-pointer`}
                          onSelect={() => handleNavigation(option.link)}
                          disabled={!isAdmin() && option.admin}
                        >
                          {option.icon}
                          {option.text}
                        </CommandItem>
                      </HoverCardTrigger>
                      {!isAdmin() && option.admin && (
                        <HoverCardContent>
                          <p className="text-sm">
                            Only admins can access this option
                          </p>
                        </HoverCardContent>
                      )}
                    </HoverCard>
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
