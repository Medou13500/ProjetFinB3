import React from 'react';
import Header from '../component/Header';
import Footer from '../component/Footer';
import { Outlet } from 'react-router-dom';

const Layout = () => {
  return (
    <div className='d-flex flex-column min-vh-100'>
      <Header />

      <main className='flex-grow-1 mt-4'>
        <Outlet />
      </main>

      <Footer />
    </div>
  );
};

export default Layout;
