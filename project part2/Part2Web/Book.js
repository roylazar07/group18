class Workout {
    constructor(time,date,type){
        this.time = time
        this.date = date
        this.type = type
    }
    getTime() {
        return time
    }
    getDate() {
        return date
    }
    getType() {
        return type
    }

    getInfo(){
        return `<i class="fa-regular fa-calendar-days"></i> Date: ${this.date}, <i class="fa-solid fa-clock"></i> Time: ${this.time}, <i class="fa-solid fa-trophy"></i> Type: ${this.type}`
    }
}

const btn = document.querySelector("#Book");
const Workouts = [];
const Workouts_list = document.querySelector("#booked-workouts-list")

const datePicker = document.getElementById('training-date');
const today = new Date();
datePicker.setAttribute("max",'2030-12-31')
datePicker.setAttribute("min",`${today.getFullYear()}-${String(today.getMonth() + 1).padStart(2, '0')}-${String(today.getDate()).padStart(2, '0')}`)
console.log(`${today.getFullYear()}-${String(today.getMonth() + 1).padStart(2, '0')}-${String(today.getDate()).padStart(2, '0')}`)

///////////////////////////////////////////////////////////////////////////////////////////
// const today = new Date();
//
//
// const btn = document.querySelector("#Book");
// const Workouts = [];
// const Workouts_list = document.querySelector("#booked-workouts-list");
//
// const today = new Date();
// const yyyy = today.getFullYear();
// const mm = String(today.getMonth() + 1).padStart(2, '0');
// const dd = String(today.getDate()).padStart(2, '0');
//
// const futureDate = new Date();
// futureDate.setFullYear(yyyy + 5);
//
// const minDate = `${yyyy}-${mm}-${dd}`;
// const maxDate = `${futureDate.getFullYear()}-${String(futureDate.getMonth() + 1).padStart(2, '0')}-${String(futureDate.getDate()).padStart(2, '0')}`;
//
// const datePicker = document.getElementById('training-date');
// datePicker.setAttribute('min', minDate);
// datePicker.setAttribute('max', maxDate);
//
/////////////////////////////////////////////////////////////////////////////////////////////////////


btn.addEventListener("click", (e) => {
    e.preventDefault()
    const training_time = document.querySelector("#training-time").value
    const training_date = document.querySelector("#training-date").value
    const training_type = document.querySelector("#training-type").value

    if (training_date != ""){
        const title = document.querySelector("#ul-title")
        title.textContent = "Your upcoming workouts"
        Workouts_list.innerHTML = ""

        console.log(training_time)
        console.log(training_date)
        console.log(training_type)
        Workouts.push(new Workout(training_time,training_date,training_type))


        Workouts.forEach(function(Workout) {
            Workouts_list.innerHTML += "<li><h2>" + Workout.getInfo() + "</h2></li>"
        });
    } else {
        const date_select = document.querySelector("#training-date")
        date_select.style.border = " 2px solid red"
        window.alert("Please enter a date for your workout")
    }
});



btn.addEventListener("mouseover", (e) => {
    e.preventDefault()
    btn.style.backgroundColor = "blue"
    btn.innerText="מחכים לפגוש אותך!"
});

btn.addEventListener("mouseleave", (e) => {
    e.preventDefault()
    btn.style.backgroundColor = "black"
    btn.innerText="קבע את האימון"

});




