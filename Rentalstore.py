import datetime
import logging
import os

logging.basicConfig(filename='car_rental_system.log', level=logging.INFO)

def display_cars():
    try:
        print("--------------------------------------------------------------------------------------------------------------------")
        print("Car ID\t\tBrand\t\tModel\t\tManufactured Year\t\tPrice/Day\t\tStatus")
        print("--------------------------------------------------------------------------------------------------------------------")
        with open('carstore.txt', 'r') as file:
            for line in file:
                print("\t\t".join(line.strip().split(", ")))
        print("--------------------------------------------------------------------------------------------------------------------")
        logging.info("Displayed available cars")
    except FileNotFoundError:
        print("Error: Unable to display available cars. Please contact support for assistance.")
        logging.error("carstore.txt not found")
    except Exception as e:
        print(f"Error: An unexpected error occurred.")
        logging.error(f"Error displaying available cars: {e}")

def generate_invoice(transaction_type, car_id, brand, model, year, price_per_day, customer_name, duration, total_amount):
    try:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        invoice_file = f"{transaction_type}_invoice_{timestamp}.txt"
        with open(invoice_file, 'w') as invoice:
            invoice.write(f"{transaction_type.capitalize()} Invoice\n")
            invoice.write(f"Car ID: {car_id}\n")
            invoice.write(f"Brand: {brand}\n")
            invoice.write(f"Model: {model}\n")
            invoice.write(f"Manufactured Year: {year}\n")
            invoice.write(f"Price Per Day: NPR {price_per_day}\n")
            invoice.write(f"Customer Name: {customer_name}\n")
            invoice.write(f"Date and Time of {transaction_type}: {datetime.datetime.now()}\n")
            invoice.write(f"Duration of Rent: {duration} days\n")
            invoice.write(f"Total Amount: NPR {total_amount}\n")
        logging.info(f"Generated {transaction_type} invoice: {invoice_file}")
        return invoice_file
    except Exception as e:
        print(f"Error: Unable to generate {transaction_type} invoice. Please contact support for assistance.")
        logging.error(f"Error generating {transaction_type} invoice: {e}")

def update_carstore(car_id, new_status):
    try:
        with open('carstore.txt', 'r') as file:
            cars = [line.strip().split(", ") for line in file]
        with open('carstore.txt', 'w') as file:
            for car in cars:
                if car[0] == car_id:
                    car[-1] = new_status
                file.write(", ".join(car) + "\n")
        logging.info("Updated carstore.txt after transaction")
    except Exception as e:
        print(f"Error: Unable to update carstore.txt. Please contact support for assistance.")
        logging.error(f"Error updating carstore.txt: {e}")

def rent_or_return_car(transaction_type, car_id, duration, customer_name):
    try:
        total_amount, car_found = 0, False
        # Read car information from carstore.txt
        with open('carstore.txt', 'r') as file:
            cars = [line.strip().split(", ") for line in file]
        # Loop through each car to find the specified car_id
        for car in cars:
            if car[0] == car_id:
                car_found = True
                if transaction_type == "rent":
                    # Check if the car is available for rent
                    if car[-1] == "Not Available":
                        print(f"Error: Car {car_id} is currently not available for rent.")
                        return
                    price_per_day = int(car[-2])
                    total_amount += price_per_day * duration
                    new_status = "Not Available"
                else:  # transaction_type == "return"
                    new_status = "Available"
                    total_amount += int(car[-2]) * duration
                # Update car status
                update_carstore(car_id, new_status)
                # Generate invoice for the transaction
                invoice_file = generate_invoice(transaction_type, car[0], car[1], car[2], car[3], car[-2], customer_name, duration, total_amount)
                print(f"Success: Car {car_id} has been {'rented to' if transaction_type == 'rent' else 'returned by'} {customer_name}. Invoice generated: {invoice_file}")
                logging.info(f"Car {car_id} {transaction_type}ed by {customer_name}")
                return
        if not car_found:
            print(f"Error: Car {car_id} not found.")
    except Exception as e:
        print(f"Error: Unable to complete the {transaction_type} process. Please contact support for assistance.")
        logging.error(f"Error {transaction_type}ing car: {e}")

def view_invoices():
    try:
        print("\nList of Generated Invoices:")
        invoices = [file for file in os.listdir() if file.endswith(".txt") and ("rent_invoice" in file or "return_invoice" in file)]
        if invoices:
            for idx, invoice in enumerate(invoices, 1):
                print(f"{idx}. {invoice}")
            choice = input("Enter the number of the invoice to view its content, or enter '0' to return to the main menu: ")
            if choice.isdigit():
                choice = int(choice)
                if 0 < choice <= len(invoices):
                    invoice_file = invoices[choice - 1]
                    with open(invoice_file, 'r') as file:
                        print("\nInvoice Content:")
                        print(file.read())
                elif choice != 0:
                    print("Invalid choice.")
            else:
                print("Invalid input.")
        else:
            print("No invoices found.")
    except Exception as e:
        print(f"Error: Unable to view invoices. Please contact support for assistance.")
        logging.error(f"Error viewing invoices: {e}")

def get_rental_info_from_invoices():
    rental_info = {}
    try:
        invoices = [file for file in os.listdir() if file.endswith(".txt") and ("rent_invoice" in file or "return_invoice" in file)]
        for invoice_file in invoices:
            with open(invoice_file, 'r') as file:
                lines = file.readlines()
                car_id = lines[1].split(":")[1].strip()
                customer_name = lines[6].split(":")[1].strip()
                transaction_type = lines[0].split()[0].lower()
                if car_id not in rental_info:
                    rental_info[car_id] = {"customer": customer_name, "transaction_type": transaction_type}
                else:
                    # If car is already rented/returned by someone else, update the info
                    if transaction_type == "rent":
                        rental_info[car_id] = {"customer": customer_name, "transaction_type": transaction_type}
        return rental_info
    except Exception as e:
        print(f"Error: Unable to retrieve rental information from invoices. Please contact support for assistance.")
        logging.error(f"Error retrieving rental information from invoices: {e}")

def main():
    try:
        while True:
            print("\nCar Rental System")
            print("1. Display Available Cars")
            print("2. Rent Car")
            print("3. Return Car")
            print("4. View Invoices")
            print("5. Quick View Rented Cars info.")
            print("6. Exit")
            choice = input("Enter your choice: ")
            if choice == '1':
                print("\nAvailable Cars:")
                display_cars()
            elif choice in ['2', '3']:
                transaction_type = "rent" if choice == '2' else "return"
                car_id = input(f"Enter Car ID to {transaction_type}: ")
                duration = int(input("Enter duration of rent (in days): ")) if transaction_type == "rent" else 0
                customer_name = input("Enter customer name: ")
                rent_or_return_car(transaction_type, car_id, duration, customer_name)
            elif choice == '4':
                view_invoices()
            elif choice == '5':
                rental_info = get_rental_info_from_invoices()
                if rental_info:
                    print("\nRental Information from Invoices:")
                    for car_id, info in rental_info.items():
                        print(f"Car ID: {car_id}, Rented by: {info['customer']}, Transaction Type: {info['transaction_type']}")
                else:
                    print("No rental information found in invoices.")
            elif choice == '6':
                break
            else:
                print("Error: Invalid choice. Please enter a valid option.")
                logging.error("Invalid choice entered")
    except KeyboardInterrupt:
        print("\nExiting...")
        logging.info("Exiting the Car Rental System")
    except Exception as e:
        print(f"Error: An unexpected error occurred. Please contact support for assistance.")
        logging.error(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()
