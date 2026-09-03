// document.addEventListener("DOMContentLoaded", () => {

//     // Lucide Icons Render
//     if (typeof lucide !== "undefined") {
//         lucide.createIcons();
//     }

//     // =========================
//     // DOM ELEMENTS
//     // =========================
//     const fileInput = document.getElementById("fileInput");
//     const chooseFileBtn = document.getElementById("chooseFileBtn");
//     const dropZone = document.getElementById("dropZone") || document.querySelector(".drop-zone");

//     const uploadTitle = document.getElementById("uploadTitle");
//     const dragText = document.getElementById("dragText");
//     const selectedFile = document.getElementById("selectedFile");

//     const MAX_FILE_SIZE = 20 * 1024 * 1024; // 20MB


//     // =========================
//     // FILE VALIDATION
//     // =========================
//     function validateEmailFile(file) {
//         if (!file) return false;

//         if (!file.name.toLowerCase().endsWith(".eml")) {
//             alert("Please select a valid .eml file.");
//             return false;
//         }

//         if (file.size > MAX_FILE_SIZE) {
//             alert("Maximum file size limit is 20 MB.");
//             return false;
//         }

//         return true;
//     }


//     // =========================
//     // DISPLAY FILE NAME IN UI
//     // =========================
//     function showSelectedFile(file) {
//         if (!file) return;

//         if (uploadTitle) uploadTitle.textContent = "Email selected";
//         if (dragText) dragText.textContent = "Ready to analyze";

//         if (selectedFile) {
//             selectedFile.textContent = "📄 " + file.name;
//             selectedFile.style.display = "block";
//         }

//         console.log("✅ File Selected Successfully:", file.name);
//     }


//     // =========================
//     // BUTTON CLICK HANDLER
//     // =========================
//     if (chooseFileBtn && fileInput) {
//         chooseFileBtn.addEventListener("click", (e) => {
//             e.preventDefault();
//             e.stopPropagation();
//             fileInput.click();
//         });
//     }


//     // =========================
//     // FILE INPUT CHANGE HANDLER
//     // =========================
//     if (fileInput) {
//         fileInput.addEventListener("change", (e) => {
//             e.stopPropagation();

//             const file = e.target.files[0];
//             if (!file) return;

//             if (!validateEmailFile(file)) {
//                 fileInput.value = ""; // Reset invalid file
//                 return;
//             }

//             // Show selected file immediately in UI
//             showSelectedFile(file);

//             // Upload to API
//             uploadEmail(file);
//         });
//     }


//     // =========================
//     // DRAG & DROP HANDLERS
//     // =========================
//     if (dropZone) {
//         ["dragenter", "dragover", "dragleave", "drop"].forEach(eventName => {
//             dropZone.addEventListener(eventName, (e) => {
//                 e.preventDefault();
//                 e.stopPropagation();
//             }, false);
//         });

//         dropZone.addEventListener("dragover", () => {
//             dropZone.classList.add("drag-over");
//         });

//         dropZone.addEventListener("dragleave", () => {
//             dropZone.classList.remove("drag-over");
//         });

//         dropZone.addEventListener("drop", (e) => {
//             dropZone.classList.remove("drag-over");

//             const files = e.dataTransfer.files;
//             if (!files || files.length === 0) return;

//             const file = files[0];
//             if (!validateEmailFile(file)) return;

//             // Assign file to input element safely using DataTransfer
//             const dataTransfer = new DataTransfer();
//             dataTransfer.items.add(file);
//             fileInput.files = dataTransfer.files;

//             showSelectedFile(file);
//             uploadEmail(file);
//         });
//     }


//     // =========================
//     // UPLOAD TO BACKEND SERVER
//     // =========================
//     async function uploadEmail(file) {
//         const formData = new FormData();
//         formData.append("email", file);

//         console.log("📤 Sending EML file to server:", file.name);

//         try {
//             const response = await fetch("http://localhost:5000/api/emails/analyze", {
//                 method: "POST",
//                 body: formData
//             });

//             const result = await response.json();

//             if (!response.ok) {
//                 throw new Error(result.message || "File analysis failed");
//             }

//             console.log("📥 Backend Analysis Result:", result);

//             // Maintain file selection UI state
//             showSelectedFile(file);

//         } catch (error) {
//             console.error("❌ Upload error:", error);
//             // File interface screen par retained rahegi
//             showSelectedFile(file);
//         }
//     }


//     // =========================
//     // HELP MODAL HANDLERS
//     // =========================
//     const helpBtn = document.getElementById("helpBtn");
//     const helpModal = document.getElementById("helpModal");
//     const closeModal = document.getElementById("closeModal");
//     const gotIt = document.getElementById("gotIt");

//     if (helpBtn && helpModal) {
//         helpBtn.addEventListener("click", () => helpModal.classList.add("active"));
//     }
//     if (closeModal && helpModal) {
//         closeModal.addEventListener("click", () => helpModal.classList.remove("active"));
//     }
//     if (gotIt && helpModal) {
//         gotIt.addEventListener("click", () => helpModal.classList.remove("active"));
//     }
//     if (helpModal) {
//         helpModal.addEventListener("click", (e) => {
//             if (e.target === helpModal) helpModal.classList.remove("active");
//         });
//     }

// });


document.addEventListener("DOMContentLoaded", () => {

    // =========================
    // LUCIDE ICONS
    // =========================
    if (typeof lucide !== "undefined") {
        lucide.createIcons();
    }


    // =========================
    // DOM ELEMENTS
    // =========================
    const fileInput = document.getElementById("fileInput");
    const chooseFileBtn = document.getElementById("chooseFileBtn");
    const analyzeBtn = document.getElementById("analyzeBtn");

    const dropZone =
        document.getElementById("dropZone") ||
        document.querySelector(".drop-zone");

    const uploadTitle = document.getElementById("uploadTitle");
    const dragText = document.getElementById("dragText");
    const selectedFile = document.getElementById("selectedFile");

    const MAX_FILE_SIZE = 20 * 1024 * 1024; // 20 MB

    // Store selected file
    let selectedEmailFile = null;


    // =========================
    // FILE VALIDATION
    // =========================
    function validateEmailFile(file) {

        if (!file) return false;

        if (!file.name.toLowerCase().endsWith(".eml")) {
            alert("Please select a valid .eml file.");
            return false;
        }

        if (file.size > MAX_FILE_SIZE) {
            alert("Maximum file size limit is 20 MB.");
            return false;
        }

        return true;
    }


    // =========================
    // DISPLAY SELECTED FILE
    // =========================
    function showSelectedFile(file) {

        if (!file) return;

        selectedEmailFile = file;

        if (uploadTitle) {
            uploadTitle.textContent = "Email selected";
        }

        if (dragText) {
            dragText.textContent = "Ready to analyze";
        }

        if (selectedFile) {
            selectedFile.textContent = "📄 " + file.name;
            selectedFile.style.display = "block";
        }

        // Enable Analyze button
        if (analyzeBtn) {
            analyzeBtn.disabled = false;
        }

        console.log("✅ File selected:", file.name);
    }


    // =========================
    // CHOOSE FILE BUTTON
    // =========================
    if (chooseFileBtn && fileInput) {

        chooseFileBtn.addEventListener("click", (e) => {

            e.preventDefault();
            e.stopPropagation();

            fileInput.click();
        });
    }


    // =========================
    // FILE INPUT CHANGE
    // =========================
    if (fileInput) {

        fileInput.addEventListener("change", (e) => {

            e.stopPropagation();

            const file = e.target.files[0];

            if (!file) return;

            if (!validateEmailFile(file)) {

                fileInput.value = "";
                selectedEmailFile = null;

                if (analyzeBtn) {
                    analyzeBtn.disabled = true;
                }

                return;
            }

            // ONLY show file
            // Backend call nahi hogi
            showSelectedFile(file);
        });
    }


    // =========================
    // DRAG & DROP
    // =========================
    if (dropZone) {

        ["dragenter", "dragover", "dragleave", "drop"].forEach(eventName => {

            dropZone.addEventListener(eventName, (e) => {

                e.preventDefault();
                e.stopPropagation();

            }, false);
        });


        dropZone.addEventListener("dragover", () => {

            dropZone.classList.add("drag-over");

        });


        dropZone.addEventListener("dragleave", () => {

            dropZone.classList.remove("drag-over");

        });


        dropZone.addEventListener("drop", (e) => {

            dropZone.classList.remove("drag-over");

            const files = e.dataTransfer.files;

            if (!files || files.length === 0) return;

            const file = files[0];

            if (!validateEmailFile(file)) return;


            // Put file inside input
            const dataTransfer = new DataTransfer();

            dataTransfer.items.add(file);

            fileInput.files = dataTransfer.files;


            // ONLY select file
            // Backend call nahi hogi
            showSelectedFile(file);
        });
    }


    // =========================
    // ANALYZE BUTTON
    // =========================
    if (analyzeBtn) {

        analyzeBtn.addEventListener("click", async () => {

            // No file selected
            if (!selectedEmailFile) {

                alert("Please upload an .eml file first.");

                return;
            }


            // =========================
            // ANALYZING STATE
            // =========================

            analyzeBtn.disabled = true;

            analyzeBtn.innerHTML = `
                <i data-lucide="loader-circle"></i>
                Analyzing...
            `;

            if (typeof lucide !== "undefined") {
                lucide.createIcons();
            }


            // =========================
            // SEND FILE TO BACKEND
            // =========================

            await uploadEmail(selectedEmailFile);

        });
    }


    // =========================
    // UPLOAD + ANALYZE EMAIL
    // =========================

//     async function uploadEmail(file) {

//     console.log("📁 FILE:", file.name);
//     console.log("📏 SIZE:", file.size);

//     const formData = new FormData();
//     formData.append("email", file);

//     console.log("📦 FormData:", formData.has("email"));
//     console.log("🚀 Starting XHR...");

//     return new Promise((resolve, reject) => {

//         const xhr = new XMLHttpRequest();

//         xhr.open(
//             "POST",
//             "http://localhost:5000/api/emails/analyze",
//             true
//         );

//         xhr.timeout = 10000;

//         xhr.onload = function () {

//             console.log("✅ XHR RESPONSE:", xhr.status);
//             console.log("📥 RESPONSE:", xhr.responseText);

//             try {

//                 const result = JSON.parse(xhr.responseText);

//                 if (xhr.status < 200 || xhr.status >= 300) {
//                     throw new Error(
//                         result.message || "File analysis failed"
//                     );
//                 }

//                 console.log("✅ EMAIL ANALYZED SUCCESSFULLY");
//                 console.log("🆔 Email ID:", result.emailId);

//                 window.location.href = "./analysis_result.html";

//                 resolve(result);

//             } catch (error) {

//                 console.error("❌ Response error:", error);

//                 analyzeBtn.disabled = false;

//                 analyzeBtn.innerHTML = `
//                     <i data-lucide="scan-search"></i>
//                     Analyze Email
//                 `;

//                 if (typeof lucide !== "undefined") {
//                     lucide.createIcons();
//                 }

//                 reject(error);
//             }
//         };

//         xhr.onerror = function () {

//             console.error("❌ XHR NETWORK ERROR");

//             analyzeBtn.disabled = false;

//             analyzeBtn.innerHTML = `
//                 <i data-lucide="scan-search"></i>
//                 Analyze Email
//             `;

//             if (typeof lucide !== "undefined") {
//                 lucide.createIcons();
//             }

//             reject(new Error("Unable to connect to backend"));
//         };

//         xhr.ontimeout = function () {

//             console.error("⏰ XHR TIMEOUT");

//             analyzeBtn.disabled = false;

//             analyzeBtn.innerHTML = `
//                 <i data-lucide="scan-search"></i>
//                 Analyze Email
//             `;

//             if (typeof lucide !== "undefined") {
//                 lucide.createIcons();
//             }

//             reject(new Error("Backend request timed out"));
//         };

//         xhr.onabort = function () {
//             console.error("🛑 XHR ABORTED");
//             reject(new Error("Request aborted"));
//         };

//         console.log("📤 Sending file to backend...");

//         xhr.send(formData);
//     });
// }


// async function uploadEmail(file) {

//     console.log("📁 FILE:", file.name);
//     console.log("📏 SIZE:", file.size);

//     const formData = new FormData();
//     formData.append("email", file);

//     try {

//         console.log("📤 Sending EML file to backend...");

//         const response = await fetch(
//             "http://localhost:5000/api/emails/analyze",
//             {
//                 method: "POST",
//                 body: formData
//             }
//         );

//         console.log("✅ Backend response:", response.status);

//         const result = await response.json();

//         console.log("📥 Backend result:", result);

//         if (!response.ok) {
//             throw new Error(
//                 result.message || "Email analysis failed"
//             );
//         }

//         console.log("✅ EMAIL ANALYZED SUCCESSFULLY");
//         console.log("🆔 Email ID:", result.emailId);

//         // Save latest analyzed email ID
//         localStorage.setItem(
//             "lastAnalyzedEmailId",
//             result.emailId
//         );

//         // Redirect
//         // window.location.replace("analysis_result.html");

//         console.log("✅ EMAIL ANALYZED SUCCESSFULLY");
//         console.log("🆔 Email ID:", result.emailId);

//         localStorage.setItem(
//             "lastAnalyzedEmailId",
//             result.emailId
//         );

//         window.location.href =
//             "http://localhost:3000/frontend/user/analysis_result.html";

//     } catch (error) {

//         console.error("❌ Analysis error:", error);

//         alert(
//             error.message ||
//             "Unable to analyze email. Please try again."
//         );

//         analyzeBtn.disabled = false;

//         analyzeBtn.innerHTML = `
//             <i data-lucide="scan-search"></i>
//             Analyze Email
//         `;

//         if (typeof lucide !== "undefined") {
//             lucide.createIcons();
//         }
//     }
// }



async function uploadEmail(file) {

    console.log("📁 FILE:", file.name);
    console.log("📏 SIZE:", file.size);

    const formData = new FormData();
    formData.append("email", file);

    try {

        console.log("📤 Sending EML file to backend...");

        const response = await fetch(
            "http://localhost:5000/api/emails/analyze",
            {
                method: "POST",
                body: formData
            }
        );

        console.log("✅ Response received:", response.status);

        const result = await response.json();

        console.log("📥 Result:", result);

        if (!response.ok) {
            throw new Error(
                result.message || "Email analysis failed"
            );
        }

        // Save ID for result page
        localStorage.setItem(
            "lastAnalyzedEmailId",
            result.emailId
        );

        console.log("🎯 REDIRECTING NOW");

        // HARD-CODED REDIRECT
        window.location.href =
            "http://127.0.0.1:3000/frontend/user/analysis_result.html";

    } catch (error) {

        console.error("❌ Analysis failed:", error);

        alert(error.message || "Unable to analyze email.");

        analyzeBtn.disabled = false;

        analyzeBtn.innerHTML = `
            <i data-lucide="scan-search"></i>
            Analyze Email
        `;

        if (typeof lucide !== "undefined") {
            lucide.createIcons();
        }
    }
}

//     async function uploadEmail(file) {

//         const formData = new FormData();

//         formData.append("email", file);

//         console.log("📤 Sending EML file to server:", file.name);


//         try {

//             console.log("📤 Sending EML file to server:", file.name);
// console.log("🌐 Calling backend...");

// const response = await fetch(
//     "http://localhost:5000/api/emails/analyze",
//             {
//                 method: "POST",
//                 body: formData
//             }
//         );

//         console.log("✅ Backend response received:", response.status);

//         const result = await response.json();

//         console.log("📥 Backend result:", result);


//             if (!response.ok) {

//                 throw new Error(
//                     result.message || "File analysis failed"
//                 );
//             }


//             console.log(
//                 "📥 Backend Analysis Result:",
//                 result
//             );


//             // =========================
//             // ANALYSIS SUCCESS
//             // =========================

//             /*
//                 Ab backend ne:
//                 1. .eml parse ki
//                 2. analysis ki
//                 3. MongoDB me save ki
//             */

//                 console.log("✅ Analysis saved successfully");
//                 console.log("➡️ Redirecting to analysis_result.html");
//             // Demo ke liye result page
//             window.location.href = "./analysis_result.html";


//         } catch (error) {

//             console.error("❌ Analysis error:", error);

//             alert(
//                 error.message ||
//                 "Unable to analyze email. Please try again."
//             );


//             // Enable button again
//             analyzeBtn.disabled = false;

//             analyzeBtn.innerHTML = `
//                 <i data-lucide="scan-search"></i>
//                 Analyze Email
//             `;

//             if (typeof lucide !== "undefined") {
//                 lucide.createIcons();
//             }
//         }
//     }


    // =========================
    // HELP MODAL
    // =========================
    const helpBtn = document.getElementById("emailhelpBtn");
    const helpModal = document.getElementById("helpModal");
    const closeModal = document.getElementById("closeModal");
    const gotIt = document.getElementById("gotIt");


    if (helpBtn && helpModal) {

        helpBtn.addEventListener("click", () => {

            helpModal.classList.add("active");

        });
    }


    if (closeModal && helpModal) {

        closeModal.addEventListener("click", () => {

            helpModal.classList.remove("active");

        });
    }


    if (gotIt && helpModal) {

        gotIt.addEventListener("click", () => {

            helpModal.classList.remove("active");

        });
    }


    if (helpModal) {

        helpModal.addEventListener("click", (e) => {

            if (e.target === helpModal) {

                helpModal.classList.remove("active");

            }
        });
    }

});

