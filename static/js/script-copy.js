document.getElementById("btn-view-rooms").addEventListener("click", () => {
    // These values could be pulled from form inputs (not shown in your UI yet)
    const destination = "Ottawa";       // Replace with input if needed
    const capacity = 2;
    const checkIn = "2025-04-01";
    const checkOut = "2025-04-03";
  
    const url = `/rooms/available?destination=${encodeURIComponent(destination)}&capacity=${capacity}&check_in=${checkIn}&check_out=${checkOut}`;
  
    fetch(url)
      .then(res => res.json())
      .then(data => {
        const container = document.getElementById("available-rooms");
        container.innerHTML = "<h3>Available Rooms:</h3>";
  
        if (data.length === 0) {
          container.innerHTML += "<p>No rooms available for that search.</p>";
          return;
        }
  
        const list = document.createElement("ul");
        data.forEach(room => {
          const item = document.createElement("li");
          item.textContent = `Room ${room.room_number} (Capacity: ${room.capacity}) at Hotel ID ${room.hotel_id}`;
          list.appendChild(item);
        });
  
        container.appendChild(list);
      })
      .catch(err => {
        console.error("Failed to fetch rooms:", err);
        alert("Could not load available rooms.");
      });
  });
  