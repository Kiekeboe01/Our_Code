document.addEventListener("DOMContentLoaded", () => {
    const searchInputs = document.querySelectorAll(".search-input");

    // Create an object to keep track of the search queries for each column
    const searchQueries = {};
    // loops through every search input
    searchInputs.forEach((inputField) => {
        // Gets every table row in the body
        const tableRows = inputField.closest("table").querySelectorAll("tbody > tr");
        // Gets every header
        const otherHeaderCells = Array.from(inputField.closest("table").querySelectorAll("thead th"));
        // Gets the columnIndex
        const columnIndex = otherHeaderCells.indexOf(inputField.closest("th"));

        // Set the initial search query to an empty string
        searchQueries[columnIndex] = "";

        inputField.addEventListener("input", () => {
            // Update the search query for this column
            searchQueries[columnIndex] = inputField.value.toLowerCase();

            // Loop through all rows and check if they match the search queries for all columns
            for (const row of tableRows) {
                let rowMatchesSearch = true;
                for (const [index, query] of Object.entries(searchQueries)) {
                    const value = row.querySelectorAll("td")[index].textContent.toLowerCase().replace(",", "");
                    if (value.search(query) === -1) {
                        rowMatchesSearch = false;
                        break;
                    }
                }
                row.style.display = rowMatchesSearch ? "" : "none";
            }
        });
    });
});