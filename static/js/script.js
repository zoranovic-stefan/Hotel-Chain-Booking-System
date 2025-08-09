document.addEventListener('DOMContentLoaded', function() {
  // Set default dates for the form
  const today = new Date();
  const tomorrow = new Date(today);
  tomorrow.setDate(tomorrow.getDate() + 1);
  
  document.getElementById('check-in').valueAsDate = today;
  document.getElementById('check-out').valueAsDate = tomorrow;
  
  // Load hotel chains and featured rooms
  loadHotelChains();
  loadFeaturedRooms();
  
  // Add event listener to search form
  document.getElementById('search-form').addEventListener('submit', function(e) {
      e.preventDefault();
      const destination = document.getElementById('destination').value;
      const checkIn = document.getElementById('check-in').value;
      const checkOut = document.getElementById('check-out').value;
      const guests = document.getElementById('guests').value;
      
      // In a real application, you would send this data to your backend
      alert(`Searching for hotels in ${destination} from ${checkIn} to ${checkOut} for ${guests} guest(s)`);
  });
});

// Mock data loading functions (replace with actual API calls)
function loadHotelChains() {
  // Simulate API call with setTimeout
  setTimeout(function() {
      const chains = [
          {
              id: 1,
              name: "Luxury Resort Collection",
              hotels: 12,
              location: "Multiple Locations",
              image: "https://source.unsplash.com/random/300x200/?luxury,hotel"
          },
          {
              id: 2,
              name: "Business Traveler Suites",
              hotels: 28,
              location: "Major Urban Centers",
              image: "https://source.unsplash.com/random/300x200/?business,hotel"
          },
          {
              id: 3,
              name: "Family Vacation Resorts",
              hotels: 15,
              location: "Family-Friendly Destinations",
              image: "https://source.unsplash.com/random/300x200/?family,resort"
          },
          {
              id: 4,
              name: "Beachside Getaways",
              hotels: 20,
              location: "Coastal Areas",
              image: "https://source.unsplash.com/random/300x200/?beach,hotel"
          },
          {
              id: 5,
              name: "Mountain Retreat Lodges",
              hotels: 8,
              location: "Mountain Regions",
              image: "https://source.unsplash.com/random/300x200/?mountain,lodge"
          }
      ];
      
      displayHotelChains(chains);
  }, 1000);
}

function displayHotelChains(chains) {
  const container = document.getElementById('hotel-chains-container');
  
  if (!chains || chains.length === 0) {
      container.innerHTML = '<p class="loading">No hotel chains found.</p>';
      return;
  }
  
  let html = '';
  chains.forEach(chain => {
      html += `
          <div class="card">
              <div class="card-image">
                  <img src="${chain.image}" alt="${chain.name}">
              </div>
              <div class="card-body">
                  <h3 class="card-title">${chain.name}</h3>
                  <p class="card-text"><i class="fas fa-hotel"></i> ${chain.hotels} Hotels</p>
                  <p class="card-text"><i class="fas fa-map-marker-alt"></i> ${chain.location}</p>
              </div>
              <div class="card-footer">
                  <button class="card-btn" onclick="viewHotelChain(${chain.id})">
                      <i class="fas fa-arrow-right"></i> View Hotels
                  </button>
              </div>
          </div>
      `;
  });
  
  container.innerHTML = html;
}

function loadFeaturedRooms() {
  // Simulate API call with setTimeout
  setTimeout(function() {
      const rooms = [
          {
              id: 101,
              name: "Deluxe Ocean View Suite",
              hotel: "Beachside Paradise Resort",
              price: 299,
              capacity: "2 Adults, 2 Children",
              amenities: ["Ocean View", "King Bed", "WiFi", "Breakfast"],
              image: "https://source.unsplash.com/random/300x200/?hotel,room,luxury"
          },
          {
              id: 102,
              name: "Executive Business Room",
              hotel: "Downtown Business Hotel",
              price: 189,
              capacity: "1 Adult",
              amenities: ["Work Desk", "Fast WiFi", "Coffee Maker"],
              image: "https://source.unsplash.com/random/300x200/?hotel,business,room"
          },
          {
              id: 103,
              name: "Family Suite",
              hotel: "Family Fun Resort",
              price: 259,
              capacity: "2 Adults, 3 Children",
              amenities: ["2 Bedrooms", "Game Console", "Mini Fridge"],
              image: "https://source.unsplash.com/random/300x200/?hotel,family,room"
          },
          {
              id: 104,
              name: "Mountain View Cabin",
              hotel: "Alpine Mountain Lodge",
              price: 229,
              capacity: "2 Adults",
              amenities: ["Fireplace", "Private Balcony", "Panoramic Views"],
              image: "https://source.unsplash.com/random/300x200/?mountain,cabin,room"
          }
      ];
      
      displayFeaturedRooms(rooms);
  }, 1500);
}

function displayFeaturedRooms(rooms) {
  const container = document.getElementById('featured-rooms-container');
  
  if (!rooms || rooms.length === 0) {
      container.innerHTML = '<p class="loading">No featured rooms found.</p>';
      return;
  }
  
  let html = '';
  rooms.forEach(room => {
      html += `
          <div class="card">
              <div class="card-image">
                  <img src="${room.image}" alt="${room.name}">
              </div>
              <div class="card-body">
                  <div class="badge">${room.capacity}</div>
                  <h3 class="card-title">${room.name}</h3>
                  <p class="card-text"><i class="fas fa-building"></i> ${room.hotel}</p>
                  <div class="amenities">
                      ${room.amenities.map(amenity => `<span><i class="fas fa-check"></i> ${amenity}</span>`).join(' ')}
                  </div>
                  <p class="card-price">$${room.price} <span>per night</span></p>
              </div>
              <div class="card-footer">
                  <button class="card-btn" onclick="viewRoom(${room.id})">
                      <i class="fas fa-info-circle"></i> View Details
                  </button>
              </div>
          </div>
      `;
  });
  
  container.innerHTML = html;
}

// Action functions
function viewHotelChain(chainId) {
  alert(`Viewing hotels for chain ID: ${chainId}`);
  // In a real application, you would redirect to the hotels page or load a modal
}

function viewRoom(roomId) {
  alert(`Viewing details for room ID: ${roomId}`);
  // In a real application, you would redirect to the room details page or load a modal
}