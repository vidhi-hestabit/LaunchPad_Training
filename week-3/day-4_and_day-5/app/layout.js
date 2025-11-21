import "./globals.css";
import Modal from "./components/ui/Modal";

export const metadata = {
  title: "Dashboard",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>
        <Modal>
          {children}
        </Modal>
      </body>
    </html>
  );
}
