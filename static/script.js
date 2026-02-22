// ================= GLOBAL CHART INSTANCES =================
let trendChartInstance = null;
let importanceChartInstance = null;


// ================= LOAD COURSES =================
fetch("/courses")
.then(res => res.json())
.then(data => {

    let table = document.getElementById("courseTable");

    // Clear before adding (important)
    table.innerHTML = "";
    document.getElementById("topHigh").innerHTML = "";
    document.getElementById("topLow").innerHTML = "";
    document.getElementById("topJobs").innerHTML = "";

    // -------- TOP HIGH --------
    let high = data.filter(d => d.demand === "High")
                   .sort((a,b) => b.growth - a.growth)
                   .slice(0,3);

    high.forEach(c => {
        document.getElementById("topHigh").innerHTML +=
        `<li>${c.course}</li>`;
    });

    // -------- TOP LOW --------
    let low = data.filter(d => d.demand === "Low")
                  .sort((a,b) => a.growth - b.growth)
                  .slice(0,3);

    low.forEach(c => {
        document.getElementById("topLow").innerHTML +=
        `<li>${c.course}</li>`;
    });

    // -------- TOP JOB ORIENTED (Salary + Demand Score) --------
    let jobTop = [...data]
        .sort((a,b) => b.job_score - a.job_score)
        .slice(0,3);

    jobTop.forEach(c => {
        document.getElementById("topJobs").innerHTML +=
        `<li>${c.course} (₹ ${Math.round(c.salary)})</li>`;
    });

    // -------- ALL COURSES TABLE --------
    data.forEach(course => {

        table.innerHTML += `
        <tr onclick="showTrend('${course.course}')">
            <td>${course.course}</td>
            <td>${course.growth.toFixed(4)}</td>
            <td class="${course.demand=='High'?'text-success':'text-danger'}">
                ${course.demand}
            </td>
            <td>₹ ${Math.round(course.salary)}</td>
        </tr>`;
    });

});


// ================= TREND MODAL =================
// function showTrend(course){

//     fetch("/trend/" + course)
//     .then(res => res.json())
//     .then(data => {

//         document.getElementById("modalTitle").innerText =
//             course + " - Growth Trend";

//         const modal = new bootstrap.Modal(
//             document.getElementById("trendModal")
//         );

//         modal.show();

//         const ctx = document.getElementById("trendChart");

//         if (trendChartInstance) {
//             trendChartInstance.destroy();
//         }

//         trendChartInstance = new Chart(ctx, {
//             type: "line",
//             data: {
//                 labels: data.months,
//                 datasets: [
// {
//     label: "Monthly Hours",
//     data: data.hours,
//     borderColor: "#00ffff",
//     backgroundColor: "rgba(0,255,255,0.2)",
//     tension: 0.4,
//     fill: true
// },
// {
//     label: "Trend Line (Linear Regression)",
//     data: data.trend,
//     borderColor: "#ff4c4c",
//     borderDash: [5,5],
//     tension: 0,
//     fill: false
// }
// ]
//             },
//             options: {
//                 responsive: true,
//                 animation: { duration: 1200 },
//                 plugins: {
//                     legend: {
//                         labels: { color: "white" }
//                     }
//                 },
//                 scales: {
//                     x: { ticks: { color: "white" } },
//                     y: { ticks: { color: "white" } }
//                 }
//             }
//         });
//     });
// }


// if (data.slope > 0) {
//     document.getElementById("trendText").innerText =
//         "Course is Growing 📈 (Slope: " + data.slope.toFixed(2) + ")";
// }
// else if (data.slope < 0) {
//     document.getElementById("trendText").innerText =
//         "Course is Declining 📉 (Slope: " + data.slope.toFixed(2) + ")";
// }
// else {
//     document.getElementById("trendText").innerText =
//         "Course is Stable";
// }

function showTrend(course){

    fetch("/trend/" + course)
    .then(res => res.json())
    .then(data => {

        document.getElementById("modalTitle").innerText =
            course + " - Growth Trend";

        const modal = new bootstrap.Modal(
            document.getElementById("trendModal")
        );

        modal.show();

        const ctx = document.getElementById("trendChart");

        if (trendChartInstance) {
            trendChartInstance.destroy();
        }

        trendChartInstance = new Chart(ctx, {
            type: "line",
            data: {
                labels: data.months,
                datasets: [
                    {
                        label: "Monthly Hours",
                        data: data.hours,
                        borderColor: "#00ffff",
                        backgroundColor: "rgba(0,255,255,0.2)",
                        tension: 0.4,
                        fill: true
                    },
                    {
                        label: "Trend Line (Linear Regression)",
                        data: data.trend,
                        borderColor: "#ff4c4c",
                        borderDash: [5,5],
                        tension: 0,
                        fill: false
                    }
                ]
            },
            options: {
                responsive: true
            }
        });
        let avg = data.hours.reduce((a,b)=>a+b,0)/data.hours.length;
let growthRate = data.slope / avg;

let trendText = "";

if (growthRate > 0.05) {
    trendText = "Strong Growth 📈";
}
else if (growthRate > 0.01) {
    trendText = "Moderate Growth ↗";
}
else if (growthRate > -0.01) {
    trendText = "Stable ➖";
}
else {
    trendText = "Declining 📉";
}

document.getElementById("trendText").innerText =
    trendText + " (Normalized Growth: " + growthRate.toFixed(3) + ")";

    });
}
function showClusters(){

    fetch("/cluster")
    .then(res => res.json())
    .then(data => {

        console.log("Cluster Data:", data);  // 👈 Add this

        if(data.length === 0){
            alert("No cluster data received");
            return;
        }

        let trace = {
            x: data.map(d => d.Skill_Level),
            y: data.map(d => d.Hours_Watched),
        z: data.map(d => d.Salary_Expectation),
            mode: 'markers',
            marker: {
                size: 6,
                color: data.map(d => d.Cluster),
                colorscale: 'Viridis'
            },
            type: 'scatter3d',
            text: data.map(d => d.Course_Name)
        };

        let layout = {
            title: "3D Clustering (Skill vs Hours vs Salary)",
            paper_bgcolor: "#111",
            font: { color: "white" },
            height: 500
        };

        Plotly.newPlot("clusterPlot", [trace], layout);
    });
}
Plotly.purge("clusterPlot");
Plotly.newPlot("clusterPlot", [trace], layout);
// ================= FEATURE IMPORTANCE =================
function showImportance(){

    fetch("/feature_importance")
    .then(res => res.json())
    .then(data => {

        const ctx = document.getElementById("importanceChart");

        if (importanceChartInstance) {
            importanceChartInstance.destroy();
        }

        importanceChartInstance = new Chart(ctx, {
            type: "bar",
            data: {
                labels: data.features,
                datasets: [{
                    label: "Feature Importance",
                    data: data.importance,
                    backgroundColor: "orange"
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        labels: { color: "white" }
                    }
                },
                scales: {
                    x: { ticks: { color: "white" } },
                    y: { ticks: { color: "white" } }
                }
            }
        });
    });
}