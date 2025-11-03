const fileInput = document.getElementById("fileInput");
const fileName = document.getElementById("fileName");
const uploadBtn = document.getElementById("uploadBtnId");
const sts = document.getElementById("status");

fileInput.addEventListener("change", () => {
  if (fileInput.files.length > 0) {
    fileName.textContent = fileInput.files[0].name;
    uploadBtn.disable = false;
    sts.textContent = "";
  } else {
    fileName.textContent = "";
    uploadBtn.disable = true;
    sts.textContent = "";
  }
});

uploadBtn.addEventListener("click", () => {
    sts.className = "status"
  if (fileInput.files.length === 0) return;
  const formdata = new FormData();
  formdata.append("file", fileInput.files[0]);
  const apiurl = "http://160.12.158.20:5051/globals/import";
  sts.textContent = "Uploading...";
  fetch(apiurl, {
    method: "POST",
    body: formdata,
  })
    .then((res) => {
      if (!res.ok) {
        throw new Error("Server Error status: " + res.status);
      }
      return res.json();
    })
    .then((data) => {
      sts.textContent = "Uploaded Successfully!";
      console.log("Success \n",data);
      sts.className = "status success"
    })
    .catch((err) => {
      sts.textContent = "Upload Failed!! " + err?.message;
      sts.className = "status error"
      console.error(err);
    });
});
