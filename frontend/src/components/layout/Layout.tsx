import { Outlet, useLocation } from 'react-router-dom'
import Header from './Header'
import Sidebar from './Sidebar'

// content via <Outlet/>. The pending-approvals count is a placeholder for now;
// later tasks replace it with the live value from the approvals data hook.
export default function Layout() {
  const { pathname } = useLocation()

  return (
    <div className="min-h-screen flex">
      <Sidebar />
      <div className="flex-1 min-w-0 flex flex-col">
        <Header pendingApprovals={0} />
        <main key={pathname} className="flex-1 px-6 py-7 max-w-[1400px] w-full mx-auto">
          <Outlet />
        </main>
      </div>
    </div>
  )
}
