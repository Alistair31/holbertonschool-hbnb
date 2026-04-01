/* 
  This is a SAMPLE FILE to get you started.
  Please, follow the project instructions to complete the tasks.
*/

document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            if (loginForm.checkValidity()) {
                const formData = new FormData(loginForm);
                const data = {
                    email: formData.get('email'),
                    password: formData.get('password')
                };
                loginUser(data.email, data.password);
            }
        });
    }

    const priceFilter = document.getElementById('price-filter');
    if (priceFilter) {
        priceFilter.addEventListener('change', (event) => {
            selectPlacesByPrice(event.target.value);
        });
    }
    if (document.getElementById('place-details')) {
        checkAuthForPlace();
    } else {
        checkAuthentication();
    }

    const reviewForm = document.getElementById('review-form');
    if (reviewForm && window.location.pathname.includes('add_review')) {
        const token = checkAuthForReview();
        const placeId = getPlaceIdFromURL();
        reviewForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            const formData = new FormData(reviewForm);
            const reviewData = {
                comment: formData.get('review-text'),
                rating: formData.get('rating')
            };
            await submitReview(token, placeId, reviewData);
        });
    }
});
	
async function loginUser(email, password) {
	const response = await fetch('http://127.0.0.1:5000/api/v1/auth/login', {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json'
		},
		body: JSON.stringify({ email, password })
	});
	console.log('response.ok:', response.ok, 'status:', response.status);
	if (response.ok) {
		const data = await response.json();
		console.log('data:', data);
		document.cookie = `access_token=${data.access_token}; path=/`;
		console.log('cookie set, redirecting...');
		window.location.href = '/index';
	} else {
		alert('Login failed. Please check your credentials and try again.');
	}
}

function checkAuthentication() {
    const token = getCookie('access_token');
    const loginLink = document.getElementById('login-link');
    if (!loginLink) return;

    if (!token) {
        loginLink.style.display = 'block';
    } else {
        loginLink.style.display = 'none';
        fetchPlaces(token);
    }
}

function getCookie(name) {
	const value = `; ${document.cookie}`;
	const parts = value.split(`; ${name}=`);
	if (parts.length === 2) return parts.pop().split(';').shift();
}

async function fetchPlaces(token) {
    const response = await fetch('http://127.0.0.1:5000/api/v1/places', {
        headers: {
            'Authorization': `Bearer ${token}`
        }
    });
    if (!response.ok) {
        console.error('Failed to fetch places:', response.status);
        return;
    }
    const data = await response.json();
    displayPlaces(data);
}

function displayPlaces(places) {
	  const placesList = document.getElementById('places-list');

	  // Clear the container
	  placesList.innerHTML = '';

	  places.forEach(place => {
		  const placeElement = document.createElement('div');
		  placeElement.setAttribute('data-price', place.price);
		  placeElement.className = 'place-card';
		  placeElement.innerHTML = `
			  <h3>${place.name}</h3>
			  <p>Price: $${place.price}</p>
			  <button class="details-button">View Details</button>
		  `;
		  placeElement.querySelector('.details-button').addEventListener('click', () => {
			  window.location.href = `/place?place_id=${place.id}`;
		  });
		  placesList.appendChild(placeElement);
	  });
  }

function selectPlacesByPrice(selectedPrice) {
    const cards = document.querySelectorAll('.place-card');
    cards.forEach(card => {
        const cardPrice = card.dataset.price;
        if (selectedPrice === '' || selectedPrice === 'all' || parseFloat(cardPrice) <= parseFloat(selectedPrice)) {
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
        }
    });
}

function getPlaceIdFromURL() {
	const urlParams = new URLSearchParams(window.location.search);
	return urlParams.get('place_id');
	
   }

function checkAuthForPlace() {
    const token = getCookie('access_token');
    const addReviewSection = document.getElementById('add-review');
    if (!token) {
        addReviewSection.style.display = 'none';
    } else {
        addReviewSection.style.display = 'block';
        const placeId = getPlaceIdFromURL();
        fetchPlaceDetails(token, placeId);
    }
}

async function fetchPlaceDetails(token, placeId) {
    const response = await fetch(`http://127.0.0.1:5000/api/v1/places/${placeId}`, {
		headers: {
			'Authorization': `Bearer ${token}`
		}
	});
	const place = await response.json();
	displayPlaceDetails(place);
}

function displayPlaceDetails(place) {
	const placeDetails = document.getElementById('place-details');
	placeDetails.innerHTML = `
		<h2>${place.name}</h2>
		<p><strong>Host:</strong> ${place.host}</p>
		<p><strong>Price:</strong> $${place.price} per night</p>
		<p><strong>Description:</strong> ${place.description}</p>
		<p><strong>Amenities:</strong> ${place.amenities}</p>
	`;
	const reviewsList = document.getElementById('reviews-list');
	reviewsList.innerHTML = '';
	place.reviews.forEach(review => {
    const reviewCard = document.createElement('div');
    reviewCard.className = 'review-card';
    reviewCard.innerHTML = `
        <p>${review.comment}</p>
        <p><strong>${review.user_name}</strong> - ${review.rating}/5</p>
    `;
    reviewsList.appendChild(reviewCard);
  });
}

function checkAuthForReview() {
    const token = getCookie('access_token');
    if (!token) {
        window.location.href = '/index';
    }
    return token;
}

async function submitReview(token, placeId, reviewData) {
	  const response = await fetch(`http://127.0.0.1:5000/api/v1/places/${placeId}/reviews`, {
		  method: 'POST',
		  headers: {
			  'Content-Type': 'application/json',
			  'Authorization': `Bearer ${token}`
		  },
		  body: JSON.stringify(reviewData)
	  });
	  handleResponse(response);
  }

function handleResponse(response) {
    if (response.ok) {
        alert('Review submitted successfully!');
        document.getElementById('review-form').reset();
    } else {
        alert('Failed to submit review');
    }
}

