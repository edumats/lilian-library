document.addEventListener('DOMContentLoaded', () => {
    // Start/stop scanner button
    document.getElementById("cam-btn").addEventListener("click", function () {
        if (_scannerIsRunning) {
            Quagga.stop();
        } else {
            startScanner();
        }
    }, false);

    // Variable used for starting/stopping camera
    let _scannerIsRunning = false;

    // For barcode scanner features
    function startScanner() {
        // Config for initializing camera
        Quagga.init({
            inputStream: {
                name: "Live",
                type: "LiveStream",
                target: document.querySelector('#scanner-container'),
                constraints: {
                    width: 800,
                    height: 600,
                    facingMode: "environment"
                },
                area: { // defines rectangle of the detection/localization area
                    top: "20%",    // top offset
                    right: "20%",  // right offset
                    left: "20%",   // left offset
                    bottom: "20%"  // bottom offset
                },
            },
            locate: false,
            decoder: {
                readers: [
                    "ean_reader",
                ],
                debug: {
                    showCanvas: false,
                    showPatches: true,
                    showFoundPatches: true,
                    showSkeleton: true,
                    showLabels: true,
                    showPatchLabels: true,
                    showRemainingPatchLabels: true,
                    boxFromPatches: {
                        showTransformed: true,
                        showTransformedBox: true,
                        showBB: true
                    }
                }
            },

        }, function (err) {
            if (err) {
                console.log(err);
                return
            }

            console.log("Initialization finished. Ready to start");
            Quagga.start();

            // Set flag to is running
            _scannerIsRunning = true;
        });


        // Checks result and draws boxes or a box on page
        // Draws red line if it is a final result
        Quagga.onProcessed(function (result) {
            var drawingCtx = Quagga.canvas.ctx.overlay,
            drawingCanvas = Quagga.canvas.dom.overlay;

            if (result) {
                if (result.boxes) {
                    drawingCtx.clearRect(0, 0, parseInt(drawingCanvas.getAttribute("width")), parseInt(drawingCanvas.getAttribute("height")));
                    result.boxes.filter(function (box) {
                        return box !== result.box;
                    }).forEach(function (box) {
                        Quagga.ImageDebug.drawPath(box, { x: 0, y: 1 }, drawingCtx, { color: "green", lineWidth: 2 });
                    });
                }

                if (result.box) {
                    Quagga.ImageDebug.drawPath(result.box, { x: 0, y: 1 }, drawingCtx, { color: "#00F", lineWidth: 2 });
                }

                if (result.codeResult && result.codeResult.code) {
                    Quagga.ImageDebug.drawPath(result.line, { x: 'x', y: 'y' }, drawingCtx, { color: 'red', lineWidth: 3 });
                }
            }
        });

        // Runs when a code is retrieved from a barcode
        Quagga.onDetected(function (result) {
            // Gets the code extracted from barcode
            let code = result.codeResult.code;

            // Parses code into ISBN checker
            let isbn = ISBN.parse(code);

            // Checker returns null if not a ISBN code
            if (isbn != null) {
                // If ISBN is in a valid format, paste into input field
                if (isbn.isValid()) {
                    console.log("Barcode detected and processed : [" + code + "]", result);
                    // Parse checked code to input field
                    document.getElementsByName('isbn')[0].value = code;

                    // Submits the form
                    document.querySelector('#submit-isbn').submit();
                } else {
                    console.log('Not valid');
                }
            } else {
                console.log('Code failed ISBN check');
            }
        });
    }
})
