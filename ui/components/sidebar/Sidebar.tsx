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
import {
  Command,
  CommandGroup,
  CommandItem,
  CommandList,
  CommandSeparator,
} from '../ui/command';

import { usePathname, useRouter } from 'next/navigation';

const Sidebar = () => {
  const router = useRouter();
  const pathname = usePathname();

  const handleNavigation = (link: string) => {
    router.push(link);
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
          link: '/dashboard/add-customer',
          icon: <HandshakeIcon />,
          text: 'Add New Customer',
        },
        {
          link: '/dashboard/view-customers',
          icon: <GroupIcon />,
          text: 'View All Customers',
        },
      ],
    },
    {
      group: 'Projects',
      items: [
        {
          link: '/dashboard/add-project',
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
          link: '/dashboard/add-user',
          icon: <UserRoundPlusIcon />,
          text: 'Add New User',
        },
        {
          link: '/dashboard/view-users',
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
            {menuList.map((menu, key: number) => {
              return (
                <>
                  <CommandSeparator />
                  <CommandGroup key={key} heading={menu.group}>
                    {menu.items.map((option, idx) => (
                      <CommandItem
                        key={idx}
                        className={`flex gap-2 cursor-pointer ${
                          pathname === option.link ? 'active' : ''
                        }`}
                        onSelect={() => handleNavigation(option.link)}
                      >
                        {option.icon}
                        {option.text}
                      </CommandItem>
                    ))}
                  </CommandGroup>
                </>
              );
            })}
          </CommandList>
        </Command>
      </div>

      <div>Log out</div>
    </div>
  );
};
export default Sidebar;
