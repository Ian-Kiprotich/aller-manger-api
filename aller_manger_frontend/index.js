//get data from the login form and store token
//login form
const loginForm = document.getElementById('login-form')
const signupForm = document.getElementById('signup-form')
const deleteForm = document.getElementById('delete-trash-form')
const reservationForm = document.getElementById('make-reservation-form')
const cancellationForm = document.getElementById('cancel-form')
const reservationFormContainer = document.getElementById('reservations-table')
const loginIconListItem = document.getElementById('login-button')
const signUpBtn_Show = document.getElementById('sign-up-btn')
const loginUpBtn_Show = document.getElementById('login-back-btn')
const reservationBtn = document.getElementById('reservationNavBtn')
const getReservationNavBtn = document.getElementById('getReservationNavBtn')
const cancelReservationBtn = document.getElementById('cancelReservationBtn')
const correctMsg = document.getElementById('message-correct')
const wrongMsg = document.getElementById('message-wrong')
const logoutBtn = document.getElementById('logout-button')
let tableDataBody = document.getElementById('tbody-list')
//check for stored users tokens
const token = sessionStorage.getItem('token')


//add functionalities
signUpBtn_Show.addEventListener('click', showRegistration)
loginUpBtn_Show.addEventListener('click', showLogin)
loginIconListItem.addEventListener('click', showLogin)

logoutBtn.addEventListener('click', ()=>{
    correctMsg.style.display = "block"
    sessionStorage.removeItem('token')
    correctMsg.innerHTML = `<p>You have been logged out successfully.</p>`
    setTimeout(()=>{
        location.reload()
    },2000)
})

//check for the availability of a token
setInterval(()=>{
    if(token){
        loginIconListItem.style.backgroundColor = "#ddffed";
        loginIconListItem.innerHTML = `<i class="fa fa-lock"></i> `;
    }else{
        loginIconListItem.style.backgroundColor = "#ffe1e1";
        loginIconListItem.innerHTML = `<i class="fa fa-lock-open"></i> `;
    }
}, 1000)

//login user
loginForm.addEventListener('submit', async (e) =>{
    e.preventDefault();
    const username  = document.getElementById('username').value
    const password = document.getElementById('password').value
    
    const login_icon_btn_nav = document.getElementById('login-button')
    // login POST endpoint
    let loginEndpoint  = "http://127.0.0.1:8000/api/aller-manger/v1.0/users/login";
    //do some error handling
    try {
        const response = await fetch(
            loginEndpoint,
            {
                method:'POST',
                headers: {
                    'accept': 'application/json',
                    'Content-Type':'application/x-www-form-urlencoded'
                },
                body: `grant_type=password&username=${username}&password=${password}&scope=&client_id=string&client_secret=string`
            }
        )

        //get token from the response body
        const data = await response.json()
        console.log(data)
        if(data.access_token){
            sessionStorage.setItem('token',data.access_token);
            
            setTimeout(()=>{
                location.reload()
            },2000)

            loginIconListItem.style.backgroundColor = "#ddffed";
            login_icon_btn_nav.innerHTML = `<i class="fa fa-lock"></i> `;
            loginForm.style.display = "none";
            cancellationForm.style.display = "none";
            reservationFormContainer.style.display = "none";
            reservationForm.style.display = "block";
            correctMsg.style.display = "none";
            wrongMsg.style.display = "none"
                
        }else{
            wrongMsg.style.display = "block"
            wrongMsg.innerHTML = `<p>${data.detail}</p>`
        }

    } catch (error) {
        wrongMsg.style.display = "block"
        wrongMsg.innerHTML = `<p>${error}</p>`
    }
})

//register user
signupForm.addEventListener('submit', async (e) =>{
    e.preventDefault();
    const username  = document.getElementById('user_name').value
    const fname = document.getElementById('first_name').value
    const lname = document.getElementById('last_name').value
    const email = document.getElementById('email').value
    const phone  = document.getElementById('phone').value
    const password_signup = document.getElementById('password-signup').value
    console.log(`Password: ${password_signup}`)
    //format phone number
    let phone_number_index = phone.substr(0,1)
    let phone_number = ""
    if( phone_number_index == "0"){
        phone_number = `254${phone.substr(1)}`
    }else{
        phone_number = phone.substr(1)
    }
    
    // login POST endpoint
    let signupEndpoint  = "http://127.0.0.1:8000/api/aller-manger/v1.0/users/create/account";
    //do some error handling
    try {
        const response = await fetch(
            signupEndpoint,
            {
                method:'POST',
                headers: {
                    'accept': 'application/json',
                    'Content-Type':'application/x-www-form-urlencoded'
                },
                body: `user_name=${username}&first_name=${fname}&last_name=${lname}&email=${email}&phone=${phone_number}&password=${password_signup}`
            }
        )

        //get token from the response body
        const data = await response.json()
        
        if(response.status == 201){
            signupForm.style.display = "none"
            cancellationForm.style.display = "none";
            reservationForm.style.display = "none"
            loginForm.style.display = "block";
        }else{
            console.log(data)
        }

    } catch (error) {
        alert(`Error: ${error}`)
    }
})

//register user
reservationForm.addEventListener('submit', async (e) =>{
    e.preventDefault();
    let guestList = []
    let idsList = []
    const gnames  = document.getElementById('guest_names').value
    const gids = document.getElementById('guest_ids').value
    const address = document.getElementById('address').value
    const tableNumber = document.getElementById('tableNumber').value
    const phone  = document.getElementById('phone-reservations').value
    console.log(phone)
    const time = document.getElementById('time').value
    //create name list
    let inputGNames = gnames.split(',')
    for(let i=0; i<inputGNames.length-1; i++){
        guestList.push(inputGNames[i])
    }
    //create IDs list
    let inputIds = gids.split(',')
    for(let i=0; i<inputIds.length-1; i++){
        idsList.push(inputIds[i])
    }
   // Format phone number
   let phone_number = "";
   if (phone && phone.startsWith("0")) {
       phone_number = `254${phone.substr(1)}`;  // Replace starting '0' with '254'
   } else {
       phone_number = phone.trim();  // Use original phone number if it doesn't start with '0'
   }
   console.log("Formatted phone number:", phone_number);
    // reservation POST endpoint
    let reserveEndpoint  = "http://127.0.0.1:8000/api/aller-manger/v1.0/add/reservation";
    //do some error handling
    try {
        const response = await fetch(
            reserveEndpoint,
            {
                method:'POST',
                headers: {
                    'accept': 'application/json',
                    'Authorization': `Bearer ${token}`,
                    'Content-Type':'application/x-www-form-urlencoded'
                },
                body: `guest_names=${gnames}&guest_ids=${gids}&address=${address}&phone=${phone_number}&table_no=${tableNumber}&time=${time}`
            }
        )

        //get token from the response body
        const data = await response.json()
        
        if(response.status == 201){
            
            signupForm.style.display = "none"
            reservationForm.style.display = "block"
            cancellationForm.style.display = "none";
            reservationFormContainer.style.display = "none";
            loginForm.style.display = "none"
            correctMsg.style.display = "block"
            correctMsg.innerHTML = `<p>${data.detail}</p>`
            wrongMsg.style.display = "none"
        }else{
            correctMsg.style.display = "none"
            wrongMsg.style.display = "block"
            wrongMsg.innerHTML = `<p>${data.detail}</p>`
        }

    } catch (error) {
        correctMsg.style.display = "none"
        wrongMsg.style.display = "block"
        wrongMsg.innerHTML = `<p>${error}</p>`
    }
})

//cancellation user
cancellationForm.addEventListener('submit', async (e) =>{
    e.preventDefault();
    const table_no  = document.getElementById('table_no').value
    
    // reservation POST endpoint
    let cancelEndpoint  = "http://127.0.0.1:8000/api/aller-manger/v1.0/user/reservations/cancel";
    //do some error handling
    try {
        const response = await fetch(
            cancelEndpoint,
            {
                method:'PUT',
                headers: {
                    'accept': 'application/json',
                    'Authorization': `Bearer ${token}`,
                    'Content-Type':'application/x-www-form-urlencoded'
                },
                body: `table_no=${table_no}`
            }
        )

        //get token from the response body
        const data = await response.json()
        
        if(response.status == 201){
            
            signupForm.style.display = "none"
            reservationForm.style.display = "none"
            cancellationForm.style.display = "block";
            reservationFormContainer.style.display = "none";
            loginForm.style.display = "none"
            correctMsg.style.display = "block"
            correctMsg.innerHTML = `<p>${data.detail}</p>`
            wrongMsg.style.display = "none"
        }else{
            correctMsg.style.display = "none"
            wrongMsg.style.display = "block"
            wrongMsg.innerHTML = `<p>${data.detail}</p>`
        }

    } catch (error) {
        correctMsg.style.display = "none"
        wrongMsg.style.display = "block"
        wrongMsg.innerHTML = `<p>${error}</p>`
    }
})

//delete reservation
async function deleteReservation(rsvdId){
    
    // reservation POST endpoint
    let deleteReservationEndpoint  = `http://127.0.0.1:8000/api/aller-manger/v1.0/user/reservations/delete/${rsvdId}`;
    //do some error handling
    try {
        const response = await fetch(
            deleteReservationEndpoint,
            {
                method:'DELETE',
                headers: {
                    'accept': 'application/json',
                    'Authorization': `Bearer ${token}`
                }
            }
        )

        //get token from the response body
        const data = await response.json()
        
        if(response.status == 201){
            
            signupForm.style.display = "none"
            reservationForm.style.display = "none"
            cancellationForm.style.display = "none";
            reservationFormContainer.style.display = "none";
            loginForm.style.display = "none"
            correctMsg.style.display = "block"
            correctMsg.innerHTML = `<p>${data.detail}</p>`
            wrongMsg.style.display = "none"
            setTimeout(()=>{
                location.reload()
            },2000)
        }else{
            correctMsg.style.display = "none"
            wrongMsg.style.display = "block"
            wrongMsg.innerHTML = `<p>${data.detail}</p>`
        }

    } catch (error) {
        correctMsg.style.display = "none"
        wrongMsg.style.display = "block"
        wrongMsg.innerHTML = `<p>${error}</p>`
    }
}



function showRegistration(){
    loginForm.style.display = "none"
    reservationForm.style.display = "none"
    signupForm.style.display = "block"
    reservationFormContainer.style.display = "none";
}

function showLogin(){
    loginForm.style.display = "block"
    reservationForm.style.display = "none"
    signupForm.style.display = "none"
    reservationFormContainer.style.display = "none";
}

//add functionality to nav buttons

reservationBtn.addEventListener('click',()=>{
    loginForm.style.display = "none"
    reservationForm.style.display = "block"
    signupForm.style.display = "none"
    cancellationForm.style.display = "none";
    reservationFormContainer.style.display = "none";
})

cancelReservationBtn.addEventListener('click',()=>{
    loginForm.style.display = "none"
    reservationForm.style.display = "none"
    signupForm.style.display = "none"
    cancellationForm.style.display = "block";
    reservationFormContainer.style.display = "none";
})

getReservationNavBtn.addEventListener('click', async () => {
    loginForm.style.display = "none";
    reservationForm.style.display = "none";
    signupForm.style.display = "none";
    cancellationForm.style.display = "none";
    reservationFormContainer.style.display = "block";

    // Reservation GET endpoint
    let getReservationsEndpoint = `http://127.0.0.1:8000/api/aller-manger/v1.0/user/reservations`;

    try {
        const response = await fetch(getReservationsEndpoint, {
            method: 'GET',
            headers: {
                'accept': 'application/json',
                'Authorization': `Bearer ${token}`
            }
        });

        const data = await response.json();

        if (response.status === 200) {
            // Clear previous table data
            tableDataBody.innerHTML = "";

            data.forEach(reservation => {
                // Convert guest names and IDs arrays to comma-separated strings
                let guestNames = reservation.guest_names.join(", ");
                let guestIds = reservation.guest_ids.join(", ");

                tableDataBody.innerHTML += `
                    <tr>
                        <td>${reservation.reservation_id}</td>
                        <td>${guestNames}</td>
                        <td>${guestIds}</td>
                        <td>${reservation.time}</td>
                        <td>${reservation.table_no}</td>
                        <td>
                            <form id="delete-trash-form">
                                <input type="hidden" name="rsvdId" id="rsvdId" value="${reservation.reservation_id}" readonly>
                                <button type="button" onclick="deleteReservation('${reservation.reservation_id}')">
                                    <i class="fa fa-trash"></i>
                                </button>
                            </form>
                        </td>
                    </tr>
                `;
            });

            correctMsg.style.display = "block";
            correctMsg.innerHTML = `<p>Reservations loaded successfully</p>`;
            wrongMsg.style.display = "none";
        } else {
            correctMsg.style.display = "none";
            wrongMsg.style.display = "block";
            wrongMsg.innerHTML = `<p>Error: ${data.detail || "Unable to fetch reservations"}</p>`;
        }

    } catch (error) {
        correctMsg.style.display = "none";
        wrongMsg.style.display = "block";
        wrongMsg.innerHTML = `<p>${error.message}</p>`;
    }
});


