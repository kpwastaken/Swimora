console.log("Chart code started");
const ctx = document.getElementById("distanceChart");


if (ctx) {


    const gradient = ctx
        .getContext("2d")
        .createLinearGradient(0, 0, 0, 300);


    gradient.addColorStop(
        0,
        "rgba(0,122,255,0.45)"
    );


    gradient.addColorStop(
        1,
        "rgba(0,122,255,0.05)"
    );



    new Chart(ctx, {


        type: "line",



        data: {


            labels: workoutDates,



            datasets: [


                {

                    label: "Distance (meters)",


                    data: workoutDistances,


                    borderColor:
                    "#007aff",


                    backgroundColor:
                    gradient,


                    fill: true,


                    tension: 0.45,



                    pointRadius: 6,


                    pointHoverRadius: 9,


                    borderWidth: 4


                }


            ]

        },




        options: {


            responsive: true,



            animation: {


                duration: 1500


            },



            plugins: {


                legend: {


                    display: false


                }



            },



            scales: {


                y: {


                    beginAtZero: true,


                    grid: {


                        display: false


                    }


                },



                x: {


                    grid: {


                        display: false


                    }


                }


            }



        }



    });


}