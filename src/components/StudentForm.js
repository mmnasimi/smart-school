import React, { useState } from "react";
import axios from "axios";

const StudentForm = () => {
  const [formData, setFormData] = useState({ name: "", grade: "", age: "" });

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post("http://localhost:8000/students", formData);
      alert("Student added successfully!");
    } catch (error) {
      console.error("Error adding student:", error);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        placeholder="Name"
        value={formData.name}
        onChange={(e) => setFormData({ ...formData, name: e.target.value })}
      />
      <input
        type="text"
        placeholder="Grade"
        value={formData.grade}
        onChange={(e) => setFormData({ ...formData, grade: e.target.value })}
      />
      <input
        type="number"
        placeholder="Age"
        value={formData.age}
      />
      <button type="submit">Add Student</button>
    </form>
  );
};

export default StudentForm;

import { API_BASE_URL } from "../apiConfig";

const handleSubmit = async (event) => {
    event.preventDefault();
    const studentData = { name, grade, interests, age };
    try {
        await axios.post(`${API_BASE_URL}/students`, studentData);
        alert("دانش‌آموز با موفقیت اضافه شد!");
    } catch (error) {
        console.error("خطا در افزودن دانش‌آموز", error);
    }
};
