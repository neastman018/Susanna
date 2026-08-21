import '@fontsource/inter'; // Defaults to weight 400
import ThemeRegistry from './theme.provider';
import { ReactQueryProvider } from "./querywrapper";

export const metadata = {
  title: "Smart Display",
  description: "Custom Magic Mirror Display Screen",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>
        <ReactQueryProvider><ThemeRegistry>{children}</ThemeRegistry></ReactQueryProvider>
      </body>
    </html>
  );
}
