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

    console.log("Difference in days:", diffDays);
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
