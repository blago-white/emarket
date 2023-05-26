function Filters() {
    if (document.getElementsByClassName("filters")[0].style.display == "none") {
        let header = document.getElementsByClassName("main-header")[0];
        let filters_window = document.getElementsByClassName("filters")[0];
        let others_pages_urls = document.getElementsByClassName("paginator");

        document.getElementById("change-order").href += "&filters";
        for (page_url in others_pages_urls) {
            if (typeof others_pages_urls[page_url].href === "string") {
                others_pages_urls[page_url].href += "&filters"
            }
        }

        header.animate([{height: "14vh"}], {duration: 200, easing: "ease"});
        setTimeout(e => {
            header.style.height = "14vh";
        }, 200);
        filters_window.style.display = "flex";
    } else {
        let header = document.getElementsByClassName("main-header")[0];
        let filters_window = document.getElementsByClassName("filters")[0];
        let others_pages_urls = document.getElementsByClassName("paginator");

        document.getElementById("change-order").href = document.getElementById("change-order").href.replace("&filters", "");
        for (page_url in others_pages_urls) {
            if (typeof others_pages_urls[page_url].href === "string") {
                others_pages_urls[page_url].href = others_pages_urls[page_url].href.replace("&filters", "");
            }
         }

        header.animate([{height: "7vh"}], {duration: 200, easing: "ease"});
        setTimeout(e => {
            header.style.height = "7vh";
            filters_window.style.display = "none"
        }, 200);
    }
}
