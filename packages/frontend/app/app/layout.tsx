import Footer from "@/components/footer/Footer";

export default function AppLayout({children}: {children: React.ReactNode}) {
  return (
    <div className="min-h-screen flex flex-col">
      <main className="grow flex">{children}</main>
      <Footer />
    </div>
  );
}
