// end-date color change
document.addEventListener("DOMContentLoaded", function () {
  const endDateCells = document.querySelectorAll(".end-date");
  const today = new Date();
  today.setHours(0, 0, 0, 0);

  endDateCells.forEach((cell) => {
    const endDateString = cell.getAttribute("data-end-date");
    if (endDateString === "수시채용" || endDateString === "채용시") {
      return;
    }
    let endDate = new Date(endDateString);
    if (isNaN(endDate)) {
      return;
    }
    endDate.setHours(0, 0, 0, 0);
    const diffTime = endDate - today;
    const diffDays = diffTime / (1000 * 60 * 60 * 24);
    const span = cell.querySelector("span");
    if (diffDays === 0) {
      span.classList.add("red-background");
    } else if (diffDays > 0 && diffDays <= 10) {
      span.classList.add("orange-background");
    }
  });
});

// table filter
document.addEventListener("DOMContentLoaded", function () {
  const filterLinks = document.querySelectorAll(".filter-nav a");
  const rows = document.querySelectorAll(".recruit-row");

  filterLinks.forEach((link) => {
    link.addEventListener("click", function (event) {
      event.preventDefault();

      filterLinks.forEach((link) => link.classList.remove("active"));
      this.classList.add("active");

      const filterCategory = this.getAttribute("data-category");

      rows.forEach((row) => {
        const rowCategory = row.getAttribute("data-category");

        if (filterCategory === "ALL" || rowCategory === filterCategory) {
          row.style.display = "";
        } else {
          row.style.display = "none";
        }
      });
    });
  });
});

// bookmark
document.addEventListener("DOMContentLoaded", function () {
  const recruitTableBody = document.getElementById("recruitTableBody");
  let checkedRows = [];

  recruitTableBody.addEventListener("change", function (event) {
    if (event.target.matches('input[type="checkbox"]')) {
      const row = event.target.closest("tr");

      if (event.target.checked) {
        recruitTableBody.insertBefore(row, recruitTableBody.firstChild);
        checkedRows.push(row);
      } else {
        checkedRows = checkedRows.filter((checkedRow) => checkedRow !== row);

        if (checkedRows.length > 0) {
          const lastCheckedRow = checkedRows[checkedRows.length - 1];
          recruitTableBody.insertBefore(row, lastCheckedRow.nextElementSibling);
        } else {
          recruitTableBody.appendChild(row);
        }
      }
    }
  });
});

// this week filter button
// document.addEventListener("DOMContentLoaded", function () {
//   const rows = document.querySelectorAll("#result .recruit-row");

//   rows.forEach((row) => {
//     if (row.querySelector("td:nth-child(2)").textContent.includes("수시채용")) {
//       row.style.display = "none";
//     }
//   });

//   document.getElementById("filterThisWeek").addEventListener("click", function () {
//     const today = new Date();
//     const endOfWeek = new Date(today);
//     endOfWeek.setDate(today.getDate() + 7);

//     rows.forEach((row) => {
//       const endDate = new Date(row.querySelector(".end-date").dataset.endDate);
//       const isRecruitmentOpen = !row.querySelector("td:nth-child(2)").textContent.includes("수시채용");

//       if (endDate >= today && endDate <= endOfWeek && isRecruitmentOpen) {
//         row.style.display = "";
//       } else {
//         row.style.display = "none";
//       }
//     });
//   });
// });

// table sort
document.addEventListener("DOMContentLoaded", () => {
  const sortButton = document.querySelector(".sort button");
  console.log(sortButton);
  if (sortButton) {
    console.log("Sort button found");
    sortButton.addEventListener("click", () => {
      let ascending = true;
      const table = document.getElementById("detail-table");
      if (!table) {
        console.error("Table not found");
        return;
      }
      const rows = Array.from(table.tBodies[0].rows);
      if (!rows.length) {
        console.error("No rows found in the table body");
        return;
      }
      rows.sort((rowA, rowB) => {
        const cellA = rowA.cells[4];
        const cellB = rowB.cells[4];

        if (!cellA || !cellB) {
          console.error("Table cell not found");
          return 0;
        }

        const dateA = new Date(cellA.textContent);
        const dateB = new Date(cellB.textContent);

        const isDateAValid = !isNaN(dateA);
        const isDateBValid = !isNaN(dateB);

        if (!isDateAValid && !isDateBValid) {
          return 0;
        } else if (!isDateAValid) {
          return 1;
        } else if (!isDateBValid) {
          return -1;
        } else {
          return ascending ? dateA - dateB : dateB - dateA;
        }
      });

      ascending = !ascending;
      rows.forEach((row) => table.tBodies[0].appendChild(row)); // 정렬된 행을 다시 추가
    });
  } else {
    console.error("Sort button not found");
  }
});
