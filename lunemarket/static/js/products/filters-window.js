function Filters() {
    if (document.getElementsByClassName("filters")[0].style.display == "none") {
        let header = document.getElementsByClassName("main-header")[0];
        let filters_window = document.getElementsByClassName("filters")[0];
        let others_pages_urls = document.getElementsByClassName("paginator");

        let url;
        for (page_url in others_pages_urls) {
            if (typeof others_pages_urls[page_url].href === "string") {
                url = new URL(others_pages_urls[page_url]);
                url.searchParams.set("filters", 1);
                others_pages_urls[page_url].href = url.href;
            }
        }

        header.animate([{height: "16.9vh"}], {duration: 200, easing: "ease"});
        setTimeout(e => {
            header.style.height = "16.9vh";
        }, 200);
        filters_window.style.display = "flex";
    } else {
        let header = document.getElementsByClassName("main-header")[0];
        let filters_window = document.getElementsByClassName("filters")[0];
        let others_pages_urls = document.getElementsByClassName("paginator");

        document.getElementById("change-order").href = document.getElementById("change-order").href.replace("&filters", "");
        let url;
        for (page_url in others_pages_urls) {
            if (typeof others_pages_urls[page_url].href === "string") {
                url = new URL(others_pages_urls[page_url]);
                url.searchParams.set("filters", 0);
                others_pages_urls[page_url].href = url.href;
            }
        }

        header.animate([{height: "6vh"}], {duration: 200, easing: "ease"});
        setTimeout(e => {
            header.style.height = "6vh";
            filters_window.style.display = "none"
        }, 200);
    }
}