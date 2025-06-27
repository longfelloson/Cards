import Header from "./Header"

const Layout = ({ children }) => {
  return (
    <div>
      <Header/>
      <main 
        className="flex h-screen flex-col gap-8 bg-[#F9FAFB] px-8 md:px-14 pt-8 items-center"
      >
        {children}
      </main>
    </div>
  )
}

export default Layout
