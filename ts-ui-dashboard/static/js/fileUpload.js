$("#upload").click(function() {

    $.ajax({
        url: "/adminroute/upload",
        type: 'POST',
        cache: false,
        data: new FormData($("#uploadForm")[0]),
        processData: false,
        contentType: false,
        success: function (result) {
            alert("Success");
        },
        error: function (err) {
            alert("Upload Route List Fail.");
        }
    });
});
