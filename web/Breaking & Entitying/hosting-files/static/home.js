function showPopup(message) {
  const popup = document.getElementById("popup");
  const content = document.getElementById("popup-content");

  content.textContent = message;
  popup.style.display = "block";
}

function hidePopup() {
  document.getElementById("popup").style.display = "none";
}

document.getElementById("popup-close").addEventListener("click", hidePopup);

function getJwtPayload() {
  const token = document.cookie
    .split("; ")
    .find(row => row.startsWith("token="))
    ?.split("=")[1];

  if (!token) return null;

  const payload = token.split(".")[1];
  return JSON.parse(atob(payload));
}

document.getElementById("accountForm").addEventListener("submit", function (e) {
  e.preventDefault();

  const jwt = getJwtPayload();
  if (!jwt) {
    showPopup("Not logged in");
    return;
  }

  const xml = `<?xml version="1.0"?>
<data>
  <username>${jwt.username}</username>
  <name>${jwt.name}</name>
</data>`;

  fetch("/account", {
    method: "POST",
    headers: {
      "Content-Type": "application/xml"
    },
    body: xml
  })
    .then(resp => {
      if (resp.ok) {
        return resp.blob();
      }
      return resp.text().then(t => { throw t; });
    })
    .then(blob => {
      const url = window.URL.createObjectURL(blob);
      window.open(url);
    })
    .catch(err => {
      showPopup(typeof err === "string" ? err : "Something went wrong");
    });
});
