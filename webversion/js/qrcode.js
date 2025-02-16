$(document).ready(function() {
    const $video = $('#video');
    const $startButton = $('#startButton');
    const $output = $('#output');

    $startButton.on('click', startScanning);
    $output.on('click', goToMainPage);

    function startScanning() {
        navigator.mediaDevices.getUserMedia({ video: { facingMode: "environment" } })
            .then(function(stream) {
                $video[0].srcObject = stream;
                $video.attr("playsinline", true);
                $video[0].play();
                requestAnimationFrame(tick);
                $startButton.prop('disabled', true).text('Scanning...');
            })
            .catch(function(err) {
                console.error("카메라 액세스 오류:", err);
                $output.text("카메라 액세스 오류: " + err.message)
                       .removeClass('alert-info').addClass('alert-danger')
                       .show();
            });
    }

    function tick() {
        if ($video[0].readyState === $video[0].HAVE_ENOUGH_DATA) {
            const canvas = document.createElement("canvas");
            canvas.width = $video[0].videoWidth;
            canvas.height = $video[0].videoHeight;
            const ctx = canvas.getContext("2d");
            ctx.drawImage($video[0], 0, 0, canvas.width, canvas.height);
            const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
            const code = jsQR(imageData.data, imageData.width, imageData.height);

            if (code) {
                console.log("QR 코드 내용:", code.data);
                $output.text("QR code: " + code.data)
                       .removeClass('alert-info').addClass('alert-success')
                       .show();
                $output.data('qrData', code.data);
                $startButton.prop('disabled', false).text('다시 스캔');
                return;
            }
        }
        requestAnimationFrame(tick);
    }

    function goToMainPage() {
        const qrData = $output.data('qrData');
        if (qrData) {
            window.location.href = 'main.html?url=' + encodeURIComponent(qrData);
        }
    }
});