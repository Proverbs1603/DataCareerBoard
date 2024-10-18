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

// this week filter button
document.addEventListener("DOMContentLoaded", function () {
  const rows = document.querySelectorAll("#result .recruit-row");

  rows.forEach((row) => {
    if (row.querySelector("td:nth-child(2)").textContent.includes("수시채용")) {
      row.style.display = "none";
    }
  });

  document.getElementById("filterThisWeek").addEventListener("click", function () {
    const today = new Date();
    const endOfWeek = new Date(today);
    endOfWeek.setDate(today.getDate() + 7);

    rows.forEach((row) => {
      const endDate = new Date(row.querySelector(".end-date").dataset.endDate);
      const isRecruitmentOpen = !row.querySelector("td:nth-child(2)").textContent.includes("수시채용");

      if (endDate >= today && endDate <= endOfWeek && isRecruitmentOpen) {
        row.style.display = "";
      } else {
        row.style.display = "none";
      }
    });
  });
});

// table sort
function sortTable(columnIndex) {
  const table = document.getElementById("detail-table");
  const rows = Array.from(table.rows).slice(1);
  const isAsc = table.getAttribute("data-order") === "asc";

  // 기존의 아이콘과 스타일 초기화
  Array.from(table.rows[0].cells).forEach((cell) => {
    cell.classList.remove("sorted");
    cell.style.color = "";
  });

  table.rows[0].cells[columnIndex].classList.add("sorted");
  table.rows[0].cells[columnIndex].style.color = "#FF7F00";

  rows.sort((a, b) => {
    const dateA = new Date(a.cells[columnIndex].innerText);
    const dateB = new Date(b.cells[columnIndex].innerText);
    return isAsc ? dateA - dateB : dateB - dateA;
  });

  rows.forEach((row) => table.appendChild(row));
  table.setAttribute("data-order", isAsc ? "desc" : "asc");
}

// 워드클라우드
// 현재 표시 중인 워드클라우드의 인덱스를 추적
let currentWordCloudIndex = 0;

function showWordCloud(index) {
    const wordcloudItems = document.querySelectorAll('.wordcloud-item');
    if (index < 0) {
        index = wordcloudItems.length - 1; // 첫 번째에서 이전으로 가면 마지막으로 이동
    } else if (index >= wordcloudItems.length) {
        index = 0; // 마지막에서 다음으로 가면 첫 번째로 이동
    }

    // 모든 워드클라우드 숨기기
    wordcloudItems.forEach(item => item.style.display = 'none');

    // 선택된 워드클라우드만 표시
    wordcloudItems[index].style.display = 'block';
    currentWordCloudIndex = index;
}

// 화살표 버튼 클릭 이벤트에 showWordCloud 연결
document.querySelectorAll('.controls button').forEach((button, idx) => {
    button.addEventListener('click', () => {
        const direction = parseInt(button.getAttribute('onclick').match(/-?\d+/)[0]);
        showWordCloud(currentWordCloudIndex + direction);
    });
});

// 페이지 로드 시 첫 번째 워드클라우드 표시
document.addEventListener('DOMContentLoaded', () => {
    showWordCloud(0);
});
// 워드클라우드 종료