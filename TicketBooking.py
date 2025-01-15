import pymongo 
import sys 
client = pymongo.MongoClient("mongodb://localhost:27017/") 
db = client["ticket_booking_system"] 
users_collection = db["users"] 
bus_collection = db["Bus"] 
flight_collection = db["Flight"] 
train_collection = db["Train"] 
booked_tickets_collection = db["booked_tickets"] 
 
# Function to register a new user 
def register(): 
    name = input("Enter name: ")  # Input user's name 
    age = input("Enter age: ")  # Input user's age 
    email = input("Enter email: ")  # Input user's email 
    username = input("Create username: ")  # Create username 
    while True: 
        password = input("Enter password: ")  # Input password 
        password1 = input("Re-enter password: ")  # Re-enter password for confirmation 
        if password != password1: 
            print("Password does not match")  # Print message if passwords don't match 
        else: 
            break  # Break the loop if passwords match 
    user = {"username": username, "password": password, "name": name, "age": age}  # Create user object 
    users_collection.insert_one(user)  # Insert user into the collection 
    print("Registration successful!")  # Print success message 
 
# Function to login a user 
def login(): 
    username = input("Enter username: ")  # Input username 
    password = input("Enter password: ")  # Input password 
    user = users_collection.find_one({"username": username, "password": password})  # Find user in the collection 
     
    if user: 
        if username == "Dhruv" and password == "Dhruv@30":  # Check if admin login 
            print("Admin login successful!")  # Print admin login success message 
            admin_menu()  # Call admin menu function 
            return "admin"  # Return "admin" to identify admin login 
        else: 
            print("Login successful!")  # Print login success message 
            print("hii!", username, "welcome to UPES ticket booking system")  # Print welcome message 
            return username  # Return username 
    else: 
        print("Invalid username or password.")  # Print message for invalid credentials 
        return None  # Return None if login fails 
 
# Function to book a ticket 
def book_ticket(username): 
    while True: 
        if username: 
            print("\nTransportation Modes:") 
            print("1. Bus") 
            print("2. Train") 
            print("3. Flight") 
            print("4. Back") 
            mode = input("Choose mode of transportation (1/2/3): ")  # Choose mode of transportation 
            if mode == "1": 
                book_bus_ticket(username)  # Call function to book a bus ticket 
            elif mode == "2": 
                book_train_ticket(username)  # Call function to book a train ticket 
            elif mode == "3": 
                book_flight_ticket(username)  # Call function to book a flight ticket 
            elif mode == "4": 
                ticket_menu(username)  # Go back to ticket menu 
            else: 
                print("Invalid choice.")  # Print message for invalid choice 
 
def book_bus_ticket(username): 
    mode = "bus"  # Set the mode of transportation to "bus" 
    while True: 
        source = input("Enter source station: ")  # Input source station 
        destination = input("Enter destination station: ")  # Input destination station 
         
        while True: 
            date = input("Enter date (YYYY-MM-DD): ") 
            date_parts = date.split("-") 
            if len(date_parts) == 3: 
                year = date_parts[0] 
                month = date_parts[1] 
                day = date_parts[2] 
 
                if int(year) >= 2024: 
                    break 
                else: 
                    print("Invalid year. Please enter a year greater than or equal to 2024.") 
                 
                if 1 <= int(month) <= 12: 
                    break 
                else: 
                    print("Invalid month. Please enter a month between 1 to 12.") 
                 
                if 1 <= int(day) <= 30: 
                    break 
                else: 
                    print("Invalid date. Please enter a date between 1 to 30.") 
            else: 
                print("Invalid date format. Please enter date in YYYY-MM-DD format.")  # Print the date 
         
        # Find buses available for the specified source and destination 
        buses = bus_collection.find({"source": source, "destination": destination}) 
        lst = list(buses) 
         
        if lst: 
            k = 1 
            for bus in lst: 
                # Print available buses with their details 
                print(f"slot {k} --> Source: {bus['source']}, Destination: {bus['destination']}, Time: {bus['time']}, Price per passenger: {bus['price']}") 
                k += 1 
 
            ch = int(input("Enter Choice: "))  # Get user choice 
            ch -=1 
            while True: 
                if 0 <= ch < len(lst): 
                    num_passengers = int(input("Enter the number of passengers: "))  # Get number of passengers 
                     
                    # Calculate total price based on the number of passengers 
                    total_price = num_passengers * lst[ch]['price'] 
                     
                    passengers = allocate_seats(num_passengers, mode, source, destination, date)  # Allocate seats 
                    # Book the selected bus 
                    print("Booked:", lst[ch]['source'], lst[ch]['destination'], lst[ch]['time'], "Rs.",total_price, "Date:", date) 
                    print("Passengers:") 
                    for passenger in passengers: 
                        # Print passenger details 
                        print(f"Name: {passenger['name']}, Age: {passenger['age']}, Seat: {passenger['seat']}") 
                    confirm = input("Do you want to book this bus? (1 for yes, 2 for no): ")  # Confirm booking 
                    if confirm == "1": 
                        booked_bus = lst[ch] 
                        book_ticket = { 
                            "username": username, 
                            "mode": "Bus", 
                            "source": source, 
                            "destination": destination, 
                            "date": date, 
                            "bus_number": booked_bus["bus_number"], 
                            "time": booked_bus["time"], 
                            "price": total_price,  # Update price with the total price 
                            "passengers": passengers 
                        } 
                        booked_tickets_collection.insert_one(book_ticket)  # Insert booking into collection 
                        print("Bus ticket booked successfully!")  # Print success message 
                    elif confirm == "2": 
                        print("Booking canceled.")  # Print cancellation message 
                    else: 
                        print("Invalid choice.")  # Print message for invalid choice 
                    break  # Exit the loop if the booking is successful 
                     
                else: 
                    print("Invalid choice. Please enter a valid slot number.")  # Print message for invalid choice 
            break 
        else: 
            print("No bus available for this route. Please enter valid source and destination.")  # Print message if no buses available 
 
# Function to book a flight ticket 
def book_flight_ticket(username): 
    mode = "flight"  # Set the mode of transportation to "flight" 
    while True: 
        source = input("Enter source station: ")  # Input source station 
        destination = input("Enter destination station: ")  # Input destination station 
         
        while True: 
            date = input("Enter date (YYYY-MM-DD): ") 
            date_parts = date.split("-") 
            if len(date_parts) == 3: 
                year = date_parts[0] 
                month = date_parts[1] 
                day = date_parts[2] 
 
                if int(year) >= 2024: 
                    break 
                else: 
                    print("Invalid year. Please enter a year greater than or equal to 2024.") 
                 
                if 1 <= int(month) <= 12: 
                    break 
                else: 
                    print("Invalid month. Please enter a month between 1 to 12.") 
                 
                if 1 <= int(day) <= 30: 
                    break 
                else: 
                    print("Invalid date. Please enter a date between 1 to 30.") 
            else: 
                print("Invalid date format. Please enter date in YYYY-MM-DD format.") 
         
        # Find flights available for the specified source and destination 
        flights = flight_collection.find({"source": source, "destination": destination}) 
        lst = list(flights) 
         
        if lst: 
            k = 1 
            for flight in lst: 
                # Print available flights with their details 
                print(f"slot {k} --> Source: {flight['source']}, Destination: {flight['destination']}, Time: {flight['time']}, Price: {flight['price']}") 
                k += 1 
 
            ch = int(input("Enter Choice: "))  # Get user choice 
            ch -=1 
            while True: 
                if 0 <= ch < len(lst): 
                    num_passengers = int(input("Enter the number of passengers: "))  # Get number of passengers 
                    # Calculate total price based on the number of passengers 
                    total_price = num_passengers * lst[ch]['price'] 
                     
                    passengers = allocate_seats(num_passengers, mode, source, destination, date)  # Allocate seats 
                    # Book the selected flight 
                    print("Booked:", lst[ch]['source'], lst[ch]['destination'], lst[ch]['time'], "Rs.",total_price,"Date:",date) 
                    print("Passengers:") 
                    for passenger in passengers: 
                        # Print passenger details 
                        print(f"Name: {passenger['name']}, Age: {passenger['age']}, Seat: {passenger['seat']}") 
                    confirm = input("Do you want to book this flight? (1 for yes, 2 for no): ")  # Confirm booking 
                    if confirm == "1": 
                        booked_flight = lst[ch] 
                        book_ticket = { 
                            "username": username, 
                            "mode": "Flight", 
                            "source": source, 
                            "destination": destination, 
                            "date": date, 
                            "flight_number": booked_flight["flight_number"], 
                            "time": booked_flight["time"], 
                            "price": total_price, 
                            "passengers": passengers 
                        } 
                        booked_tickets_collection.insert_one(book_ticket)  # Insert booking into collection 
                        print("Flight ticket booked successfully!")  # Print success message 
                    elif confirm == "2": 
                        print("Booking canceled.")  # Print cancellation message 
                    else: 
                        print("Invalid choice.")  # Print message for invalid choice 
                    break  # Exit the loop if the booking is successful 
                else: 
                    print("Invalid choice. Please enter a valid slot number.")  # Print message for invalid choice 
                    break 
            break 
        else: 
            print("No flight available for this route. Please enter valid source and destination.")  # Print message if no flights available 
 
# Function to book a train ticket 
def book_train_ticket(username): 
    mode = "train"  # Set the mode of transportation to "train" 
    while True: 
        source = input("Enter source station: ")  # Input source station 
        destination = input("Enter destination station: ")  # Input destination station 
         
        while True: 
            date = input("Enter date (YYYY-MM-DD): ") 
            date_parts = date.split("-") 
            if len(date_parts) == 3: 
                year = date_parts[0] 
                month = date_parts[1] 
                day = date_parts[2] 
 
                if int(year) >= 2024: 
                    break 
                else: 
                    print("Invalid year. Please enter a year greater than or equal to 2024.") 
                 
                if 1 <= int(month) <= 12: 
                    break 
                else: 
                    print("Invalid month. Please enter a month between 1 to 12.") 
                 
                if 1 <= int(day) <= 30: 
                    break 
                else: 
                    print("Invalid date. Please enter a date between 1 to 30.") 
            else: 
                print("Invalid date format. Please enter date in YYYY-MM-DD format.")  # Print the date 
         
        # Find trains available for the specified source and destination 
        trains = train_collection.find({"source": source, "destination": destination}) 
        lst = list(trains) 
         
        if lst: 
            k = 1 
            for train in lst: 
                # Print available trains with their details 
                print(f"slot {k} --> Source: {train['source']}, Destination: {train['destination']}, Time: {train['time']}, Price: {train['price']}") 
                k += 1 
 
            ch = int(input("Enter Choice: "))  # Get user choice 
            ch -=1 
            while True: 
                if 0 <= ch < len(lst): 
                     
                    num_passengers = int(input("Enter the number of passengers: "))  # Get number of passengers 
                    # Calculate total price based on the number of passengers 
                    total_price = num_passengers * lst[ch]['price'] 
                     
                    passengers = allocate_seats(num_passengers, mode, source, destination, date)  # Allocate seats 
                    # Book the selected train 
                    print("Booked:", lst[ch]['source'], lst[ch]['destination'], lst[ch]['time'], "Rs.",total_price,"Date:",date) 
                    print("Passengers:") 
                    for passenger in passengers: 
                        # Print passenger details 
                        print(f"Name: {passenger['name']}, Age: {passenger['age']}, Seat: {passenger['seat']}") 
                    confirm = input("Do you want to book this train? (1 for yes, 2 for no): ")  # Confirm booking 
                    if confirm == "1": 
                        booked_train = lst[ch] 
                        book_ticket = { 
                            "username": username, 
                            "mode": "Train", 
                            "source": source, 
                            "destination": destination, 
                            "date": date, 
                            "train_number": booked_train["train_number"], 
                            "time": booked_train["time"], 
                            "price": total_price, 
                            "passengers": passengers 
                        } 
                        booked_tickets_collection.insert_one(book_ticket)  # Insert booking into collection 
                        print("Train ticket booked successfully!")  # Print success message 
                    elif confirm == "2": 
                        print("Booking canceled.")  # Print cancellation message 
                    else: 
                        print("Invalid choice.")  # Print message for invalid choice 
                    break  # Exit the loop if the booking is successful 
                else: 
                    print("Invalid choice. Please enter a valid slot number.")  # Print message for invalid choice 
                    break 
            break 
        else: 
            print("No train available for this route. Please enter valid source and destination.")  # Print message if no trains available 
 
# Function to allocate seats for passengers based on mode, source, destination, and date 
def allocate_seats(num_passengers, mode, source, destination, date): 
    # Define total available seats based on the mode of transportation 
    if mode == "bus": 
        total_seats = 50  # Total seats for buses 
    elif mode == "train": 
        total_seats = 100  # Total seats for trains 
    elif mode == "flight": 
        total_seats = 150  # Total seats for flights 
    else: 
        print("Invalid mode of transportation.") 
        return None  # Return None if mode is invalid 
 
    # Get already booked seats for the same mode, source, destination, and date 
    booked_seats = set() 
    booked_tickets = booked_tickets_collection.find({"mode": mode, "source": source, "destination": destination, "date": date}) 
    for ticket in booked_tickets: 
        for passenger in ticket['passengers']: 
            booked_seats.add(passenger['seat']) 
 
    available_seats = set(range(1, total_seats + 1)) - booked_seats  # Calculate available seats 
 
    # Check if there are enough available seats for the requested number of passengers 
    if len(available_seats) < num_passengers: 
        print("Sorry, there are not enough available seats for the requested number of passengers.") 
        return None 
 
    passengers = [] 
    for i in range(num_passengers): 
        passenger_name = input(f"Enter name of passenger {i+1}: ")  # Input passenger's name 
        passenger_age = int(input(f"Enter age of passenger {i+1}: "))  # Input passenger's age 
 
        # Find the next available seat 
        if available_seats: 
            seat_number = available_seats.pop() 
            passengers.append({"name": passenger_name, "age": passenger_age, "seat": seat_number})  # Add passenger details 
        else: 
            print("Sorry, all available seats are booked.") 
            return None 
 
    return passengers  # Return list of passengers with allocated seats 
 
# Function for the main menu 
def main_menu(): 
    while True: 
        print("\nMain Menu") 
        print("1. Register") 
        print("2. Login") 
        print("3. About Us") 
        print("4. Exit") 
        choice = input("Enter your choice: ")  # Input choice 
 
        if choice == "1": 
            register()  # Call register function 
        elif choice == "2": 
            username = login()  # Call login function 
            if username: 
                ticket_menu(username)  # If login successful, go to ticket menu 
        elif choice == "3": 
            display_about_us()  # Call function to display about us 
        elif choice == "4": 
            print("Thank you for using the ticket booking system.") 
            sys.exit()  # Exit the program 
        else: 
            print("Invalid choice. Please try again.")  # Print message for invalid choice 
 
# Function to display information about the company 
def display_about_us(): 
    print("\nAbout Us") 
    print("UPES TRAVEL AGENCY") 
    print("Address: 216B I,\n Second Floor,Splendor Forum,\n Plot Bearing No. 3,Jasola District Centre, Jasola,\n New Delhi-110025") 
    print("Contact: 18001028737") 
 
# Function for the ticket menu 
def ticket_menu(username): 
    while True: 
        print("\nTicket Menu") 
        print("1. Book Ticket") 
        print("2. View Tickets") 
        print("3. Cancel Booking") 
        print("4. Logout") 
        choice = input("Enter your choice: ")  # Input choice 
        print() 
 
        if choice == "1": 
            book_ticket(username)  # Call function to book a ticket 
        elif choice == "2": 
            view_tickets(username)  # Call function to view tickets 
        elif choice == "3": 
            cancel_booking(username)  # Call function to cancel booking 
        elif choice == "4": 
            print("Logged out successfully.") 
            main_menu()  # Go back to main menu 
        else: 
            print("Invalid choice. Please try again.")  # Print message for invalid choice 
 
# Function to cancel a booking for a user 
def cancel_booking(username): 
    # Input for selecting the mode of transportation 
    mode_choice = input("Enter mode of transportation (1 for bus, 2 for flight, 3 for train): ") 
 
    # Determine the mode based on user input 
    if mode_choice == '1': 
        mode = 'Bus' 
    elif mode_choice == '2': 
        mode = 'Flight' 
    elif mode_choice == '3': 
        mode = 'Train' 
    else: 
        print("Invalid mode selection.") 
        return 
 
    # Retrieve bookings for the user and mode 
    bookings = list(booked_tickets_collection.find({"username": username, "mode": mode})) 
 
    # If no bookings found, print a message and return 
    if not bookings: 
        print(f"No {mode} bookings found for this user.") 
        return 
 
    # Display existing bookings for the user 
    print("Existing bookings:") 
    for index, booking in enumerate(bookings, 1): 
        print(f"{index}. Source: {booking['source']}, Destination: {booking['destination']}, Date: {booking['date']}, Time: {booking['time']}") 
 
    # Input for selecting the booking to cancel 
    cancel_choice = input("Enter the number of booking to cancel: ") 
    if cancel_choice.isdigit(): 
        cancel_index = int(cancel_choice) - 1 
        if 0 <= cancel_index < len(bookings): 
            booking_to_cancel = bookings[cancel_index] 
 
            # Delete the booking 
            booked_tickets_collection.delete_one({"_id": booking_to_cancel["_id"]}) 
            print("Booking canceled successfully.") 
        else: 
            print("Invalid booking number.") 
    else: 
        print("Invalid input. Please enter a number.") 
 
# Function to view tickets booked by a user 
def view_tickets(username): 
    # Retrieve tickets booked by the user 
    user_tickets = booked_tickets_collection.find({"username": username}) 
 
    # Display details of each ticket 
    for ticket in user_tickets: 
        print("Ticket Number:", ticket['_id']) 
        print("Source:", ticket['source']) 
        print("Destination:", ticket['destination']) 
        print("Time:", ticket['time']) 
        print("Date:", ticket['date']) 
        print("Price:", ticket['price']) 
        mode = ticket['mode'] 
        print(f"{mode.capitalize()} number:", ticket[f"{mode.lower()}_number"]) 
        print("Passengers:") 
        for passenger in ticket['passengers']: 
            print(f"Name: {passenger['name']}, Age: {passenger['age']}, Seat number: {passenger['seat']}") 
        print() 
 
# Function to delete a route for a mode of transportation 
def delete_route(): 
    mode = input("Enter mode of transportation (1 for Bus / 2 for Flight / 3 for Train): ") 
    if mode not in ['1', '2', '3']: 
        print("Invalid mode of transportation.") 
        return 
 
    source = input("Enter source: ") 
    destination = input("Enter destination: ") 
 
    # Determine the collection and mode string based on the mode of transportation 
    if mode == '1': 
        collection = bus_collection 
        mode_str = 'Bus' 
    elif mode == '2': 
        collection = flight_collection 
        mode_str = 'Flight' 
    elif mode == '3': 
        collection = train_collection 
        mode_str = 'Train' 
 
    # Retrieve routes based on source and destination 
    routes = collection.find({"source": source, "destination": destination}) 
    routes_list = list(routes) 
 
    # If no routes found, print a message and return 
    if not routes_list: 
        print(f"No {mode_str} routes found for the given source and destination.") 
        return 
 
    # Display available routes 
    print(f"Available {mode_str} Routes:") 
    for i, route in enumerate(routes_list, 1): 
        if mode_str == 'Bus': 
            print(f"{i}. Source: {source}, Destination: {destination}, Price: {route['price']}, Bus Number: {route['bus_number']}") 
        elif mode_str == 'Flight': 
            print(f"{i}. Source: {source}, Destination: {destination}, Price: {route['price']}, Flight Number: {route['flight_number']}") 
        elif mode_str == 'Train': 
            print(f"{i}. Source: {source}, Destination: {destination}, Price: {route['price']}, Train Number: {route['train_number']}") 
 
    # Input for selecting the route to delete 
    choice = input("Enter the number of the route to delete: ") 
 
    if choice.isdigit(): 
        route_index = int(choice) - 1 
        if 0 <= route_index < len(routes_list): 
            route_to_delete = routes_list[route_index] 
 
            # Delete the route 
            collection.delete_one({"_id": route_to_delete["_id"]}) 
            print("Route deleted successfully.") 
        else: 
            print("Invalid route number.") 
    else: 
        print("Invalid input. Please enter a number.") 
 
#Function to handle admin menu options 
def admin_menu(): 
    while True: 
        print("\nAdmin Menu") 
        print("1. Add New Route") 
        print("2. Update Route Timing") 
        print("3. View All Routes") 
        print("4. Update Route Pricing") 
        print("5. Delete Existing Route") 
        print("6. View All Bookings") 
        print("7. View Route Statistics") 
        print("8. View details for specific vehicle") 
        print("9. Logout") 
        choice = input("Enter your choice: ") 
        print() 
 
        if choice == "1": 
            add_new_route() 
        elif choice == "2": 
            update_route_timing() 
        elif choice == "3": 
            view_all_routes() 
        elif choice == "4": 
            update_route_pricing() 
        elif choice == "5": 
            delete_route()  # Option to delete a route 
        elif choice == "6": 
            view_all_bookings() 
        elif choice == "7": 
            view_route_statistics()  # Option to view route statistics 
        elif choice == "8": 
            show_tickets_and_passengers() 
        elif choice == "9": 
            print("Logged out successfully.") 
            main_menu() 
        else: 
            print("Invalid choice. Please try again.") 
 
# Function to view statistics for different routes 
def view_route_statistics(): 
    # Count the total number of buses, flights, and trains 
    total_buses = bus_collection.count_documents({}) 
    total_flights = flight_collection.count_documents({}) 
    total_trains = train_collection.count_documents({}) 
 
    print("Vehicle Statistics:") 
    print(f"Total Buses: {total_buses}") 
    print(f"Total Flights: {total_flights}") 
    print(f"Total Trains: {total_trains}") 
    while True: 
         
        # Prompt the user to select a mode (bus, flight, or train) 
        mode = input("Select mode (1 for Bus / 2 for Flight / 3 for Train, 0 to exit): ") 
        if mode == '0': 
            print("Exiting...") 
            return 
        elif mode not in ['1', '2', '3']: 
            print("Invalid mode selection.") 
            continue 
 
        # Determine the collection and mode string based on the selected mode 
        if mode == '1': 
            collection = bus_collection 
            mode_str = 'Bus' 
        elif mode == '2': 
            collection = flight_collection 
            mode_str = 'Flight' 
        else: 
            collection = train_collection 
            mode_str = 'Train' 
 
        # Aggregate to count the number of vehicles per route 
        routes = collection.aggregate([ 
            {"$group": { 
                "_id": {"source": "$source", "destination": "$destination"}, 
                "count": {"$sum": 1} 
            }}, 
            {"$sort": {"_id.source": 1, "_id.destination": 1}} 
        ]) 
 
        # Display the results 
        total_routes = 0 
        print(f"\nNumber of {mode_str}s Available per Route:") 
        for route in routes: 
            total_routes += 1 
            print(f"\nSource: {route['_id']['source']}, Destination: {route['_id']['destination']}, Number of {mode_str}s: {route['count']}") 
 
        print(f"\nTotal Routes Available: {total_routes}") 
        print() 
 
# Function to display all bookings and a summary of total tickets and passengers for each mode of transportation 
def view_all_bookings(): 
    # Pipeline to aggregate total tickets and passengers for each mode 
    pipeline = [ 
        { 
            "$group": { 
                "_id": "$mode", 
                "total_tickets": {"$sum": 1}, 
                "total_passengers": {"$sum": {"$size": "$passengers"}}  # Count total passengers 
            } 
        } 
    ] 
 
    # Aggregate the bookings summary 
    bookings_summary = booked_tickets_collection.aggregate(pipeline) 
 
    print("Booking Summary:") 
    for summary in bookings_summary: 
        mode = summary["_id"] 
        total_tickets = summary["total_tickets"] 
        total_passengers = summary["total_passengers"] 
        print(f"Mode: {mode}, Total Tickets booked: {total_tickets}, Total Passengers: {total_passengers}") 
 
    # Retrieve all bookings 
    all_bookings = booked_tickets_collection.find({}) 
    all_bookings_list = list(all_bookings)  # Convert cursor to list to count 
    if len(all_bookings_list) == 0: 
        print("No bookings found.") 
        return 
 
    print("\nAll Bookings:") 
    index = 1 
    for booking in all_bookings_list: 
        print(f"{index}. Username: {booking['username']}, Mode: {booking['mode']}, Source: {booking['source']}, Destination: {booking['destination']}, Date: {booking['date']}, Time: Date: {booking['time']}") 
        mode = booking['mode'] 
        if mode == 'Bus': 
            print(f"   Bus Number: {booking['bus_number']}") 
        elif mode == 'Train': 
            print(f"   Train Number: {booking['train_number']}") 
        elif mode == 'Flight': 
            print(f"   Train Number: {booking['flight_number']}") 
 
        passengers = booking['passengers'] 
        passenger_count = len(passengers) 
        ticket_count = 1 if passenger_count > 0 else 0 
        print(f"   Passenger count: {passenger_count}") 
 
        if passengers: 
            print("   Passengers:") 
            for passenger in passengers: 
                print(f"      Name: {passenger['name']}, Age: {passenger['age']}, Seat: {passenger['seat']}") 
        else: 
            print("   No passengers.") 
        print() 
        index += 1 
 
# Function to display tickets and passengers details for a specific mode of transportation 
from bson import ObjectId 
 
def show_tickets_and_passengers(): 
    modes = {"1": "bus", "2": "flight", "3": "train"} 
 
    while True: 
        # Ask user for mode of transportation (bus/flight/train) 
        mode_input = input("Enter mode of transportation (1: bus, 2: flight, 3: train, 0: exit): ").strip() 
        if mode_input == "0": 
            print("Exiting.") 
            break 
        elif mode_input not in modes: 
            print("Invalid mode. Please enter 1, 2, 3, or 0.") 
            continue 
 
        mode = modes[mode_input] 
 
        # Aggregate to get distinct numbers and total tickets for the selected mode 
        pipeline = [ 
            {"$match": {f"{mode}_number": {"$exists": True}}}, 
            {"$group": {"_id": f"${mode}_number", "total_tickets": {"$sum": 1}}} 
        ] 
 
        distinct_numbers = booked_tickets_collection.aggregate(pipeline) 
 
        # Display all mode-specific numbers with their respective number of booked tickets 
        print(f"\n{mode.capitalize()} Numbers with Booked Tickets:") 
 
        for index, number_info in enumerate(distinct_numbers, 1): 
            number = number_info["_id"] 
            total_tickets = number_info["total_tickets"] 
            print(f"Slot => {index}. {mode.capitalize()} Number: {number}, Total Tickets Booked: {total_tickets}") 
 
        # Ask user to select a specific number or exit 
        while True: 
            choice = input(f"\nEnter a Slot number to show more details (enter '0' to exit): ") 
            if choice == "0": 
                print("Exiting.") 
                return 
            elif choice.isdigit() and 1 <= int(choice) <= index: 
                specific_number = distinct_numbers[int(choice) - 1]["_id"] 
                break 
            else: 
                print("Invalid input. Please enter a valid number or '0' to exit.") 
 
        # Find bookings for the specific mode and number 
        bookings = booked_tickets_collection.find({f"{mode}_number": specific_number}) 
 
        # Display passengers details for the specific number 
        print(f"\nPassengers Details for {mode.capitalize()} Number: {specific_number}:") 
        for booking in bookings: 
            passengers = booking.get("passengers", []) 
            print(f"Username: {booking['username']}, Mode: {booking['mode']}, Source: {booking['source']}, Destination: {booking['destination']}, Date: {booking['date']}, Time: {booking.get('time', '')}") 
 
            if passengers: 
                print("Passengers:") 
                for passenger in passengers: 
                    print(f"   Name: {passenger['name']}, Age: {passenger['age']}, Seat: {passenger['seat']}") 
            else: 
                print("No passengers for this booking.") 
 
            print() 
 
# Function to add a new route based on user input 
def add_new_route(): 
    mode = input("Enter mode of transportation (1 for Bus / 2 for Flight / 3 for Train): ") 
    if mode not in ['1', '2', '3']: 
        print("Invalid mode of transportation.") 
        return 
 
    # Mapping mode input to mode string 
    mode_map = {'1': 'Bus', '2': 'Flight', '3': 'Train'} 
    mode = mode_map[mode] 
 
    source = input("Enter source station: ") 
    destination = input("Enter destination station: ") 
    time = input("Enter departure time: ") 
    price = float(input("Enter ticket price: ")) 
 
    new_route = { 
        "source": source, 
        "destination": destination, 
        "time": time, 
        "price": price 
    } 
 
    # Depending on mode, prompt for specific vehicle number and insert the new route into the corresponding collection 
    if mode == 'Bus': 
        bus_number = input("Enter bus number: ") 
        new_route["bus_number"] = bus_number 
        bus_collection.insert_one(new_route) 
        print("New bus route added successfully!") 
    elif mode == 'Train': 
        train_number = input("Enter train number: ") 
        new_route["train_number"] = train_number 
        train_collection.insert_one(new_route) 
        print("New train route added successfully!") 
    elif mode == 'Flight': 
        flight_number = input("Enter flight number: ") 
        new_route["flight_number"] = flight_number 
        flight_collection.insert_one(new_route) 
        print("New flight route added successfully!") 
 
# Function to update the timing of a route 
def update_route_timing(): 
    mode = input("Enter mode of transportation (1 for Bus / 2 for Flight / 3 for Train): ") 
    if mode not in ['1', '2', '3']: 
        print("Invalid mode of transportation.") 
        return 
 
    source = input("Enter source: ") 
    destination = input("Enter destination: ") 
 
    # Determine the collection and mode string based on the mode of transportation 
    if mode == '1': 
        collection = bus_collection 
        mode_str = 'Bus' 
    elif mode == '2': 
        collection = flight_collection 
        mode_str = 'Flight' 
    elif mode == '3': 
        collection = train_collection 
        mode_str = 'Train' 
 
    # Retrieve routes based on source and destination 
    routes = collection.find({"source": source, "destination": destination}) 
    routes_list = list(routes) 
 
    # If no routes found, print a message and return 
    if not routes_list: 
        print(f"No {mode_str} routes found for the given source and destination.") 
        return 
 
    # Display available routes for the selected mode 
    print(f"Available {mode_str} Routes:") 
    for i, route in enumerate(routes_list, 1): 
        if mode_str == 'Bus': 
            print(f"{i}. Source: {source}, Destination: {destination}, Time: {route['time']}, Bus Number: {route['bus_number']}") 
        elif mode_str == 'Flight': 
            print(f"{i}. Source: {source}, Destination: {destination}, Time: {route['time']}, Flight Number: {route['flight_number']}") 
        elif mode_str == 'Train': 
            print(f"{i}. Source: {source}, Destination: {destination}, Time: {route['time']}, Train Number: {route['train_number']}") 
 
    # Input for selecting the route to update timing 
    choice = input("Enter the number of the route to update timing: ") 
 
    if choice.isdigit(): 
        route_index = int(choice) - 1 
        if 0 <= route_index < len(routes_list): 
            route_to_update = routes_list[route_index] 
            new_time = input("Enter new departure time: ") 
            collection.update_one({"_id": route_to_update["_id"]}, {"$set": {"time": new_time}}) 
            print("Route timing updated successfully.") 
        else: 
            print("Invalid route number.") 
    else: 
        print("Invalid input. Please enter a number.") 
 
# Function to update the pricing of a route 
def update_route_pricing(): 
    mode = input("Enter mode of transportation (1 for Bus / 2 for Flight / 3 for Train): ") 
    if mode not in ['1', '2', '3']: 
        print("Invalid mode of transportation.") 
        return 
 
    source = input("Enter source: ") 
    destination = input("Enter destination: ") 
 
    # Determine the collection and mode string based on the mode of transportation 
    if mode == '1': 
        collection = bus_collection 
        mode_str = 'Bus' 
    elif mode == '2': 
        collection = flight_collection 
        mode_str = 'Flight' 
    elif mode == '3': 
        collection = train_collection 
        mode_str = 'Train' 
 
    # Retrieve routes based on source and destination 
    routes = collection.find({"source": source, "destination": destination}) 
    routes_list = list(routes) 
 
    # If no routes found, print a message and return 
    if not routes_list: 
        print(f"No {mode_str} routes found for the given source and destination.") 
        return 
 
    # Display available routes for the selected mode 
    print(f"Available {mode_str} Routes:") 
    for i, route in enumerate(routes_list, 1): 
        if mode_str == 'Bus': 
            print(f"{i}. Source: {source}, Destination: {destination}, Price: {route['price']}, Bus Number: {route['bus_number']}") 
        elif mode_str == 'Flight': 
            print(f"{i}. Source: {source}, Destination: {destination}, Price: {route['price']}, Flight Number: {route['flight_number']}") 
        elif mode_str == 'Train': 
            print(f"{i}. Source: {source}, Destination: {destination}, Price: {route['price']}, Train Number: {route['train_number']}") 
 
    # Input for selecting the route to update pricing 
    choice = input("Enter the number of the route to update pricing: ") 
 
    if choice.isdigit(): 
        route_index = int(choice) - 1 
        if 0 <= route_index < len(routes_list): 
            route_to_update = routes_list[route_index] 
            new_price = float(input("Enter new ticket price: ")) 
            collection.update_one({"_id": route_to_update["_id"]}, {"$set": {"price": new_price}}) 
            print("Route pricing updated successfully.") 
        else: 
            print("Invalid route number.") 
    else: 
        print("Invalid input. Please enter a number.") 
 
# Function to view all routes for a selected mode of transportation 
def view_all_routes(): 
    while True: 
        mode = input("Choose mode of transportation (1 for Bus, 2 for Train, 3 for Flight, 0 to exit): ") 
        if mode == '0': 
            print("Exiting...") 
            return 
        elif mode not in ['1', '2', '3']: 
            print("Invalid mode of transportation.") 
        else: 
            # Determine the mode string and corresponding collection based on user input 
            if mode == '1': 
                mode_str = 'Bus' 
                routes = bus_collection.find({}) 
            elif mode == '2': 
                mode_str = 'Train' 
                routes = train_collection.find({}) 
            elif mode == '3': 
                mode_str = 'Flight' 
                routes = flight_collection.find({}) 
 
            # Display all routes for the selected mode 
            print(f"All {mode_str} routes:") 
            for route in routes: 
                print(f"Source: {route['source']}, Destination: {route['destination']}, Time: {route['time']}, Price: {route['price']}") 
 
# Entry point of the program 
if __name__ == "__main__": 
    main_menu() 