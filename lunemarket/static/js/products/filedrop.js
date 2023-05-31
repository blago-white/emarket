document.getElementById('upload-photo').addEventListener('change', function(e) {
  if (e.target.files[0]) {
    console.log(document.getElementsByClassName("drop")[0].textContent);
    document.getElementsByClassName("drop")[0].textContent = " " + e.target.files[0].name.slice(0, 20) + (
        e.target.files[0].name.length > 20 ? "..." : ""
    );
    document.getElementsByClassName("drop")[0].title = e.target.files[0].name;
  }
});