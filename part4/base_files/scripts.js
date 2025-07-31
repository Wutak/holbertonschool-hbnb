/* 
  This is a SAMPLE FILE to get you started.
  Please, follow the project instructions to complete the tasks.
*/

document.addEventListener('DOMContentLoaded', () => {
    checkAuthentication();
    populatePriceFilter();
});

// --- Verify if a token is in the Cookies ---
function checkAuthentication() {
    const token = getCookie('token');
    const loginLink = document.getElementById('login-link');

    if (!token) {
        loginLink.style.display = 'inline-block';
    } else {
        loginLink.style.display = 'none';
        fetchPlaces(token);
    }
}

// --- Read a Cookie's value by it's name ---
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}

// --- Fetching places from API ---
async function fetchPlaces(token) {
    try {
        const response = await fetch('https://your-api-url/places', {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        });

        if (response.ok) {
            const places = await response.json();
            displayPlaces(places);
        } else {
            console.error('Failed to fetch places:', response.statusText);
        }
    } catch (error) {
        console.error('Error fetching places:', error);
    }
}

// --- Display places in #places-list ---
function displayPlaces(places) {
    const placesList = document.getElementById('places-list');
    placesList.innerHTML = ''; // Clear current content

    places.forEach(place => {
        const placeDiv = document.createElement('div');
        placeDiv.className = 'place-details';
        placeDiv.setAttribute('data-price', place.price);

        placeDiv.innerHTML = `
            <h3>${place.name}</h3>
            <p><strong>Location:</strong> ${place.location}</p>
            <p><strong>Price:</strong> $${place.price}</p>
            <p>${place.description}</p>
        `;

        placesList.appendChild(placeDiv);
    });
}

// --- Fill the filter with price for the listener ---
function populatePriceFilter() {
    const filter = document.getElementById('price-filter');
    const priceOptions = [10, 50, 100, 'All'];

    priceOptions.forEach(price => {
        const option = document.createElement('option');
        option.value = price === 'All' ? 'all' : price;
        option.textContent = price === 'All' ? 'All' : `$${price}`;
        filter.appendChild(option);
    });

    filter.addEventListener('change', event => {
        const selectedPrice = event.target.value;
        const places = document.querySelectorAll('.place-details');

        places.forEach(place => {
            const price = parseFloat(place.getAttribute('data-price'));

            if (selectedPrice === 'all' || price <= parseFloat(selectedPrice)) {
                place.style.display = 'block';
            } else {
                place.style.display = 'none';
            }
        });
    });
}

document.addEventListener('DOMContentLoaded', () => {
    const placeId = getPlaceIdFromURL();
    const token = getCookie('token');

    if (!placeId) {
        alert('No place ID provided in the URL');
        return;
    }

    if (token) {
        document.getElementById('add-review').style.display = 'block';
    } else {
        document.getElementById('add-review').style.display = 'none';
    }

    fetchPlaceDetails(placeId, token);
});

// --- Fetch Place's ID from URL ---
function getPlaceIdFromURL() {
    const params = new URLSearchParams(window.location.search);
    return params.get('id');
}

// --- Fetch Cookie by it's name ---
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';')[0];
    return null;
}

// --- Fetch Place's details from API ---
async function fetchPlaceDetails(placeId, token) {
    try {
        const response = await fetch(`https://your-api-url/places/${placeId}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                ...(token && { 'Authorization': `Bearer ${token}` })
            }
        });

        if (response.ok) {
            const place = await response.json();
            displayPlaceDetails(place);
        } else {
            console.error('Failed to load place details');
        }
    } catch (error) {
        console.error('Error fetching place details:', error);
    }
}

// --- Display Place's details ---
function displayPlaceDetails(place) {
    const placeDetails = document.getElementById('place-details');
    placeDetails.innerHTML = ''; // Clear previous content

    const name = document.createElement('h2');
    name.textContent = place.name;

    const description = document.createElement('p');
    description.textContent = place.description;

    const location = document.createElement('p');
    location.innerHTML = `<strong>Location:</strong> ${place.location}`;

    const price = document.createElement('p');
    price.innerHTML = `<strong>Price:</strong> $${place.price}`;

    // Amenities
    const amenitiesDiv = document.createElement('div');
    amenitiesDiv.classList.add('amenities');
    if (place.amenities && place.amenities.length > 0) {
        place.amenities.forEach(amenity => {
            const img = document.createElement('img');
            img.src = `images/${amenity}.png`; // Assuming icons match the amenity names
            img.alt = amenity;
            img.title = amenity;
            amenitiesDiv.appendChild(img);
        });
    }

    // Append all
    placeDetails.appendChild(name);
    placeDetails.appendChild(location);
    placeDetails.appendChild(price);
    placeDetails.appendChild(description);
    placeDetails.appendChild(amenitiesDiv);

    // Show Reviews
    displayReviews(place.reviews || []);
}

// --- Display users Reviews ---
function displayReviews(reviews) {
    const reviewsSection = document.getElementById('reviews');
    const heading = document.getElementById('reviews-heading');

    if (!reviews.length) {
        heading.textContent = 'No reviews yet.';
        return;
    }

    reviews.forEach(review => {
        const reviewCard = document.createElement('div');
        reviewCard.classList.add('review-card');
        reviewCard.innerHTML = `
            <p><strong>Rating:</strong> ${review.rating} Star${review.rating > 1 ? 's' : ''}</p>
            <p>${review.text}</p>
        `;
        reviewsSection.appendChild(reviewCard);
    });
}
