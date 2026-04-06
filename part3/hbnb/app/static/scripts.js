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

    const createPlaceForm = document.getElementById('create-place-form');
    if (createPlaceForm && window.location.pathname.includes('create_place')) {
        const initToken = checkAuthForReview();
        fetchAmenities(initToken);
        createPlaceForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            const token = getCookie('access_token');
            if (!token) { window.location.href = '/login'; return; }
            const formData = new FormData(createPlaceForm);
            const selectedAmenities = Array.from(
                createPlaceForm.querySelectorAll('input[name="amenities"]:checked')
            ).map(cb => cb.value);
            const placeData = {
                title: formData.get('title'),
                description: formData.get('description'),
                price: parseFloat(formData.get('price')),
                latitude: parseFloat(formData.get('latitude')),
                longitude: parseFloat(formData.get('longitude')),
                amenities: selectedAmenities
            };
            const response = await fetch('/api/v1/places/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify(placeData)
            });
            if (response.ok) {
                const created = await response.json();
                const imageFiles = createPlaceForm.querySelector('#images').files;
                if (imageFiles.length > 0) {
                    const imgData = new FormData();
                    for (const file of imageFiles) {
                        imgData.append('images', file);
                    }
                    await fetch(`/upload_images/${created.id}`, {
                        method: 'POST',
                        headers: { 'Authorization': `Bearer ${getCookie('access_token')}` },
                        body: imgData
                    });
                }
                alert('Place created successfully!');
                window.location.href = '/index';
            } else {
                alert('Failed to create place');
            }
        });
    }

    const registerForm = document.getElementById('register-form');
    if (registerForm) {
        registerForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            const formData = new FormData(registerForm);
            const data = {
                first_name: formData.get('first_name'),
                last_name: formData.get('last_name'),
                email: formData.get('email'),
                password: formData.get('password')
            };
            const response = await fetch('/api/v1/auth/register', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
            if (response.ok) {
                alert('Account created! You can now log in.');
                window.location.href = '/login';
            } else {
                const err = await response.json();
                alert('Error: ' + (err.error || 'Registration failed'));
            }
        });
    }

    const reviewForm = document.getElementById('review-form');
    if (reviewForm) {
        const token = getCookie('access_token');
        const placeId = getPlaceIdFromURL();
        reviewForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            const formData = new FormData(reviewForm);
            const reviewData = {
                comment: formData.get('review-text'),
                rating: parseInt(formData.get('rating')) || 5
            };
            await submitReview(token, placeId, reviewData);
        });
    }
});
	
async function loginUser(email, password) {
	const response = await fetch('/api/v1/auth/login', {
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

    const createBtn = document.getElementById('create-place-btn');
    const logoutBtn = document.getElementById('logout-btn');

    if (logoutBtn) {
        logoutBtn.addEventListener('click', () => {
            document.cookie = 'access_token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
            window.location.href = '/login';
        });
    }

    if (!token || isTokenExpired(token)) {
        if (token) forceLogout();
        const path = window.location.pathname;
        if (!path.includes('login') && !path.includes('register')) {
            window.location.href = '/login';
        }
        return;
    }
    loginLink.style.display = 'none';
    const registerLink = document.getElementById('register-link');
    if (registerLink) registerLink.style.display = 'none';
    if (logoutBtn) logoutBtn.style.display = 'inline-block';
    if (createBtn) createBtn.style.display = 'inline-block';
    const claims = parseJwt(token);
    const addAmenityBtn = document.getElementById('add-amenity-btn');
    if (addAmenityBtn && claims.is_admin) {
        addAmenityBtn.style.display = 'inline-block';
        setupAmenityModal(token);
    }
    fetchPlaces(token);
}

function getCookie(name) {
	const value = `; ${document.cookie}`;
	const parts = value.split(`; ${name}=`);
	if (parts.length === 2) return parts.pop().split(';').shift();
}

async function fetchAmenities(token) {
    const response = await fetch('/api/v1/amenities/', {
        headers: { 'Authorization': `Bearer ${token}` }
    });
    if (!response.ok) return;
    const amenities = await response.json();
    const container = document.getElementById('amenities-list');
    if (!container) return;
    amenities.forEach(amenity => {
        const iconHtml = amenity.icon_url
            ? `<img src="${amenity.icon_url}" alt="${amenity.name}" class="amenity-logo">`
            : (amenity.icon || '🏠');
        const label = document.createElement('label');
        label.innerHTML = `
            <input type="checkbox" name="amenities" value="${amenity.id}">
            ${iconHtml} ${amenity.name}
        `;
        container.appendChild(label);
    });
}

function isTokenExpired(token) {
    try {
        const claims = parseJwt(token);
        if (!claims.exp) return false;
        return Date.now() / 1000 > claims.exp;
    } catch {
        return true;
    }
}

function forceLogout() {
    document.cookie = 'access_token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
    window.location.href = '/login';
}

async function apiFetch(url, options = {}) {
    const response = await fetch(url, options);
    if (response.status === 401) {
        forceLogout();
        return null;
    }
    return response;
}

function parseJwt(token) {
    try {
        const payload = token.split('.')[1];
        return JSON.parse(atob(payload));
    } catch {
        return {};
    }
}

async function fetchPlaces(token) {
    const response = await fetch('/api/v1/places/', {
        headers: {
            'Authorization': `Bearer ${token}`
        }
    });
    if (!response.ok) {
        console.error('Failed to fetch places:', response.status);
        return;
    }
    const data = await response.json();
    displayPlaces(data, token);
}

function displayPlaces(places, token) {
    const placesList = document.getElementById('places-list');
    if (!placesList) return;
    const claims = token ? parseJwt(token) : {};
    const currentUserId = claims.sub;
    const isAdmin = claims.is_admin || false;
    placesList.innerHTML = '';
    places.forEach(place => {
        const placeElement = document.createElement('div');
        placeElement.setAttribute('data-price', place.price);
        placeElement.className = 'place-card';
        const canDelete = isAdmin || currentUserId === place.owner_id;
        placeElement.innerHTML = `
            ${place.image_url ? `<img src="${place.image_url}" alt="${place.title}" class="place-img">` : ''}
            <div class="place-card-body">
                <div class="place-card-header">
                    <h3>${place.title}</h3>
                    <span class="place-price" aria-label="Price: ${place.price} gold per night">${place.price}<small> gold/night</small></span>
                </div>
                <button class="details-button" aria-label="View details for ${place.title}"><span class="btn-icon"><img src="/static/images/view_details.jpg" alt=""></span>View Details</button>
                ${canDelete ? `<button class="delete-button" aria-label="Delete ${place.title}"><span class="btn-icon"><img src="/static/images/delete.jpg" alt=""></span>Delete</button>` : ''}
            </div>
        `;
        placeElement.querySelector('.details-button').addEventListener('click', () => {
            window.location.href = `/place?place_id=${place.id}`;
        });
        if (canDelete) {
            placeElement.querySelector('.delete-button').addEventListener('click', async () => {
                if (confirm(`Delete "${place.title}" ?`)) {
                    await deletePlace(token, place.id);
                    placeElement.remove();
                }
            });
        }
        placesList.appendChild(placeElement);
    });
}

async function deletePlace(token, placeId) {
    const response = await fetch(`/api/v1/places/${placeId}`, {
        method: 'DELETE',
        headers: {
            'Authorization': `Bearer ${token}`
        }
    });
    if (!response.ok) {
        alert('Failed to delete place');
    }
}

function selectPlacesByPrice(selectedPrice) {
    const cards = document.querySelectorAll('.place-card');
    cards.forEach(card => {
        const cardPrice = parseFloat(card.dataset.price);
        if (!selectedPrice || selectedPrice === 'all' || cardPrice <= parseFloat(selectedPrice)) {
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

function updateHeaderButtons(token) {
    const loginLink = document.getElementById('login-link');
    const registerLink = document.getElementById('register-link');
    const logoutBtn = document.getElementById('logout-btn');
    if (loginLink) loginLink.style.display = token ? 'none' : 'block';
    if (registerLink) registerLink.style.display = token ? 'none' : 'inline-block';
    if (logoutBtn) logoutBtn.style.display = token ? 'inline-block' : 'none';
}


function checkAuthForPlace() {
    const token = getCookie('access_token');
    if (token && isTokenExpired(token)) { forceLogout(); return; }
    updateHeaderButtons(token);
    const logoutBtn = document.getElementById('logout-btn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', () => {
            document.cookie = 'access_token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
            window.location.href = '/login';
        });
    }
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
    const [placeResponse, reviewsResponse, imagesResponse] = await Promise.all([
        fetch(`/api/v1/places/${placeId}`, {
            headers: { 'Authorization': `Bearer ${token}` }
        }),
        fetch('/api/v1/reviews/', {
            headers: { 'Authorization': `Bearer ${token}` }
        }),
        fetch(`/place_images/${placeId}`)
    ]);
    const place = await placeResponse.json();
    const allReviews = await reviewsResponse.json();
    const images = await imagesResponse.json();
    place.reviews = allReviews.filter(r => r.place_id === placeId);
    place.all_images = images;
    displayPlaceDetails(place);
}

function displayPlaceDetails(place) {
	const placeDetails = document.getElementById('place-details');
	const images = place.all_images || [];
	let galleryHtml = '';
	if (images.length > 1) {
		galleryHtml = `<div class="image-gallery">${images.map(img =>
			`<img src="${img.image_url}" alt="${place.title}" class="gallery-img${img.is_primary ? ' gallery-img-primary' : ''}">`
		).join('')}</div>`;
	} else if (images.length === 1) {
		galleryHtml = `<img src="${images[0].image_url}" alt="${place.title}" class="place-img-detail">`;
	} else if (place.image_url) {
		galleryHtml = `<img src="${place.image_url}" alt="${place.title}" class="place-img-detail">`;
	}
	placeDetails.innerHTML = `
		<div class="place-card-header">
			<h2>${place.title}</h2>
			<span class="place-price">${place.price}<small> gold/night</small></span>
		</div>
		${galleryHtml}
		<p><strong>Host:</strong> ${place.host || 'Unknown'}</p>
		<p><strong>Description:</strong> ${place.description}</p>
		<div class="amenities-section">
			<strong>Amenities:</strong>
			<div class="amenities-icons">
				${place.amenities && place.amenities.length
					? place.amenities.map(a => {
						const iconHtml = a.icon_url
							? `<img src="${a.icon_url}" alt="" class="amenity-logo">`
							: `<span aria-hidden="true">${a.icon || '🏠'}</span>`;
						return `<span class="amenity-badge" aria-label="${a.name}">${iconHtml} ${a.name}</span>`;
					}).join('')
					: '<span>None</span>'}
			</div>
		</div>
	`;
	const reviewsList = document.getElementById('reviews-list');
	reviewsList.innerHTML = '';
	const reviews = place.reviews || [];
	reviews.forEach(review => {
    const reviewCard = document.createElement('div');
    reviewCard.className = 'review-card';
    reviewCard.innerHTML = `
        <p>${review.text}</p>
        <p><strong>${review.user_name}</strong> - ${review.rating}/5</p>
    `;
    reviewsList.appendChild(reviewCard);
  });
}

function checkAuthForReview() {
    const token = getCookie('access_token');
    if (!token || isTokenExpired(token)) {
        forceLogout();
        return null;
    }
    return token;
}

async function submitReview(token, placeId, reviewData) {
    const response = await fetch('/api/v1/reviews/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
            text: reviewData.comment,
            rating: reviewData.rating,
            place_id: placeId
        })
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

function setupAmenityModal(token) {
    const modal = document.getElementById('amenity-modal');
    const openBtn = document.getElementById('add-amenity-btn');
    const closeBtn = document.getElementById('amenity-modal-close');
    const form = document.getElementById('amenity-form');

    const iconFileInput = document.getElementById('amenity-icon-file');
    const iconPreview = document.getElementById('amenity-icon-preview');
    if (iconFileInput) {
        iconFileInput.addEventListener('change', () => {
            const file = iconFileInput.files[0];
            if (file) {
                iconPreview.src = URL.createObjectURL(file);
                iconPreview.style.display = 'block';
            } else {
                iconPreview.style.display = 'none';
            }
        });
    }

    openBtn.addEventListener('click', () => {
        modal.style.display = 'flex';
    });
    closeBtn.addEventListener('click', () => {
        modal.style.display = 'none';
        form.reset();
        if (iconPreview) iconPreview.style.display = 'none';
    });
    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            modal.style.display = 'none';
            form.reset();
            if (iconPreview) iconPreview.style.display = 'none';
        }
    });
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const name = document.getElementById('amenity-name').value.trim();
        const icon = document.getElementById('amenity-icon').value.trim() || '🏠';
        const response = await fetch('/api/v1/amenities/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ name, icon })
        });
        if (!response.ok) {
            const err = await response.json();
            alert('Error: ' + (err.error || 'Failed to create amenity'));
            return;
        }
        const created = await response.json();
        const iconFile = iconFileInput && iconFileInput.files[0];
        if (iconFile) {
            const imgData = new FormData();
            imgData.append('icon', iconFile);
            await fetch(`/upload_amenity_icon/${created.id}`, {
                method: 'POST',
                headers: { 'Authorization': `Bearer ${token}` },
                body: imgData
            });
        }
        alert(`Amenity "${name}" created successfully!`);
        modal.style.display = 'none';
        form.reset();
        if (iconPreview) iconPreview.style.display = 'none';
    });
}

