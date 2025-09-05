from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import datetime, timedelta
import json
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Change this in production

# Sample movie data (Tollywood movies)
movies = [
    {
        "id": 1,
        "title": "RRR",
        "director": "S. S. Rajamouli",
        "cast": "N.T. Rama Rao Jr., Ram Charan, Ajay Devgn, Alia Bhatt",
        "description": "A fictional story about two Indian revolutionaries and their journey away from home before they started fighting for their country in the 1920s.",
        "duration": "187 min",
        "language": "Telugu",
        "genre": "Action, Drama",
        "rating": "4.8",
        "poster": "rrr.jpg",
        "banner": "rrr_banner.jpg",
        "showtimes": [
            {"time": "10:00 AM", "seats": 50},
            {"time": "01:30 PM", "seats": 50},
            {"time": "05:00 PM", "seats": 50},
            {"time": "08:30 PM", "seats": 50}
        ]
    },
    {
        "id": 2,
        "title": "Pushpa: The Rise",
        "director": "Sukumar",
        "cast": "Allu Arjun, Rashmika Mandanna, Fahadh Faasil",
        "description": "A laborer rises through the ranks of a red sandalwood smuggling syndicate, making some powerful enemies in the process.",
        "duration": "179 min",
        "language": "Telugu",
        "genre": "Action, Drama",
        "rating": "4.5",
        "poster": "pushpa.jpg",
        "banner": "pushpa_banner.jpg",
        "showtimes": [
            {"time": "09:30 AM", "seats": 50},
            {"time": "12:45 PM", "seats": 50},
            {"time": "04:15 PM", "seats": 50},
            {"time": "07:45 PM", "seats": 50}
        ]
    },
    {
        "id": 3,
        "title": "Baahubali 2: The Conclusion",
        "director": "S. S. Rajamouli",
        "cast": "Prabhas, Rana Daggubati, Anushka Shetty, Tamannaah",
        "description": "When Shiva, the son of Bahubali, learns about his heritage, he begins to look for answers. His story is juxtaposed with past events that unfolded in the Mahishmati Kingdom.",
        "duration": "167 min",
        "language": "Telugu",
        "genre": "Action, Drama",
        "rating": "4.9",
        "poster": "baahubali2.jpg",
        "banner": "baahubali2_banner.jpg",
        "showtimes": [
            {"time": "11:00 AM", "seats": 50},
            {"time": "02:30 PM", "seats": 50},
            {"time": "06:00 PM", "seats": 50},
            {"time": "09:30 PM", "seats": 50}
        ]
    },
    {
        "id": 4,
        "title": "Ala Vaikunthapurramuloo",
        "director": "Trivikram Srinivas",
        "cast": "Allu Arjun, Pooja Hegde, Tabu",
        "description": "A man raised in a poor family discovers that he was switched at birth with a millionaire's son, leading to a series of conflicts and revelations.",
        "duration": "162 min",
        "language": "Telugu",
        "genre": "Action, Comedy, Drama",
        "rating": "4.3",
        "poster": "ala_vaikunthapurramuloo.jpg",
        "banner": "ala_vaikunthapurramuloo_banner.jpg",
        "showtimes": [
            {"time": "10:30 AM", "seats": 50},
            {"time": "01:45 PM", "seats": 50},
            {"time": "05:15 PM", "seats": 50},
            {"time": "08:45 PM", "seats": 50}
        ]
    },
    {
        "id": 5,
        "title": "Sarkaru Vaari Paata",
        "director": "Parasuram",
        "cast": "Mahesh Babu, Keerthy Suresh",
        "description": "A financial consultant takes on a powerful politician to recover his money and fight against corruption.",
        "duration": "163 min",
        "language": "Telugu",
        "genre": "Action, Drama",
        "rating": "4.2",
        "poster": "sarkaru_vaari_paata.jpg",
        "banner": "sarkaru_vaari_paata_banner.jpg",
        "showtimes": [
            {"time": "09:00 AM", "seats": 50},
            {"time": "12:15 PM", "seats": 50},
            {"time": "03:45 PM", "seats": 50},
            {"time": "07:15 PM", "seats": 50}
        ]
    },
    {
        "id": 6,
        "title": "KGF: Chapter 2",
        "director": "Prashanth Neel",
        "cast": "Yash, Sanjay Dutt, Raveena Tandon, Srinidhi Shetty",
        "description": "Rocky takes control of the Kolar Gold Fields and his newfound power makes the government as well as his enemies jittery. However, he must overcome threats from all sides to maintain control.",
        "duration": "168 min",
        "language": "Telugu",
        "genre": "Action, Drama",
        "rating": "4.7",
        "poster": "kgf2.jpg",
        "banner": "kgf2_banner.jpg",
        "showtimes": [
            {"time": "10:15 AM", "seats": 50},
            {"time": "01:45 PM", "seats": 50},
            {"time": "05:30 PM", "seats": 50},
            {"time": "09:00 PM", "seats": 50}
        ]
    }
]

# Sample theaters
theaters = [
    {"id": 1, "name": "PVR Cinemas", "location": "Hyderabad"},
    {"id": 2, "name": "INOX", "location": "Secunderabad"},
    {"id": 3, "name": "Cinepolis", "location": "Gachibowli"},
    {"id": 4, "name": "AMB Cinemas", "location": "Banjara Hills"}
]

# Booking data structure
bookings = []

@app.route('/')
def index():
    featured_movies = movies[:3]  # First 3 movies as featured
    return render_template('index.html', featured_movies=featured_movies, movies=movies)

@app.route('/movies')
def movies_list():
    return render_template('movies.html', movies=movies)

@app.route('/movie/<int:movie_id>')
def movie_detail(movie_id):
    movie = next((m for m in movies if m['id'] == movie_id), None)
    if not movie:
        flash('Movie not found!', 'error')
        return redirect(url_for('index'))
    return render_template('movie_detail.html', movie=movie, theaters=theaters)

@app.route('/booking/<int:movie_id>', methods=['GET', 'POST'])
def booking(movie_id):
    movie = next((m for m in movies if m['id'] == movie_id), None)
    if not movie:
        flash('Movie not found!', 'error')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        # Process booking
        showtime = request.form.get('showtime')
        theater_id = int(request.form.get('theater'))
        seats = int(request.form.get('seats'))
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        
        theater = next((t for t in theaters if t['id'] == theater_id), None)
        
        # Calculate total price
        price_per_ticket = 200  # Fixed price for simplicity
        total_price = seats * price_per_ticket
        
        # Create booking
        booking_id = len(bookings) + 1
        booking_data = {
            'id': booking_id,
            'movie': movie['title'],
            'theater': theater['name'],
            'showtime': showtime,
            'seats': seats,
            'name': name,
            'email': email,
            'phone': phone,
            'total_price': total_price,
            'booking_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        bookings.append(booking_data)
        
        # Update available seats (simplified)
        for st in movie['showtimes']:
            if st['time'] == showtime:
                st['seats'] -= seats
                break
        
        session['booking_id'] = booking_id
        return redirect(url_for('confirmation'))
    
    return render_template('booking.html', movie=movie, theaters=theaters)

@app.route('/confirmation')
def confirmation():
    booking_id = session.get('booking_id')
    if not booking_id or booking_id > len(bookings):
        flash('No booking found!', 'error')
        return redirect(url_for('index'))
    
    booking = bookings[booking_id - 1]
    return render_template('confirmation.html', booking=booking)

@app.route('/admin')
def admin():
    return render_template('admin.html', bookings=bookings, movies=movies)

if __name__ == '__main__':
    app.run(debug=True)
