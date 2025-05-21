import './App.css';
import { ThemeProvider } from './context/ThemeContext';
import AppRoutes from './routes';

export default function App() {
  return (
    <ThemeProvider>
      <div className="App">
        <AppRoutes />
      </div>
    </ThemeProvider>
  );
}
