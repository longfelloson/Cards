import { useEffect, useState } from "react";
import Layout from "../components/Layout";
import SettingsList from "../components/settings/SettingsList";
import SettingsEmail from "../components/settings/SettingsEmail";
import { getCurrentUser, getUserById } from "../users";

const SettingsPage = () => {
  const [user, setUser] = useState(null);
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
      const currentUser = async () => {
        try {
          const data = await getCurrentUser()
          setUser(data)
        } catch (err) {
          console.log("Failed to fetch the current user:", err)
          setIsLoading(false)
        } finally {
          setIsLoading(false)
        }
      }
      currentUser()
    }, []
  )

  if (isLoading) {
    return (
      <Layout className="grid grid-cols-3 grid-rows-12">
        <div>Loading user settings...</div>
      </Layout>
    );
  }

  return (
    <Layout className="grid grid-cols-3 grid-rows-12">
      <SettingsList />
      <SettingsEmail user={user}/>
    </Layout>
  )
};

export default SettingsPage