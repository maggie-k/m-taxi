from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Simulated driver database with car seat availability (can later be replaced by a real database)
drivers = [
    {"name": "Jane Doe", "location": "Nairobi", "gender": "female", "has_car_seat": True},
    {"name": "John Smith", "location": "Downtown", "gender": "male", "has_car_seat": False},
    {"name": "Alex Taylor", "location": "Suburbs", "gender": "non-binary", "has_car_seat": True},
    {"name": "David Brown", "location": "Uptown", "gender": "male", "has_car_seat": True}
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/request_ride', methods=['GET', 'POST'])
def request_ride():
    if request.method == 'POST':
        user_name = request.form.get('name')
        user_location = request.form.get('location')
        preferred_gender = request.form.get('driver_gender')
        needs_car_seat = 'needs_car_seat' in request.form  # Check if car seat is needed

        # Find drivers that match the gender and car seat preference
        matching_drivers = [driver for driver in drivers 
                            if driver['gender'] == preferred_gender.lower() and 
                               (not needs_car_seat or driver['has_car_seat'])]

        # If no matching drivers, fallback to any driver
        if not matching_drivers:
            matching_drivers = [driver for driver in drivers if not needs_car_seat or driver['has_car_seat']]

        # Select the first matching driver
        matched_driver = matching_drivers[0]

        # Redirect to the ride details page with the driver's info
        return redirect(url_for('ride_details', 
                                user_name=user_name, 
                                driver_name=matched_driver['name'], 
                                driver_location=matched_driver['location']))

    return render_template('ride_request.html')

@app.route('/ride_details')
def ride_details():
    user_name = request.args.get('user_name')
    driver_name = request.args.get('driver_name')
    driver_location = request.args.get('driver_location')

    return render_template('ride_details.html', 
                           user_name=user_name, 
                           driver_name=driver_name, 
                           driver_location=driver_location)

if __name__ == '__main__':
    app.run(debug=True)
