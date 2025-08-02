import React, { useState, useEffect } from "react";
import axios from "axios";

const StudentList = () => {
  const [students, setStudents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchQuery, setSearchQuery] = useState("");
  const [sortKey, setSortKey] = useState("age");

  useEffect(() => {
    const fetchStudents = async () => {
      try {
        const response = await axios.get("http://localhost:8000/students");
        setStudents(response.data);
        setLoading(false);
      } catch (err) {
        setError("خطا در دریافت داده.");
        setLoading(false);
      }
    };
    fetchStudents();
  }, []);

  const filteredStudents = students.filter(student =>
    student.name.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const sortedStudents = [...filteredStudents].sort((a, b) => {
    if (sortKey === "age") {
      return a.age - b.age;
    } else if (sortKey === "grade") {
      return a.grade.localeCompare(b.grade);
    }
    return 0;
  });

  if (loading) {
    return <div>در حال بارگذاری...</div>;
  }

  if (error) {
    return <div>{error}</div>;
  }

  return (
    <div>
      <h1>لیست دانش‌آموزان</h1>
      <input
        type="text"
        placeholder="جستجو بر اساس نام"
        value={searchQuery}
        onChange={(e) => setSearchQuery(e.target.value)}
      />
      <select onChange={(e) => setSortKey(e.target.value)} value={sortKey}>
        <option value="age">مرتب‌سازی بر اساس سن</option>
        <option value="grade">مرتب‌سازی بر اساس پایه تحصیلی</option>
      </select>
      <ul>
        {sortedStudents.map((student) => (
          <li key={student.id}>
            {student.name} - {student.grade} - {student.age} سال
          </li>
        ))}
      </ul>
    </div>
  );
};

export default StudentList;