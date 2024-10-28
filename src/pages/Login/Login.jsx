import React, { useState } from 'react';
import { Link } from 'react-router-dom';

const Login = () => {
  const [isSignup, setIsSignup] = useState(false);
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
  });
  const [errors, setErrors] = useState({});

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const validate = () => {
    let formErrors = {};
    if (isSignup && !formData.username.trim()) {
      formErrors.username = 'Username is required';
    }
    if (!formData.email.trim()) {
      formErrors.email = 'Email is required';
    }
    if (!formData.password.trim()) {
      formErrors.password = 'Password is required';
    }
    return formErrors;
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const formErrors = validate();
    setErrors(formErrors);
    if (Object.keys(formErrors).length === 0) {
      console.log('Form submitted', formData);
    }
  };

  return (
    <section className='h-screen bg_login text-white flex justify-center items-center'>
      <div className="lg:w-[50%] xl:w-[30%] bg-white py-10 rounded-[15px] px-5">
        <h1 className="text-3xl text-center text-primary font-semibold">
          {isSignup ? 'Sign up' : 'Login'}
        </h1>
        <form
          onSubmit={handleSubmit}
          className='my-3 flex flex-col gap-y-3 lg:w-[90%] xl:w-[90%] mx-auto'
        >
          {isSignup && (
            <div className="space-y-2">
              <label htmlFor="username" className="text-black">Username</label>
              <input
                type="text"
                name='username'
                className="bg-white px-3 border w-full text-black text-sm h-12 rounded-full"
                value={formData.username}
                onChange={handleChange}
              />
              {errors.username && <p className="text-red-500 text-sm">{errors.username}</p>}
            </div>
          )}
          <div className="space-y-2">
            <label htmlFor="email" className="text-black">Email</label>
            <input
              type="email"
              name='email'
              className="bg-white px-3 border w-full text-black text-sm h-12 rounded-full"
              value={formData.email}
              onChange={handleChange}
            />
            {errors.email && <p className="text-red-500 text-sm">{errors.email}</p>}
          </div>
          <div className="space-y-2">
            <label htmlFor="password" className="text-black">Password</label>
            <input
              type="password"
              name='password'
              className="bg-white px-3 border w-full text-black text-sm h-12 rounded-full"
              value={formData.password}
              onChange={handleChange}
            />
            {errors.password && <p className="text-red-500 text-sm">{errors.password}</p>}
          </div>
          <span className="text-primary text-sm text-center">
            {isSignup ? 'Already have an account?' : "Don't have an account?"}
            <button
              type="button"
              className='text-sm underline ml-1'
              onClick={() => setIsSignup(!isSignup)}
            >
              {isSignup ? 'Login' : 'Sign up'}
            </button>
          </span>
          <Link to={"/dashboard"} className="pt-5">
            <button
              type="submit"
              className='uppercase bg-primary h-12 px-3 rounded-full w-full'
            >
              {isSignup ? 'Sign up' : 'Login'}
            </button>
          </Link>
        </form>
      </div>
    </section>
  );
};

export default Login;
