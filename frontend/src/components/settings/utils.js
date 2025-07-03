import api from "../../api";

export async function sendVerificationEmail(user_id, newEmail){
  const data = {verify_email: true, email: newEmail}
  await api.patch(`/users/${user_id}`, data)
}
