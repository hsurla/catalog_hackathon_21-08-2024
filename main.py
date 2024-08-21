from datetime import datetime, timedelta

users = {}  #store user credentials
children = {}  #store children's information
appointments = []  #store appointments

# Vaccination schedule
vaccination_schedule = {
    "BCG": 0, 
    "Polio": 45,  
    "DTP": 75,  
}

# Function Definitions

def register(username, password):
    if username in users:
        return "Username already exists."
    users[username] = password
    return "User registered successfully."

def login(username, password):
    if username in users and users[username] == password:
        return "Login successful."
    return "Invalid username or password."

def add_child(parent_username, child_name, dob):
    if parent_username not in children:
        children[parent_username] = []
    child_info = {"name": child_name, "dob": dob, "vaccinations": []}
    children[parent_username].append(child_info)
    return f"Child {child_name} added successfully."

def suggest_next_vaccine(dob):
    current_date = datetime.now().date()
    child_age_days = (current_date - dob).days
    
    # Sort vaccinations by age in days
    sorted_vaccinations = sorted(vaccination_schedule.items(), key=lambda item: item[1])
    
    for vaccine, due_in_days in sorted_vaccinations:
        # Calculate the date when the vaccine is due
        vaccine_due_date = dob + timedelta(days=due_in_days)
        
        if current_date < vaccine_due_date:
            return f"Next vaccine: {vaccine}, Date: {vaccine_due_date}"
    
    return "All vaccinations up to date."

def book_appointment(parent_username, child_name, vaccine_type, appointment_date):
    appointment_info = {
        "parent_username": parent_username,
        "child_name": child_name,
        "vaccine_type": vaccine_type,
        "appointment_date": appointment_date
    }
    appointments.append(appointment_info)
    return f"Appointment for {vaccine_type} on {appointment_date} booked successfully."

def get_reminders():
    reminders = []
    current_date = datetime.now().date()
    for appointment in appointments:
        days_until = (appointment["appointment_date"] - current_date).days
        if days_until <= 7:  # Remind 7 days before
            reminders.append({
                "parent_username": appointment["parent_username"],
                "child_name": appointment["child_name"],
                "vaccine_type": appointment["vaccine_type"],
                "appointment_date": appointment["appointment_date"]
            })
    return reminders

def update_vaccination_record(parent_username, child_name, vaccine_type):
    for child in children[parent_username]:
        if child["name"] == child_name:
            child["vaccinations"].append(vaccine_type)
            return f"Vaccination record for {vaccine_type} updated."
    return "Child not found."

def view_vaccination_history(parent_username, child_name):
    for child in children[parent_username]:
        if child["name"] == child_name:
            return child["vaccinations"]
    return "Child not found."

# Main Function to Handle User Input
def main():
    while True:
        print("\nChild Vaccination Management System")
        print("1. User Registration")
        print("2. User Login")
        print("3. Add Child")
        print("4. Suggest Next Vaccine")
        print("5. Book Appointment")
        print("6. Get Reminders")
        print("7. Update Vaccination Record")
        print("8. View Vaccination History")
        print("9. Exit")
        
        try:
            choice = int(input("Enter your choice (1-9): "))
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 9.")
            continue
        
        if choice == 1:
            username = input("Enter username: ")
            password = input("Enter password: ")
            print(register(username, password))
        
        elif choice == 2:
            username = input("Enter username: ")
            password = input("Enter password: ")
            print(login(username, password))
        
        elif choice == 3:
            parent_username = input("Enter parent username: ")
            child_name = input("Enter child name: ")
            dob = input("Enter child's date of birth (YYYY-MM-DD): ")
            try:
                dob = datetime.strptime(dob, '%Y-%m-%d').date()
            except ValueError:
                print("Invalid date format. Please use YYYY-MM-DD.")
                continue
            print(add_child(parent_username, child_name, dob))
        
        elif choice == 4:
            dob = input("Enter child's date of birth (YYYY-MM-DD): ")
            try:
                dob = datetime.strptime(dob, '%Y-%m-%d').date()
            except ValueError:
                print("Invalid date format. Please use YYYY-MM-DD.")
                continue
            print(suggest_next_vaccine(dob))
        
        elif choice == 5:
            parent_username = input("Enter parent username: ")
            child_name = input("Enter child name: ")
            vaccine_type = input("Enter vaccine type: ")
            appointment_date = input("Enter appointment date (YYYY-MM-DD): ")
            try:
                appointment_date = datetime.strptime(appointment_date, '%Y-%m-%d').date()
            except ValueError:
                print("Invalid date format. Please use YYYY-MM-DD.")
                continue
            print(book_appointment(parent_username, child_name, vaccine_type, appointment_date))
        
        elif choice == 6:
            reminders = get_reminders()
            if reminders:
                for reminder in reminders:
                    print(f"Reminder: {reminder}")
            else:
                print("No upcoming reminders.")
        
        elif choice == 7:
            parent_username = input("Enter parent username: ")
            child_name = input("Enter child name: ")
            vaccine_type = input("Enter vaccine type: ")
            print(update_vaccination_record(parent_username, child_name, vaccine_type))
        
        elif choice == 8:
            parent_username = input("Enter parent username: ")
            child_name = input("Enter child name: ")
            history = view_vaccination_history(parent_username, child_name)
            if isinstance(history, list):
                if history:
                    print(f"Vaccination history for {child_name}: {history}")
                else:
                    print("No vaccinations recorded.")
            else:
                print(history)
        
        elif choice == 9:
            print("Exiting the system.")
            break
        
        else:
            print("Invalid choice. Please enter a number between 1 and 9.")

if __name__ == "__main__":
    main()

