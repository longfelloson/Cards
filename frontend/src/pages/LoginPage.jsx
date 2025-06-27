import { useState } from "react";
import { loginUser } from "../utils";
import Layout from "../components/Layout";

const LoginPage = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    loginUser(password, email);
  };

  return (
    <Layout>
      <form
        className="flex flex-col gap-3 border border-gray-300 p-6 shadow-md mt-4"
        onSubmit={handleSubmit}
      >
        <label htmlFor="email">Email:</label>
        <input
          className="bg-gray-200 p-2 rounded"
          type="email"
          id="email"
          placeholder="Enter your email"
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        <label htmlFor="password">Password:</label>
        <input
          className="bg-gray-200 p-2 rounded"
          type="password"
          id="password"
          placeholder="Enter your password"
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        <button
          className="bg-[#3B82F6] p-2 rounded hover:bg-[#5862fc] transition-colors duration-300 text-white"
          type="submit"
        >
          Log In
        </button>
      </form>
    </Layout>
  );
};

export default LoginPage;
