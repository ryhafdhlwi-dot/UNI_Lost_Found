let reportForm = document.getElementById("reportForm");

if (reportForm) {
    reportForm.addEventListener("submit", function(e) {

        let category = document.getElementById("category").value;
        let description = document.getElementById("description").value.trim();
        let gate = document.getElementById("gate").value;
        let image = document.getElementById("image").value;

        // 1) تأكد إن كل الحقول متعبية
        if (category === "" || description === "" || gate === "" || image === "") {
            alert("Please fill all required fields!");
            e.preventDefault();
            return;
        }

        // 2) يمنع الأرقام فقط
        if (/^[0-9]+$/.test(description)) {
            alert("Description cannot be numbers only. Please describe the lost item.");
            e.preventDefault();
            return;
        }

        // 3) لازم يحتوي حروف (عربي أو إنجليزي)
        if (!/[a-zA-Z\u0600-\u06FF]/.test(description)) {
            alert("Please enter a real description (letters required).");
            e.preventDefault();
            return;
        }

        // 4) أقل طول 5 أحرف
        if (description.length < 5) {
            alert("Description must be at least 5 characters.");
            e.preventDefault();
            return;
        }

    });
}