import api from "../api";
import Layout from "../components/Layout";
import { loginUser } from "../utils";

const RegisterPage = () => {
  const createUser = async (e) => {
    e.preventDefault();

    const form = e.target;
    const formData = new FormData(form);

    const data = {
      email: formData.get("email"),
      password: formData.get("password"),
    }
    await api.post("/users", data);
    await loginUser(null, data.password, data.email);
  };

  return (
    <Layout>
      <div className="flex flex-col shadow-md rounded-md bg-gray-100 max-w-md w-full p-8">
        <h1 className="text-center font-bold mb-4">Register</h1>
        <form 
          className="flex flex-col gap-4"
          onSubmit={(e) => {createUser(e)}}
        >
          <input 
            className="rounded-md bg-white border-2 border-blue-500 p-2" 
            type="email" 
            placeholder="Enter your email: " 
            name="email"
            required
          />
          <input 
            className="rounded-md bg-white border-2 border-blue-500 p-2" 
            type="password" 
            placeholder="Enter your password: " 
            name="password"
            required
          />
          <button 
            className="bg-blue-500 p-4 rounded-md text-white" type="submit"
          >
            Register
          </button>
        </form>
      </div>
    </Layout>
  )
};

export default RegisterPage