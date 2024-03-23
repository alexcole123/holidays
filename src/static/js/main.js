function confirmDelete() {
    const ok = confirm("Are you Sure?");
    if (!ok) event.preventDefault();
}

// Finds element by css:
const errorSpan = document.querySelector(".error");
if (errorSpan) {
    setTimeout(() => {
        errorSpan.parentNode.removeChild(errorSpan);
    }, 4000);
}

let sessionData;

if (window.location.pathname.includes("/holidays")) {
    document.addEventListener("DOMContentLoaded", () => {
        fetchSessionData()
            .then(() => {
                if (sessionData.current_user.role_id === 2) likeUsersLikedHolidays();
            })
            .catch(error => {
                console.error("Error loading session data:", error);
            });
    });
}

async function fetchSessionData() {
    try {
        const response = await fetch("/get-session-data");
        if (!response.ok) {
            throw new Error("Network response error");
        }
        sessionData = await response.json();
    } catch (error) {
        console.error("Error fetching session data", error);
    }
}

function likeUsersLikedHolidays() {
    document.querySelectorAll(".likes").forEach(likeElement => {
        const holidayId = parseInt(likeElement.dataset.id); // Update to access data-id attribute
        if (sessionData.current_user.liked_holidays.includes(holidayId)) {
            likeElement.classList.add("liked")
            likeElement.style.opacity = 1;
        }
    });
}

function changeLikeStatus(likes) {
    const likesSpan = likes.querySelector("span"); // Get the container of the like button
    const currentLikes = parseInt(likesSpan.textContent)

    console.log("Current likes before update:", currentLikes);

    let dataToSend = {
        "holiday_id": parseInt(likes.dataset.id), // Update to access data-id attribute
        "user_id": sessionData.current_user.id
    };

    console.log("Data to send:", dataToSend); // Log the data being sent

    if (!likes.classList.contains("liked")) {
        likes.classList.add("liked");
        likes.style.opacity = 1;
        likesSpan.textContent = currentLikes + 1;
        dataToSend.liked = true;
    } else {
        likes.classList.remove("liked");
        likesSpan.textContent = currentLikes - 1;
        likes.style.opacity = 0.7;
        dataToSend.liked = false;
    }

    console.log("Updated likes:", likesSpan.textContent); // Log the updated likes count

    sendLikedData(dataToSend);
}


async function sendLikedData(data) {
    try {
        const response = await fetch("/holidays/update-likes", {
            method: "POST",
            headers: {
                "Content-Type": "application/json" // Set Content-Type header
            },
            body: JSON.stringify(data) // Convert data to JSON string
        });
        if (!response.ok) {
            throw new Error("Network response error.");
        }
        return await response.json();
    } catch (error) {
        console.error("Error passing data:", error);
        throw error;
    }
}





// Function to handle file input change event
function handleFileInputChange(event) {
    const fileInput = event.target; // Get the file input element
    const file = fileInput.files[0]; // Get the selected file
    const previewImage = document.getElementById('previewImage'); // Get the preview image element

    // Check if a file is selected
    if (file) {
        // Create a file reader object
        const reader = new FileReader();

        // Define the onload event handler for the file reader
        reader.onload = function(e) {
            // Set the src attribute of the preview image to the data URL of the selected file
            previewImage.src = e.target.result;
            previewImage.style.display = 'block'; // Show the preview image
        };

        // Read the selected file as a data URL
        reader.readAsDataURL(file);
    }
}

// Add event listener to the file input element
const fileInput = document.getElementById('imageInput');
fileInput.addEventListener('change', handleFileInputChange);
