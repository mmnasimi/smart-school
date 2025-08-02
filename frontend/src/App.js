import { BrowserRouter, Routes, Route } from "react-router-dom";
import StudentForm from "./components/StudentForm";
import StudentList from "./components/StudentList";

function App() {
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/students" element={<StudentList />} />
                <Route path="/add-student" element={<StudentForm />} />
            </Routes>
        </BrowserRouter>
    );
}
export default App;
// This code sets up a React application with routing using react-router-dom.