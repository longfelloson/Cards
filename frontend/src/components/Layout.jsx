import Header from "./Header"

const Layout = ({ children, className }) => {
  return (
    <div>
      <Header />
      <main
        className={className}
        style={{
          height: '100vh',
          gap: '2rem',
          backgroundColor: '#F9FAFB',
          padding: '3.5rem',
        }}
      >
        {children}
      </main>
    </div>
  );
};

export default Layout;
