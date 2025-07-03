import api from "./api"

export async function updateUserEmail(newEmail, token, userId) {
  const data = { email: newEmail, verification_token: token };
  const response = await api.patch(`/users/${userId}`, data);
  return response;
}

export async function getUserById(userId) {
  const response = await api.get(`/users/${userId}`);
  return response.data;
}

export async function getCurrentUser() {
  const response = await api.get('/users/me');
  return response.data;
}