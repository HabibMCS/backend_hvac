import Sidebar from "@/components/Sidebar/Sidebar"
import { Switch } from "@/components/ui/switch"

const Profile = () => {
    return (
        <div className='flex'>
            <Sidebar />
            <section className="max-h-[90vh] p-4 w-[85vw] overflow-y-scroll">
                <h1 className="text-3xl text-primary">
                    My Profile
                </h1>
                <form action="" className="space-y-8 my-8">
                    <div className="flex flex-wrap gap-x-2 gap-y-4 justify-between items-center">
                        <input type="text" placeholder="First Name" className="bg-white px-3 border w-[48%] text-black text-sm h-12 rounded-full" />
                        <input type="text" placeholder="Last Name" className="bg-white px-3 border w-[48%] text-black text-sm h-12 rounded-full" />
                        <input type="email" placeholder="Your Email" className="bg-white px-3 border w-[48%] text-black text-sm h-12 rounded-full" />
                        <input type="number" placeholder="Phone Number" className="bg-white px-3 border w-[48%] text-black text-sm h-12 rounded-full" />
                    </div>
                    <h3 className="text-2xl text-primary pt-4 border-t">
                        User Preferences
                    </h3>
                    <div className="flex flex-wrap items-center gap-x-2 gap-y-4">
                        <div className="bg-white border w-[48%] text-black text-sm h-12 rounded-[10px] flex items-center justify-between px-5">
                            <span>Temperature Units</span>
                            <div className="flex items-center space-x-8">
                                <label htmlFor="°C">°C</label>
                                <Switch checked id="temp" />
                                <label htmlFor="°F">°F</label>
                            </div>
                        </div>
                        <div className="bg-white border w-[48%] text-black text-sm h-12 rounded-[10px] flex items-center justify-between px-5">
                            <span>Pressure Units</span>
                            <div className="flex items-center space-x-8">
                                <label htmlFor="kg/cm2">kg/cm2</label>
                                <Switch id="pressure" />
                                <label htmlFor="PSI">PSI</label>
                            </div>
                        </div>
                        <div className="bg-white border w-[48%] text-black text-sm h-12 rounded-[10px] flex items-center justify-between px-5">
                            <span>Time Format</span>
                            <div className="flex items-center space-x-8">
                                <label htmlFor="24hours">24 hours</label>
                                <Switch  id="time" />
                                <label htmlFor="12hours">12 hours</label>
                            </div>
                        </div>
                        <div className="bg-white border w-[48%] text-black text-sm h-12 rounded-[10px] flex items-center justify-between px-5">
                            <span>Date Format</span>
                            <div className="flex items-center space-x-8">
                                <label htmlFor="DD/MM/YY">DD/MM/YY</label>
                                <Switch id="time" />
                                <label htmlFor="MM/DD/YY"> MM/DD/YY</label>
                            </div>
                        </div>
                        <div className="bg-white border w-[48%] text-black text-sm h-12 rounded-[10px] flex items-center justify-between px-5">
                            <span>Hide filter alerts</span>
                            <div className="flex items-center space-x-8">
                                <Switch id="filter" />
                            </div>
                        </div>
                        <div className="bg-white border w-[48%] text-black text-sm h-12 rounded-[10px] flex items-center justify-between px-5">
                            <span>Enable unit/group reorder</span>
                            <div className="flex items-center space-x-8">
                                <Switch checked id="unit" />
                            </div>
                        </div>
                        <div className="bg-white border w-[48%] text-black text-sm h-12 rounded-[10px] flex items-center justify-between px-5">
                            <span>Enable email 2-factor-authentication</span>
                            <div className="flex items-center space-x-8">
                                <Switch id="2fa" />
                            </div>
                        </div>
                        <select name="lang" id="lang" className="bg-white border w-[48%] text-black text-sm h-12 rounded-[10px] flex items-center justify-between px-5">
                            <option value="" selected hidden>Select Language</option>
                            <option value="english">English</option>
                            <option value="spanish">Spanish</option>
                        </select>
                        <div className="pt-5 w-[30%] mx-auto">
                            <button className='uppercase bg-primary text-white h-12 px-3 rounded-full w-full'>
                                Save Changes
                            </button>
                        </div>
                    </div>
                </form>
            </section>
        </div>
    )
}

export default Profile
