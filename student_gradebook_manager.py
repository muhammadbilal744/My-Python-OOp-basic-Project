# 1. I learned how to use @dataclass in Python.
# 2. I learned how to use private variables using double underscore (__).
# 3. I learned how to validate user input.
# 4. I understood how dictionaries store subject and marks.
# 5. I learned how to calculate averages safely.
# 6. I learned how to use Optional and Tuple from typing.
# 7. I understood how to raise errors like ValueError and KeyError.
# 8. I learned how to find subject topper and overall topper.
# 9. I learned how to build a menu-driven CLI program.
# 10. I improved my understanding of Object-Oriented Programming (OOP)






# Import the dataclass decorator and field function from the dataclasses module
from dataclasses import dataclass, field

# Comment: we don't need to write the __init__ method, it will be generated automatically by the dataclass decorator
# This is just a comment explaining the benefit of dataclasses

# Import Dict, Tuple, and Optional types for type hinting
from typing import Dict, Tuple, Optional

# Comment: this will helps us to add the type hint to our code
# This explains that we're importing these for type annotations

@dataclass  # This decorator tells Python to generate special methods automatically
class Student:
    # Define class attributes with type hints
    student_id: str  # Public attribute: unique identifier for each student
    name: str  # Public attribute: student's name
    
     
    # Private attribute (name mangling with __) to store marks
    # field() creates a field with special properties:
    # - default_factory=dict means each instance gets its own empty dict
    # - repr=False means this field won't appear in the __repr__ output
    __marks: Dict[str, float] = field(default_factory=dict, repr=False)

    def set_mark(self, subject: str, score: float) -> None:
        # Method to add or update a mark for a subject
        
        # First validation: check if subject is empty
        if not subject:
            raise ValueError("Subject cannot be empty.")
    
    # TODO: validate subject not empty
    # TODO: validate score 0-100
    # These are TODO comments reminding what needs to be implemented
    
        # Second validation: check if score is between 0 and 100
        if not 0 <= score <= 100:
            raise ValueError("Score must be between 0 and 100.")
        
        # Add/update the mark in the private dictionary
        self.__marks[subject] = score
        
    def get_mark(self, subject: str) -> Optional[float]:
        # Method to retrieve a mark for a specific subject
        # TODO: return mark or None if not found
        
        # Use dictionary's get() method which returns None if key doesn't exist
        return self.__marks.get(subject)
    
    def average(self) -> float:
        # Method to calculate average of all marks
        # TODO: return average (0.0 if no marks)
        
        # Calculate average: sum of values divided by number of items
        # If dictionary is empty, return 0.0 using ternary operator
        return sum(self.__marks.values()) / len(self.__marks) if self.__marks else 0.0
        
        # Alternative implementation (commented out)
        # if not self.__marks:
        #     return 0.0
        # return sum(self.__marks.values())/ len(self.__marks)
    
     
    @property  # This decorator creates a getter method that acts like an attribute
    def marks(self) -> Dict[str, float]:
        # Property to safely access marks (returns a copy, not the original)
        # TODO: return a copy (not the real dict)
        
        # Create and return a new dictionary with the same data
        return dict(self.__marks)
    
    def report_lines(self) -> list[str]:
        # Method to generate a formatted report of student data
        # TODO: create readable report lines
        
        # Start with student information line
        lines = [f"Student: {self.student_id} - {self.name}"]
        
        # Check if there are no marks
        if not self.__marks:
            lines.append("No marks recorded.")
            return lines
        
        # Add each subject and score, sorted alphabetically
        for subject, score in sorted(self.__marks.items()):
            lines.append(f"- {subject}: {score}")
        
        # Add average with 2 decimal places
        lines.append(f"Average: {self.average():.2f}")
        return lines

class Gradebook:
    def __init__(self):
        # Constructor method that initializes a new gradebook
        # Create empty dictionary to store students with ID as key
        self.students: Dict[str, Student] = {}
        
    def add_student(self, student_id: str, name: str) -> None:
        # Method to add a new student to the gradebook
        
        # Remove leading/trailing whitespace
        student_id = student_id.strip()
        name = name.strip()
        
        # TODO: validate unique id
        
        # Check if ID or name is empty
        if not student_id or not name:
            raise ValueError("Student ID and name are required.")
        
        # Check if student ID already exists
        if student_id in self.students:
            raise ValueError("Student ID already exists.")
        
        # Create new Student object and add to dictionary
        self.students[student_id] = Student(student_id, name)
        
    def record_mark(self, student_id: str, subject: str, score: float) -> None:
        # Method to record a mark for a student
        
        # Check if student exists
        if student_id not in self.students:
            raise KeyError("Student not found.")
        
        # TODO: check student exists
        
        # Call the student's set_mark method
        self.students[student_id].set_mark(subject, score)
        
    def student_report(self, student_id: str) -> list[str]:
        # Method to get report for a specific student
        
        # Check if student exists
        if student_id not in self.students:
            raise KeyError("Student not found.")
        
        # TODO: return report lines
        
        # Call the student's report_lines method
        return self.students[student_id].report_lines()
    
    def subject_topper(self, subject: str) -> Tuple[str, float]:
        # Method to find the student with highest score in a subject
        
        # Initialize variables
        topper_id = " "  # Will store ID of top student
        topper_score = -1.0  # Initialize with low score
        
        # Loop through all students
        for sid, st in self.students.items():
            # Get student's mark for this subject
            score = st.get_mark(subject)
            # If student has a mark and it's higher than current max
            if score is not None and score > topper_score:
                topper_score = score
                topper_id = sid
        
        # If no student has marks for this subject
        if topper_score < 0:
            raise ValueError("No marks found for this subject.")
        
        # Return ID and score of top student
        return topper_id, topper_score
    
        # TODO: return (student_id, score) max in subject
    
    def overall_topper(self) -> Tuple[str, float]:
        # Method to find student with highest average marks
        
        # Check if there are any students
        if not self.students:
            raise ValueError("No student.")
        
        # Initialize variables
        best_id = ""  # Will store ID of best student
        best_avg = -1.0  # Initialize with low average
        
        # Loop through all students
        for sid, st in self.students.items():
            # Get student's average
            avg = st.average()
            # If this average is higher than current best
            if avg > best_avg:
                best_avg = avg
                best_id = sid
        
        # Return ID and average of best student
        return best_id, best_avg 

def main():
    # Main function that runs the interactive program
    
    # Create a gradebook instance
    gb = Gradebook()
    
    # Infinite loop for menu system
    while True:
        # Display menu options
        print("\n--- Gradebook Menu ---")
        print("1) ADD student")
        print("2) Record/Update mark ")
        print("3) Show student report")
        print("4) Subject Topper")
        print("5) Overall Topper")
        print("6) Exit")
        
        # Get user choice
        choice = input("Choose:").strip()
        
        # Try-except block to handle errors gracefully
        try:
            # Handle each menu option
            if choice == "1":
                # Add student
                sid = input("Student ID: ")
                name = input("Name: ")
                gb.add_student(sid, name)
                print("Student added.")
                
            elif choice == "2":
                # Record mark
                sid = input("Student ID: ")
                subject = input("Subject: ")
                score = float(input("Score (0-100): "))
                gb.record_mark(sid, subject, score)
                print("Marks recorded.")
                
            elif choice == "3":
                # Show student report
                sid = input("Student ID: ")
                for line in gb.student_report(sid):
                    print(line)
                    
            elif choice == "4":
                # Show subject topper
                subject = input("Subject: ")
                sid, score = gb.subject_topper(subject)
                st = gb.students[sid]
                print(f"Topper: {st.name} ({sid}) with {score}")
                
            elif choice == "5":
                # Show overall topper
                sid, avg = gb.overall_topper()
                st = gb.students[sid]
                print(f"Overall topper: {st.name} ({sid}) average {avg:.2f}")
                
            elif choice == "6": 
                # Exit program
                print("Goodbye.")
                break
                
            else:
                # Invalid choice
                print("Invalid choice.") 
        
        # Catch any exception and display error message
        except Exception as e:
            print("Error:", e)
            
# Standard Python idiom to run main() only if this file is executed directly
if __name__ == "__main__":
    main()