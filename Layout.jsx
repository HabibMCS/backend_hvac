import Header from '@/components/Header/Header'
import Sidebar from '@/components/Sidebar/Sidebar'
import { Outlet } from 'react-router-dom'
import { useLocation } from 'react-router-dom'
function Layout() {
    const location = useLocation();
    if (location.pathname === '/') {
        return (
            <>
                <Outlet />
            </>
        )
    }
    else {
        return (
            <>
                <Header />
                <Outlet />
            </>
        )
    }

}

export default Layout
