import { Geist, Geist_Mono } from "next/font/google";
import '@fontsource/inter'; // Defaults to weight 400
import ThemeRegistry from './theme.provider';
import { ReactQueryProvider } from "./querywrapper";


const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata = {
  title: "Smart Display",
  description: "Custom Magic Mirror Display Screen",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className={`${geistSans.variable} ${geistMono.variable}`}>
        <ReactQueryProvider><ThemeRegistry>{children}</ThemeRegistry></ReactQueryProvider>
      </body>
    </html>
  );
}
