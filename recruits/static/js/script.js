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


// table category filter
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

// sort the table by "마감일" column
document.addEventListener("DOMContentLoaded", () => {
  const sortButton = document.querySelector(".sort button");
  let ascending = true;

  sortButton.addEventListener("click", () => {
    const rows = Array.from(document.querySelectorAll("#detail-table tbody tr"));
    rows.sort((a, b) => {
      const dateA = a.querySelector(".end-date").dataset.endDate;
      const dateB = b.querySelector(".end-date").dataset.endDate;

      // "None"과 "상시채용" 값들을 처리
      if (dateA === "None" && dateB === "None") return 0;
      if (dateA === "상시채용" && dateB === "상시채용") return 0;
      if (dateA === "None") return ascending ? 1 : -1;
      if (dateB === "None") return ascending ? -1 : 1;
      if (dateA === "상시채용") return ascending ? 1 : -1;
      if (dateB === "상시채용") return ascending ? -1 : 1;

      const dateObjA = new Date(dateA);
      const dateObjB = new Date(dateB);
      return ascending ? dateObjA - dateObjB : dateObjB - dateObjA;
    });

    const tbody = document.querySelector("#detail-table tbody");
    tbody.innerHTML = "";
    rows.forEach((row) => tbody.appendChild(row));
    ascending = !ascending;
    sortButton.classList.toggle("sorted", ascending);
  });
});

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

// 화살표 버튼 클릭 이벤트에 WordCloud 연결
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