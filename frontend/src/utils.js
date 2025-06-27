import { useEffect, useState } from "react";
import api from "./api";

export function useDebouncedValue(value, delay = 500) {
  const [debouncedValue, setDebouncedValue] = useState(value);

  useEffect(() => {
    const timer = setTimeout(() => setDebouncedValue(value), delay);
    return () => clearTimeout(timer); // Cleanup if value changes
  }, [value, delay]);

  return debouncedValue;
}

export async function loginUser(password, email) {
  const data = {
    email: email, 
    password: password,
  }
  const response = await api.post('/auth/token', data);
  
  localStorage.setItem('token', response.data.access_token);
  window.location.href = '/';
}
